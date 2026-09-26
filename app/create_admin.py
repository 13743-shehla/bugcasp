"""Interactive, local-only creation of the trusted platform owner."""
from getpass import getpass
from sqlalchemy import select
from app.database import initialize_database, SessionLocal
from app.models import User, AppSetting
from app.auth import passwords
import re

def main():
    initialize_database()
    handle = input('Admin handle: ').strip().lower()
    if not re.fullmatch(r'[a-z0-9_-]{3,40}', handle):
        raise SystemExit('Handle must contain 1–40 characters.')
    password = getpass('Password (12+ characters): ')
    if len(password) < 12 or len(password.encode()) > 72 or password != getpass('Repeat password: '):
        raise SystemExit('Passwords must match and contain 12+ characters, at most 72 UTF-8 bytes.')
    with SessionLocal() as db:
        if db.scalar(select(User).where(User.role == 'superadmin')):
            raise SystemExit('An admin already exists. Change its credentials through account settings.')
        if db.scalar(select(User).where(User.username == handle)):
            raise SystemExit('This handle is already registered.')
        user = User(email=None, username=handle, password_hash=passwords.hash(password), role='superadmin', is_email_verified=True)
        db.add(user)
        db.flush()
        db.add(AppSetting(key='bootstrap_admin_id', value=str(user.id)))
        db.commit()
    print('Trusted administrator created. Sign in at http://127.0.0.1:8000.')

if __name__ == '__main__':
    main()
