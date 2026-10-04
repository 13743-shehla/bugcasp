import sys
from pathlib import Path

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from contextlib import asynccontextmanager
from urllib.parse import urlsplit
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import ROOT, settings
from app.body_limit import BodyLimitMiddleware
from app.database import initialize_database, SessionLocal
from app.models import User
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.routers import auth_router, admin_router, company_router, hacker_router, management_router

@asynccontextmanager
async def lifespan(app):
    try:
        initialize_database()
    except Exception as exc:
        logging.getLogger('bugcasp').error('Initial setup unavailable: %s', type(exc).__name__)
    yield

app = FastAPI(title='BugCasp API', version='2.0.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[settings.app_url.rstrip('/')], allow_credentials=True, allow_methods=['GET', 'POST', 'PUT'], allow_headers=['Content-Type', 'Authorization'])
app.add_middleware(BodyLimitMiddleware, max_bytes=settings.max_upload_bytes + 200000)

@app.middleware('http')
async def security(request: Request, call_next):
    if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
        origin = request.headers.get('origin')
        expected = settings.app_url.rstrip('/')
        if (origin and origin != expected) or request.headers.get('sec-fetch-site') == 'cross-site':
            return JSONResponse({'detail': 'Cross-origin requests are not allowed.'}, status_code=403)
        try:
            if int(request.headers.get('content-length', '0')) > settings.max_upload_bytes + 200000:
                return JSONResponse({'detail': 'Request is too large.'}, status_code=413)
        except ValueError:
            return JSONResponse({'detail': 'Invalid request length.'}, status_code=400)
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    if request.url.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-store'
    if 'Content-Security-Policy' not in response.headers:
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-src 'self' blob:; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'"
        if request.url.path in ('/docs', '/redoc'):
            response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https://fastapi.tiangolo.com; connect-src 'self'; frame-ancestors 'self'"
    return response

for router in (auth_router.router, admin_router.router, company_router.router, hacker_router.router, management_router.router):
    app.include_router(router)

@app.get('/api/health')
def health():
    try:
        initialize_database()
        with SessionLocal() as db:
            owner_exists = db.scalar(select(User.id).where(User.role == 'superadmin').limit(1)) is not None
        if not owner_exists:
            return JSONResponse({'status': 'setup_required', 'message': 'Adminin ilkin sazlamalarını tamamlayın.'}, status_code=503)
        return {'status': 'ok', 'mode': 'live'}
    except Exception:
        return JSONResponse({'status': 'unavailable', 'message': 'Server sazlamalarını və baza bağlantısını yoxlayın.'}, status_code=503)

@app.exception_handler(SQLAlchemyError)
async def database_error(request, exc):
    logging.getLogger('bugcasp').error('Database request failed: %s', type(exc).__name__)
    return JSONResponse({'detail': 'Baza müvəqqəti əlçatan deyil. Bir az sonra yenidən yoxlayın.'}, status_code=503)

@app.get('/')
def index():
    return FileResponse(ROOT / 'static' / 'index.html')

app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000)
