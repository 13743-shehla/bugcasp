"""Create the email-free owner once; never reset changed credentials on restart."""
import re
from sqlalchemy import select, text
from .config import settings
from .models import User, AppSetting

def seed_admin(db):
    from .auth import passwords
    if db.bind.dialect.name == 'postgresql':
        db.execute(text('SELECT pg_advisory_xact_lock(724923612)'))
    if db.get(AppSetting, 'bootstrap_admin_id'):
        db.commit()
        return
    existing = db.scalar(select(User).where(User.role == 'superadmin'))
    if existing:
        db.add(AppSetting(key='bootstrap_admin_id', value=str(existing.id)))
        db.commit()
        return
    if not settings.bootstrap_admin_password_hash:
        db.commit()
        return
    username = settings.bootstrap_admin_username.lower()
    if not re.fullmatch(r'[a-z0-9_-]{3,40}', username):
        raise RuntimeError('BOOTSTRAP_ADMIN_USERNAME is invalid.')
    if not passwords.identify(settings.bootstrap_admin_password_hash):
        raise RuntimeError('BOOTSTRAP_ADMIN_PASSWORD_HASH must be a bcrypt hash.')
    if db.scalar(select(User).where(User.username == username)):
        raise RuntimeError('Bootstrap handle is already registered. No account was promoted.')
    user = User(username=username, email=None, password_hash=settings.bootstrap_admin_password_hash,
                role='superadmin', is_email_verified=True)
    db.add(user)
    db.flush()
    db.add(AppSetting(key='bootstrap_admin_id', value=str(user.id)))
    db.commit()
