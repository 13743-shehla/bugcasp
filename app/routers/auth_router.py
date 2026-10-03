from datetime import timedelta
import hashlib
import secrets
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..auth import current_user, passwords, dummy_hash, create_token, rate_limit
from ..config import settings
from ..database import get_db
from ..models import User, Company, Verification, PasswordReset, AuditEvent, now
from ..schemas import Register, Login, EmailCheck, Verify, AccountUpdate, ResetPassword, ProfileUpdate
from ..services import user_view
from ..email_verifier import verify_email_domain, send_verification, send_welcome, send_password_reset

router = APIRouter(prefix='/api/auth', tags=['Authentication'])

def issue_verification(db, user):
    token = secrets.token_urlsafe(32)
    db.execute(delete(Verification).where(Verification.user_id == user.id))
    db.add(Verification(user_id=user.id, token_hash=hashlib.sha256(token.encode()).hexdigest(), expires_at=now() + timedelta(minutes=30)))
    db.commit()
    return send_verification(user, token)

@router.post('/check-email')
def check_email(data: EmailCheck, request: Request, db: Session = Depends(get_db)):
    rate_limit(request, 'email-check', 30, db=db)
    verify_email_domain(data.email)
    return {'valid': True, 'message': 'Mail server found. Confirm the link we send to prove mailbox ownership.'}

@router.post('/register', status_code=201)
def register(data: Register, request: Request, db: Session = Depends(get_db)):
    rate_limit(request, 'register', 8, db=db)
    if data.username.lower() == settings.bootstrap_admin_username.lower():
        raise HTTPException(409, 'Bu istifadəçi adı platforma sahibi üçün ayrılıb.')
    email = verify_email_domain(data.email)
    user = User(username=data.username.lower(), email=email, password_hash=passwords.hash(data.password), role=data.role, bio=data.bio, github=data.github, tryhackme=data.tryhackme, hackthebox=data.hackthebox)
    try:
        db.add(user)
        db.flush()
        if data.role == 'company':
            db.add(Company(user_id=user.id, company_name=data.company_name, industry=data.industry, website_url=data.website_url))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'Email or handle already registered.')
    delivery = issue_verification(db, user)
    return {'message': 'Registration is pending email verification.', 'email_delivery': delivery, 'is_email_verified': False}

@router.post('/resend-verification')
def resend(data: EmailCheck, request: Request, db: Session = Depends(get_db)):
    rate_limit(request, 'resend', 5, db=db)
    user = db.scalar(select(User).where(User.email == data.email.strip().lower()))
    if user and not user.is_email_verified:
        issue_verification(db, user)
    return {'message': 'If a pending account exists, a new verification email has been requested.'}

@router.post('/verify-email')
def verify(data: Verify, request: Request, db: Session = Depends(get_db)):
    rate_limit(request, 'verify', 20, db=db)
    digest = hashlib.sha256(data.token.encode()).hexdigest()
    record = db.scalar(select(Verification).where(Verification.token_hash == digest, Verification.expires_at > now()))
    if not record:
        raise HTTPException(400, 'This verification link is invalid or expired. Request a new one.')
    user = db.get(User, record.user_id)
    consumed = db.execute(delete(Verification).where(Verification.id == record.id))
    if consumed.rowcount != 1:
        db.rollback()
        raise HTTPException(400, 'This link has already been used.')
    user.is_email_verified = True
    db.commit()
    delivery = send_welcome(user)
    return {'message': 'Email verified. You can now sign in.', 'welcome_email': delivery}

@router.post('/login')
def login(data: Login, request: Request, response: Response, db: Session = Depends(get_db)):
    identifier = data.identifier.strip().lower()
    rate_limit(request, 'login', 15, db=db)
    user = db.scalar(select(User).where((User.email == identifier) | (User.username == identifier)))
    try:
        valid = len(data.password.encode()) <= 72 and passwords.verify(data.password, user.password_hash if user else dummy_hash)
    except (ValueError, TypeError):
        valid = False
    if not user or not valid:
        raise HTTPException(401, 'İstifadəçi adı, e-poçt və ya şifrə yanlışdır.')
    if not user.is_email_verified:
        raise HTTPException(403, 'Verify your email before signing in.')
    token = create_token(user)
    response.set_cookie('bugcasp_session', token, httponly=True, secure=settings.cookie_secure, samesite='strict', max_age=28800)
    return {'access_token': token, 'token_type': 'bearer', 'user': user_view(user)}

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie('bugcasp_session', secure=settings.cookie_secure, httponly=True, samesite='strict')
    return {'message': 'Signed out.'}

@router.get('/me')
def me(user: User = Depends(current_user)):
    return user_view(user)

@router.get('/username-availability')
def username_availability(request: Request, username: str = Query(min_length=3, max_length=40, pattern=r'^[a-zA-Z0-9_-]+$'), db: Session = Depends(get_db), user: User = Depends(current_user)):
    rate_limit(request, 'username-check', 60, db=db, identifier=str(user.id))
    username = username.lower()
    reserved = user.role != 'superadmin' and username == settings.bootstrap_admin_username.lower()
    taken = db.scalar(select(User.id).where(User.username == username, User.id != user.id)) is not None
    return {'username': username, 'available': not reserved and not taken}

@router.put('/profile')
def update_profile(data: ProfileUpdate, request: Request, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if user.role != 'hacker':
        raise HTTPException(403, 'Tədqiqatçı hesabı tələb olunur.')
    rate_limit(request, 'profile-change', 15, db=db, identifier=str(user.id))
    for field, value in data.model_dump().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return {'user': user_view(user)}

@router.put('/account')
def change_account(data: AccountUpdate, request: Request, response: Response, db: Session = Depends(get_db), user: User = Depends(current_user)):
    rate_limit(request, 'account-change', 5, db=db, identifier=str(user.id))
    if len(data.current_password.encode()) > 72 or not passwords.verify(data.current_password, user.password_hash):
        raise HTTPException(403, 'Cari şifrə yanlışdır.')
    values = {'token_version': User.token_version + 1}
    if data.username is not None:
        username = data.username.lower()
        if user.role != 'superadmin' and username == settings.bootstrap_admin_username.lower():
            raise HTTPException(409, 'Bu istifadəçi adı ayrılıb.')
        values['username'] = username
    if data.new_password is not None:
        values['password_hash'] = passwords.hash(data.new_password)
    try:
        changed = db.execute(update(User).where(User.id == user.id, User.token_version == user.token_version).values(**values))
        if changed.rowcount != 1:
            db.rollback()
            raise HTTPException(409, 'Hesab başqa sorğuda yenilənib. Yenidən daxil olun.')
        db.add(AuditEvent(actor_id=user.id, subject=f'user:{user.id}', action='Account credentials updated; previous sessions revoked.'))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'Bu istifadəçi adı artıq istifadə olunur.')
    db.refresh(user)
    token = create_token(user)
    response.set_cookie('bugcasp_session', token, httponly=True, secure=settings.cookie_secure, samesite='strict', max_age=28800)
    return {'message': 'Hesab yeniləndi. Köhnə sessiyalar bağlandı.', 'user': user_view(user), 'access_token': token, 'token_type': 'bearer'}

@router.post('/forgot-password')
def forgot_password(data: EmailCheck, request: Request, db: Session = Depends(get_db)):
    rate_limit(request, 'forgot-password', 5, db=db)
    user = db.scalar(select(User).where(User.email == data.email.strip().lower(), User.is_email_verified.is_(True)))
    if user:
        token = secrets.token_urlsafe(32)
        db.execute(delete(PasswordReset).where(PasswordReset.user_id == user.id))
        db.add(PasswordReset(user_id=user.id, token_hash=hashlib.sha256(token.encode()).hexdigest(), token_version=user.token_version, expires_at=now() + timedelta(minutes=30)))
        db.commit()
        send_password_reset(user, token)
    return {'message': 'Bu e-poçtla təsdiqlənmiş hesab varsa, bərpa keçidi göndərilməsi istənildi. Gələnlər və spam qovluğunu yoxlayın.'}

@router.post('/reset-password')
def reset_password(data: ResetPassword, request: Request, response: Response, db: Session = Depends(get_db)):
    rate_limit(request, 'reset-password', 10, db=db)
    invalid = 'Bərpa keçidi etibarsızdır və ya vaxtı bitib. Yeni keçid istəyin.'
    record = db.scalar(select(PasswordReset).where(PasswordReset.token_hash == hashlib.sha256(data.token.encode()).hexdigest(), PasswordReset.expires_at > now()))
    if not record:
        raise HTTPException(400, invalid)
    user_id, version = record.user_id, record.token_version
    consumed = db.execute(delete(PasswordReset).where(PasswordReset.id == record.id))
    if consumed.rowcount != 1:
        db.rollback()
        raise HTTPException(400, invalid)
    changed = db.execute(update(User).where(User.id == user_id, User.token_version == version, User.is_email_verified.is_(True), User.email.is_not(None)).values(password_hash=passwords.hash(data.new_password), token_version=User.token_version + 1))
    if changed.rowcount != 1:
        db.rollback()
        raise HTTPException(400, invalid)
    db.execute(delete(PasswordReset).where(PasswordReset.user_id == user_id))
    db.add(AuditEvent(actor_id=user_id, subject=f'user:{user_id}', action='Password reset; previous sessions revoked.'))
    db.commit()
    response.delete_cookie('bugcasp_session', secure=settings.cookie_secure, httponly=True, samesite='strict')
    return {'message': 'Şifrəniz yeniləndi. Yeni şifrə ilə daxil olun.'}
