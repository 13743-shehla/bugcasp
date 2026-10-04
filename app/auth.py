from datetime import datetime, timedelta, timezone
from collections import defaultdict, deque
from threading import Lock
import time
import hashlib
import hmac
import jwt
from fastapi import Depends, HTTPException, Request
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db, SessionLocal
from .models import User, RateLimit, now
from sqlalchemy import delete

passwords = CryptContext(schemes=['bcrypt'], deprecated='auto')
dummy_hash = passwords.hash('constant-time-invalid-user-password')
attempts = defaultdict(deque)
attempt_lock = Lock()

def rate_limit(request: Request, bucket: str, limit: int = 10, seconds: int = 600, db=None, identifier=''):
    if settings.vercel:
        # Shared storage survives cold starts; no application-side IP header trust.
        identity = (request.client.host if request.client else 'unknown') + ':' + identifier.lower()
        key = hmac.new(settings.jwt_secret.encode(), (bucket + ':' + identity).encode(), hashlib.sha256).hexdigest()
        window = int(time.time()) // seconds * seconds
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        from sqlalchemy.dialects.sqlite import insert as sqlite_insert
        owns_session = db is None
        session = db or SessionLocal()
        try:
            insert = pg_insert if session.bind.dialect.name == 'postgresql' else sqlite_insert
            query = insert(RateLimit).values(key=key, window_start=window, count=1)
            query = query.on_conflict_do_update(index_elements=['key', 'window_start'], set_={'count': RateLimit.count + 1}).returning(RateLimit.count)
            count = session.scalar(query)
            session.execute(delete(RateLimit).where(RateLimit.window_start < int(time.time()) - 86400))
            session.commit()
            if count > limit:
                raise HTTPException(429, 'Çox sayda cəhd edildi. Bir az sonra yenidən yoxlayın.')
        finally:
            if owns_session:
                session.close()
        return
    key = (request.client.host if request.client else 'unknown', bucket)
    current = time.monotonic()
    with attempt_lock:
        for old_key in list(attempts):
            if not attempts[old_key] or current - attempts[old_key][-1] > seconds:
                del attempts[old_key]
        queue = attempts[key]
        while queue and current - queue[0] > seconds:
            queue.popleft()
        if len(queue) >= limit:
            raise HTTPException(429, 'Too many attempts. Please try again later.')
        queue.append(current)

def create_token(user):
    current = datetime.now(timezone.utc)
    return jwt.encode({'sub': str(user.id), 'user_id': user.id, 'role': user.role, 'ver': user.token_version,
                       'iat': current, 'exp': current + timedelta(hours=8),
                       'iss': 'bugcasp', 'aud': 'bugcasp'}, settings.jwt_secret, algorithm='HS256')

def current_user(request: Request, db: Session = Depends(get_db)):
    authorization = request.headers.get('authorization', '')
    token = authorization[7:] if authorization.startswith('Bearer ') else request.cookies.get('bugcasp_session')
    try:
        payload = jwt.decode(token or '', settings.jwt_secret, algorithms=['HS256'], audience='bugcasp', issuer='bugcasp', options={'require': ['exp', 'sub', 'role', 'user_id', 'ver']})
        user = db.get(User, int(payload['sub']))
        if not user or (user.blocked_until and user.blocked_until > now()) or not user.is_email_verified or user.role != payload['role'] or user.id != payload['user_id'] or user.token_version != payload['ver']:
            raise ValueError()
        return user
    except (jwt.PyJWTError, ValueError, TypeError):
        raise HTTPException(401, 'Please sign in with a verified account.')

def roles(*allowed):
    def dependency(user: User = Depends(current_user)):
        if user.role not in allowed:
            raise HTTPException(403, 'This action is not available for your role.')
        return user
    return dependency
