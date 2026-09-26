from pathlib import Path
import os
import secrets
from urllib.parse import urlsplit
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ROOT / '.env'), extra='ignore')
    app_url: str = 'http://127.0.0.1:8000'
    jwt_secret: str = ''
    vercel: bool = False
    database_url: str = ''
    storage_backend: str = 'local'
    supabase_url: str = ''
    supabase_service_role_key: str = ''
    supabase_storage_bucket: str = 'bugcasp-evidence'
    email_provider: str = 'smtp'
    brevo_api_key: str = ''
    email_from_address: str = ''
    email_from_name: str = 'BugCasp'
    bootstrap_admin_username: str = 'superadmin'
    bootstrap_admin_password_hash: str = ''
    upload_dir: str = str(ROOT / 'uploads')
    smtp_host: str = ''
    smtp_port: int = 587
    smtp_username: str = ''
    smtp_password: str = ''
    smtp_from: str = 'BugCasp <no-reply@example.com>'
    smtp_starttls: bool = True
    smtp_ssl: bool = False
    dev_email_log: bool = False
    cookie_secure: bool = False
    max_upload_bytes: int = Field(default=4 * 1024 * 1024, ge=1, le=4 * 1024 * 1024)

    def cloud_errors(self):
        if not self.vercel:
            return []
        errors = []
        if len(self.jwt_secret) < 32:
            errors.append('JWT_SECRET')
        if not self.database_url.startswith(('postgresql://', 'postgres://', 'postgresql+psycopg://')):
            errors.append('DATABASE_URL')
        origin = urlsplit(self.app_url)
        if origin.scheme != 'https' or not origin.netloc or origin.path not in ('', '/') or origin.query or origin.fragment:
            errors.append('APP_URL')
        if self.storage_backend != 'supabase' or not self.supabase_url.startswith('https://') or not self.supabase_service_role_key:
            errors.append('Supabase storage settings')
        if self.email_provider != 'brevo' or not self.brevo_api_key or not self.email_from_address:
            errors.append('Brevo email settings')
        if self.dev_email_log:
            errors.append('DEV_EMAIL_LOG must be false')
        return errors

settings = Settings()
if settings.vercel:
    settings.cookie_secure = True
elif not settings.database_url:
    settings.database_url = f'sqlite:///{ROOT / "bugcasp.db"}'
if not settings.jwt_secret and not settings.vercel:
    key_path = ROOT / '.jwt-secret'
    try:
        fd = os.open(key_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as stream:
            stream.write(secrets.token_urlsafe(48))
    except FileExistsError:
        pass
    settings.jwt_secret = key_path.read_text().strip()
if len(settings.jwt_secret) < 32 and not settings.vercel:
    raise RuntimeError('JWT_SECRET must contain at least 32 characters.')
if settings.dev_email_log and (settings.vercel or not settings.app_url.startswith(('http://127.0.0.1:', 'http://localhost:'))):
    raise RuntimeError('DEV_EMAIL_LOG is allowed only with a loopback APP_URL.')
UPLOADS = Path(settings.upload_dir).resolve()
