from io import BytesIO
from pathlib import Path
from uuid import uuid4
from pypdf import PdfReader
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..auth import roles
from ..config import settings
from ..storage import save_evidence, delete_evidence
import logging
from ..database import get_db
from ..models import User, Company, Program, Report, AuditEvent
from ..schemas import Note
from ..services import visible_program, program_view, report_view, accessible_report

router = APIRouter(prefix='/api/hacker', tags=['Researcher'])

@router.get('/programs')
def programs(db: Session = Depends(get_db)):
    return [program_view(p) for p in db.scalars(select(Program).join(Company).where(Program.is_approved.is_(True), Program.is_active.is_(True), Company.is_approved.is_(True)).order_by(Program.id.desc()))]

@router.get('/programs/{program_id}')
def program(program_id: int, db: Session = Depends(get_db)):
    return program_view(visible_program(db, program_id))

def validate_evidence(content, suffix):
    if suffix == '.txt':
        try:
            text = content.decode('utf-8')
            if '\x00' in text:
                raise ValueError()
        except (UnicodeDecodeError, ValueError):
            raise HTTPException(422, 'TXT evidence must be UTF-8 plain text.')
    elif suffix == '.pdf':
        if not content.startswith(b'%PDF-'):
            raise HTTPException(422, 'Invalid PDF file.')
        try:
            reader = PdfReader(BytesIO(content), strict=True)
            if reader.is_encrypted:
                raise ValueError('Encrypted PDF')
            root = reader.trailer['/Root']
            if any(key in root for key in ('/OpenAction', '/AA', '/AcroForm')):
                raise ValueError('Active PDF')
            if '/JavaScript' in root.get('/Names', {}):
                raise ValueError('JavaScript PDF')
            for page in reader.pages:
                if '/AA' in page or '/Annots' in page:
                    raise ValueError('Interactive PDF')
        except Exception:
            raise HTTPException(422, 'Use a readable, unencrypted PDF without scripts, forms or interactive annotations.')
    else:
        raise HTTPException(422, 'Only .pdf and .txt files are accepted.')

@router.post('/reports', status_code=201)
def submit(program_id: int = Form(...), title: str = Form(..., min_length=5, max_length=200), cwe_category: str = Form(..., min_length=1, max_length=100), attachment: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(roles('hacker'))):
    program = visible_program(db, program_id)
    if not title.strip() or not cwe_category.strip() or not attachment.filename:
        raise HTTPException(422, 'Başlıq, kateqoriya və sübut faylı tələb olunur.')
    filename = None
    if attachment and attachment.filename:
        suffix = Path(attachment.filename).suffix.lower()
        if suffix not in {'.pdf', '.txt'}:
            raise HTTPException(422, 'Only .pdf and .txt files are accepted.')
        content = attachment.file.read(settings.max_upload_bytes + 1)
        if not content or len(content) > settings.max_upload_bytes:
            raise HTTPException(413, 'Sübut faylı boş olmamalı və 4 MB həddini keçməməlidir.')
        validate_evidence(content, suffix)
        filename = uuid4().hex + suffix
        save_evidence(filename, content)
    report = Report(program_id=program.id, hacker_id=user.id, title=title.strip(), cwe_category=cwe_category.strip(), cvss_score=0, cvss_vector='', severity='Low', severity_reviewed=False, poc_steps='', impact='', http_payload='', attachment_path=filename)
    try:
        db.add(report)
        db.commit()
    except Exception:
        db.rollback()
        if filename:
            try:
                delete_evidence(filename)
            except HTTPException:
                logging.getLogger('bugcasp').warning('An unreferenced evidence object needs operator cleanup.')
        raise
    db.refresh(report)
    return report_view(report)

@router.get('/my-reports')
def reports(db: Session = Depends(get_db), user: User = Depends(roles('hacker'))):
    return [report_view(r) for r in db.scalars(select(Report).where(Report.hacker_id == user.id).order_by(Report.id.desc()))]

@router.post('/reports/{report_id}/dispute')
def dispute(report_id: int, data: Note, db: Session = Depends(get_db), user: User = Depends(roles('hacker'))):
    report = accessible_report(db, user, report_id)
    report.dispute = data.note
    db.add(AuditEvent(actor_id=user.id, subject=f'report:{report.id}', action='Dispute: ' + data.note))
    db.commit()
    return report_view(report)

@router.get('/leaderboard')
def leaderboard(db: Session = Depends(get_db)):
    resolved = select(Report.hacker_id, func.count(Report.id).label('count')).where(Report.status == 'Resolved').group_by(Report.hacker_id).subquery()
    rows = db.execute(select(User, func.coalesce(resolved.c.count, 0)).outerjoin(resolved, resolved.c.hacker_id == User.id).where(User.role == 'hacker', User.is_email_verified.is_(True)).order_by(User.reputation_score.desc(), User.id).limit(100))
    return [{'username': u.username, 'bio': u.bio, 'github': u.github, 'tryhackme': u.tryhackme, 'hackthebox': u.hackthebox, 'reputation_score': u.reputation_score, 'resolved_bugs': count} for u, count in rows]
