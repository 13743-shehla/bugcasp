"""Validated public profile images, admin operations and private report discussions."""
from datetime import date, datetime, timedelta, time
from io import BytesIO
from uuid import uuid4
import warnings
from typing import Literal
from PIL import Image, ImageOps, UnidentifiedImageError
from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, func, or_, update, delete
from sqlalchemy.orm import Session
from ..auth import current_user, roles, rate_limit
from ..database import get_db
from ..models import User, Company, Program, Report, AuditEvent, MediaImage, Announcement, ReportMessage, now
from ..services import user_view, company_view, program_view, report_view, own_company, accessible_report

router = APIRouter(prefix='/api', tags=['Management'])
admin = roles('superadmin')

class Decision(BaseModel):
    reason: str = Field(min_length=3, max_length=2000)
    @field_validator('reason')
    @classmethod
    def not_blank(cls, value):
        if len(value.strip()) < 3:
            raise ValueError('Səbəb tələb olunur.')
        return value.strip()

class Block(Decision):
    days: int = Field(ge=0, le=365)

class Suspend(Decision):
    suspended: bool

class AnnouncementInput(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    body: str = Field(min_length=3, max_length=3000)
    active: bool = False
    @field_validator('title', 'body')
    @classmethod
    def not_blank(cls, value):
        if len(value.strip()) < 3:
            raise ValueError('Mətn tələb olunur.')
        return value.strip()

class MessageInput(BaseModel):
    body: str = Field(min_length=3, max_length=5000)
    @field_validator('body')
    @classmethod
    def not_blank(cls, value):
        if len(value.strip()) < 3:
            raise ValueError('Mətn tələb olunur.')
        return value.strip()

def log(db, actor, subject, action):
    db.add(AuditEvent(actor_id=actor.id, subject=subject, action=action))

def blocked(user):
    return bool(user.blocked_until and user.blocked_until > now())

def normalized_image(content):
    if not content or len(content) > 2 * 1024 * 1024:
        raise HTTPException(413, 'Şəkil boş olmamalı və 2 MB həddini keçməməlidir.')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(BytesIO(content)) as source:
                if source.format not in ('JPEG', 'PNG', 'WEBP') or source.width * source.height > 16000000:
                    raise ValueError()
                source.seek(0)
                photo = ImageOps.exif_transpose(source).convert('RGBA')
                photo.thumbnail((384, 384))
                # Re-encode to remove metadata, animation and trailing payloads.
                output = BytesIO()
                photo.save(output, format='PNG', optimize=True)
                return output.getvalue()
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(422, 'JPG, PNG və ya WebP şəkli seçin (maksimum 16 meqapiksel).')

@router.post('/profile-image')
def upload_image(request: Request, image: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(roles('hacker', 'company'))):
    rate_limit(request, 'profile-image', 15, db=db, identifier=str(user.id))
    content = normalized_image(image.file.read(2 * 1024 * 1024 + 1))
    owner = db.scalar(select(User).where(User.id == user.id).with_for_update().execution_options(populate_existing=True))
    target = own_company(db, owner) if owner.role == 'company' else owner
    attr = 'logo_id' if owner.role == 'company' else 'avatar_id'
    old_id = getattr(target, attr)
    item = MediaImage(id=uuid4().hex, owner_id=owner.id, content=content)
    db.add(item)
    setattr(target, attr, item.id)
    if old_id:
        db.execute(delete(MediaImage).where(MediaImage.id == old_id, MediaImage.owner_id == owner.id))
    log(db, owner, f'user:{owner.id}', 'Profile image updated.')
    db.commit()
    return {'url': '/api/media/' + item.id}

@router.post('/profile-image/remove')
def remove_image(db: Session = Depends(get_db), user: User = Depends(roles('hacker', 'company'))):
    owner = db.scalar(select(User).where(User.id == user.id).with_for_update().execution_options(populate_existing=True))
    target = own_company(db, owner) if owner.role == 'company' else owner
    attr = 'logo_id' if owner.role == 'company' else 'avatar_id'
    old_id = getattr(target, attr)
    setattr(target, attr, None)
    if old_id:
        db.execute(delete(MediaImage).where(MediaImage.id == old_id, MediaImage.owner_id == owner.id))
    log(db, owner, f'user:{owner.id}', 'Profile image removed.')
    db.commit()
    return {'url': None}

@router.get('/media/{image_id}')
def image_file(image_id: str, db: Session = Depends(get_db)):
    item = db.get(MediaImage, image_id)
    if not item:
        raise HTTPException(404, 'Şəkil tapılmadı.')
    owner = db.get(User, item.owner_id)
    if blocked(owner):
        raise HTTPException(404, 'Şəkil tapılmadı.')
    return Response(item.content, media_type='image/png', headers={'X-Content-Type-Options': 'nosniff'})

@router.get('/admin/users')
def users(q: str = Query(default='', max_length=100), role: Literal['', 'hacker', 'company', 'superadmin'] = '', page: int = Query(default=1, ge=1), db: Session = Depends(get_db), actor: User = Depends(admin)):
    filters = []
    if q:
        filters.append(or_(User.username.icontains(q, autoescape=True), User.email.icontains(q, autoescape=True)))
    if role:
        filters.append(User.role == role)
    total = db.scalar(select(func.count(User.id)).where(*filters))
    rows = db.scalars(select(User).where(*filters).order_by(User.id.desc()).offset((page-1)*20).limit(20))
    return {'total': total, 'items': [{**user_view(u), 'company': company_view(u.company) if u.company else None, 'blocked': blocked(u), 'blocked_until': u.blocked_until, 'block_reason': u.block_reason, 'created_at': u.created_at} for u in rows]}

@router.put('/admin/users/{user_id}/block')
def block_user(user_id: int, data: Block, db: Session = Depends(get_db), actor: User = Depends(admin)):
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(404, 'İstifadəçi tapılmadı.')
    if target.role == 'superadmin':
        raise HTTPException(409, 'Admin hesabı bloklana bilməz.')
    db.execute(update(User).where(User.id == user_id).values(blocked_until=now()+timedelta(days=data.days) if data.days else None, block_reason=data.reason, token_version=User.token_version+1))
    log(db, actor, f'user:{user_id}', f'Block days={data.days}: {data.reason}')
    db.commit()
    return {'ok': True}

@router.get('/admin/programs')
def programs(q: str = Query(default='', max_length=100), page: int = Query(default=1, ge=1), db: Session = Depends(get_db), actor: User = Depends(admin)):
    filters = [Program.title.icontains(q, autoescape=True)] if q else []
    total = db.scalar(select(func.count(Program.id)).where(*filters))
    return {'total': total, 'items': [program_view(p) for p in db.scalars(select(Program).where(*filters).order_by(Program.id.desc()).offset((page-1)*20).limit(20))]}

@router.put('/admin/programs/{program_id}/suspension')
def suspend_program(program_id: int, data: Suspend, db: Session = Depends(get_db), actor: User = Depends(admin)):
    item = db.get(Program, program_id)
    if not item:
        raise HTTPException(404, 'Program not found.')
    item.admin_suspended = data.suspended
    item.suspension_reason = data.reason
    log(db, actor, f'program:{program_id}', f'Admin suspended={data.suspended}: {data.reason}')
    db.commit()
    return program_view(item)

@router.get('/admin/history')
def history(q: str = Query(default='', max_length=100), page: int = Query(default=1, ge=1), db: Session = Depends(get_db), actor: User = Depends(admin)):
    filters = [or_(AuditEvent.subject.icontains(q, autoescape=True), AuditEvent.action.icontains(q, autoescape=True), User.username.icontains(q, autoescape=True))] if q else []
    query = select(AuditEvent, User.username).join(User, User.id == AuditEvent.actor_id).where(*filters)
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    return {'total': total, 'items': [{'actor': name, 'subject': e.subject, 'action': e.action, 'created_at': e.created_at} for e,name in db.execute(query.order_by(AuditEvent.id.desc()).offset((page-1)*20).limit(20))]}

@router.get('/admin/overview')
def overview(start: date | None = None, end: date | None = None, db: Session = Depends(get_db), actor: User = Depends(admin)):
    if start and end and start > end:
        raise HTTPException(422, 'Tarix aralığı yanlışdır.')
    def within(model):
        return ([model.created_at >= datetime.combine(start, time.min)] if start else []) + ([model.created_at <= datetime.combine(end, time.max)] if end else [])
    def count(model, *where):
        return db.scalar(select(func.count(model.id)).where(*within(model), *where))
    return {'users': count(User), 'companies': count(Company), 'programs': count(Program), 'reports': count(Report),
            'pending_companies': count(Company, Company.review_state == 'pending'), 'pending_programs': count(Program, Program.review_state == 'pending'),
            'open_reports': count(Report, Report.status.in_(['New', 'Triaged'])), 'resolved_reports': count(Report, Report.status == 'Resolved'),
            'disputes': count(Report, Report.dispute_open.is_(True)),
            'payouts': dict(db.execute(select(Program.currency, func.sum(Report.cash_awarded)).join(Report).where(*within(Report), Report.payout_paid.is_(True)).group_by(Program.currency)).all())}

@router.get('/admin/notifications')
def notifications(db: Session = Depends(get_db), actor: User = Depends(admin)):
    # A live work queue: handled items leave the queue automatically.
    companies = db.scalar(select(func.count(Company.id)).join(User).where(Company.review_state == 'pending', User.is_email_verified.is_(True)))
    programs = db.scalar(select(func.count(Program.id)).where(Program.review_state == 'pending'))
    disputes = db.scalar(select(func.count(Report.id)).where(Report.dispute_open.is_(True)))
    return {'companies': companies, 'programs': programs, 'disputes': disputes, 'total': companies+programs+disputes}

@router.get('/admin/disputes')
def disputes(state: Literal['open','closed'] = 'open', page: int = Query(default=1, ge=1), db: Session = Depends(get_db), actor: User = Depends(admin)):
    filters = [Report.dispute != '', Report.dispute_open.is_(state == 'open')]
    return {'total': db.scalar(select(func.count(Report.id)).where(*filters)), 'items': [report_view(r) for r in db.scalars(select(Report).where(*filters).order_by(Report.id.desc()).offset((page-1)*20).limit(20))]}

@router.put('/admin/disputes/{report_id}/resolve')
def resolve_dispute(report_id: int, data: Decision, db: Session = Depends(get_db), actor: User = Depends(admin)):
    item = db.scalar(select(Report).where(Report.id == report_id).with_for_update())
    if not item:
        raise HTTPException(404, 'Report not found.')
    if not item.dispute_open:
        raise HTTPException(409, 'Mübahisə artıq bağlanıb.')
    item.mediation = data.reason
    item.dispute_open = False
    log(db, actor, f'report:{report_id}', 'Dispute resolved: ' + data.reason)
    db.commit()
    return report_view(item)

@router.get('/reports/{report_id}/messages')
def messages(report_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    accessible_report(db, user, report_id)
    return [{'author': name, 'role': role, 'body': m.body, 'created_at': m.created_at} for m,name,role in db.execute(select(ReportMessage, User.username, User.role).join(User, User.id == ReportMessage.author_id).where(ReportMessage.report_id == report_id).order_by(ReportMessage.id))]

@router.post('/reports/{report_id}/messages')
def add_message(report_id: int, data: MessageInput, request: Request, db: Session = Depends(get_db), user: User = Depends(current_user)):
    accessible_report(db, user, report_id)
    rate_limit(request, 'report-message', 30, db=db, identifier=str(user.id))
    db.add(ReportMessage(report_id=report_id, author_id=user.id, body=data.body))
    log(db, user, f'report:{report_id}', 'Report discussion message added.')
    db.commit()
    return {'ok': True}

@router.get('/announcements')
def announcements(db: Session = Depends(get_db)):
    return [{'id': a.id, 'title': a.title, 'body': a.body} for a in db.scalars(select(Announcement).where(Announcement.active.is_(True)).order_by(Announcement.id.desc()).limit(10))]

@router.get('/admin/announcements')
def admin_announcements(page: int = Query(default=1, ge=1), db: Session = Depends(get_db), actor: User = Depends(admin)):
    return {'total': db.scalar(select(func.count(Announcement.id))), 'items': [{'id': a.id, 'title': a.title, 'body': a.body, 'active': a.active} for a in db.scalars(select(Announcement).order_by(Announcement.id.desc()).offset((page-1)*20).limit(20))]}

@router.post('/admin/announcements')
def create_announcement(data: AnnouncementInput, db: Session = Depends(get_db), actor: User = Depends(admin)):
    item = Announcement(**data.model_dump())
    db.add(item)
    db.flush()
    log(db, actor, f'announcement:{item.id}', 'Announcement created; active=' + str(item.active))
    db.commit()
    return {'id': item.id}

@router.put('/admin/announcements/{item_id}')
def edit_announcement(item_id: int, data: AnnouncementInput, db: Session = Depends(get_db), actor: User = Depends(admin)):
    item = db.get(Announcement, item_id)
    if not item:
        raise HTTPException(404, 'Elan tapılmadı.')
    for key,value in data.model_dump().items():
        setattr(item, key, value)
    log(db, actor, f'announcement:{item.id}', 'Announcement updated; active=' + str(item.active))
    db.commit()
    return {'id': item.id}
