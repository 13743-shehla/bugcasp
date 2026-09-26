import logging
from threading import Lock
from fastapi import HTTPException
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import settings

def make_engine(url):
    if not url:
        return None
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql+psycopg://', 1)
    elif url.startswith('postgresql://'):
        url = url.replace('postgresql://', 'postgresql+psycopg://', 1)
    if url.startswith('postgresql+psycopg://'):
        return create_engine(url, pool_size=1, max_overflow=0, pool_timeout=15, pool_pre_ping=True, pool_recycle=300, hide_parameters=True,
                             connect_args={'sslmode': 'require', 'connect_timeout': 10, 'prepare_threshold': None})
    if settings.vercel:
        return None
    return create_engine(url, connect_args={'check_same_thread': False}, hide_parameters=True)

engine = make_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

if engine is not None and engine.dialect.name == 'sqlite':
    @event.listens_for(engine, 'connect')
    def configure_sqlite(connection, record):
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.execute('PRAGMA journal_mode=WAL')
        cursor.execute('PRAGMA busy_timeout=10000')
        cursor.close()

_ready = False
_init_lock = Lock()

def initialize_database():
    global _ready
    if _ready:
        return
    with _init_lock:
        if _ready:
            return
        if settings.cloud_errors() or engine is None:
            raise RuntimeError('Cloud configuration is incomplete. See DEPLOY_VERCEL.md.')
        from . import models
        from .bootstrap import seed_admin
        with engine.begin() as connection:
            postgres = connection.dialect.name == 'postgresql'
            if postgres:
                connection.execute(text('SELECT pg_advisory_xact_lock(724923611)'))
            Base.metadata.create_all(connection)
            if postgres:
                # FastAPI owns authorization; deny direct anonymous Data API access.
                for table in Base.metadata.sorted_tables:
                    name = connection.dialect.identifier_preparer.quote(table.name)
                    connection.execute(text(f'ALTER TABLE {name} ENABLE ROW LEVEL SECURITY'))
                    connection.execute(text(f'REVOKE ALL ON TABLE {name} FROM anon, authenticated'))
        with SessionLocal() as db:
            seed_admin(db)
        _ready = True

def get_db():
    if not _ready:
        try:
            initialize_database()
        except Exception as exc:
            logging.getLogger('bugcasp').error('Database setup unavailable: %s', type(exc).__name__)
            raise HTTPException(503, 'Server sazlanması tamamlanmayıb və ya baza əlçatan deyil.')
    with SessionLocal() as session:
        yield session
