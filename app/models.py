from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Boolean, CheckConstraint, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (CheckConstraint("role IN ('superadmin','company','hacker')"), CheckConstraint("role = 'superadmin' OR email IS NOT NULL"))
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40), unique=True)
    email: Mapped[str | None] = mapped_column(String(254), unique=True, nullable=True)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))
    reputation_score: Mapped[int] = mapped_column(Integer, default=0)
    token_version: Mapped[int] = mapped_column(Integer, default=0)
    bio: Mapped[str] = mapped_column(Text, default='')
    github: Mapped[str] = mapped_column(String(500), default='')
    tryhackme: Mapped[str] = mapped_column(String(500), default='')
    hackthebox: Mapped[str] = mapped_column(String(500), default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    company: Mapped['Company | None'] = relationship(back_populates='user', uselist=False)
    reports: Mapped[list['Report']] = relationship(back_populates='hacker')

class Company(Base):
    __tablename__ = 'companies'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    company_name: Mapped[str] = mapped_column(String(160))
    # Legacy NOT NULL/UNIQUE column: internal identifier for new companies, never requested or exposed.
    tax_id: Mapped[str] = mapped_column(String(80), unique=True, default=lambda: 'internal:' + uuid4().hex)
    industry: Mapped[str] = mapped_column(String(100))
    website_url: Mapped[str] = mapped_column(String(500))
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    review_state: Mapped[str] = mapped_column(String(20), default='pending')
    review_note: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    user: Mapped[User] = relationship(back_populates='company')
    programs: Mapped[list['Program']] = relationship(back_populates='company')

class Program(Base):
    __tablename__ = 'programs'
    __table_args__ = (CheckConstraint("bounty_type IN ('points','cash')"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), index=True)
    title: Mapped[str] = mapped_column(String(180))
    target_url: Mapped[str] = mapped_column(String(500))
    in_scope: Mapped[str] = mapped_column(Text)
    out_of_scope: Mapped[str] = mapped_column(Text)
    rules: Mapped[str] = mapped_column(Text)
    bounty_type: Mapped[str] = mapped_column(String(10))
    currency: Mapped[str] = mapped_column(String(3), default='AZN', server_default='AZN')
    reward_low: Mapped[int] = mapped_column(Integer, default=50)
    reward_medium: Mapped[int] = mapped_column(Integer, default=150)
    reward_high: Mapped[int] = mapped_column(Integer, default=500)
    reward_critical: Mapped[int] = mapped_column(Integer, default=1500)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    review_state: Mapped[str] = mapped_column(String(20), default='pending')
    review_note: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    company: Mapped[Company] = relationship(back_populates='programs')
    reports: Mapped[list['Report']] = relationship(back_populates='program')

class Report(Base):
    __tablename__ = 'reports'
    __table_args__ = (CheckConstraint("severity IN ('Low','Medium','High','Critical')"), CheckConstraint("status IN ('New','Triaged','Resolved','Duplicate','Informative','Not Applicable')"))
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(ForeignKey('programs.id'), index=True)
    hacker_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    title: Mapped[str] = mapped_column(String(200))
    cwe_category: Mapped[str] = mapped_column(String(100))
    severity: Mapped[str] = mapped_column(String(15))
    cvss_score: Mapped[float] = mapped_column(Float)
    cvss_vector: Mapped[str] = mapped_column(String(180))
    poc_steps: Mapped[str] = mapped_column(Text)
    impact: Mapped[str] = mapped_column(Text)
    http_payload: Mapped[str] = mapped_column(Text, default='')
    attachment_path: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default='New', index=True)
    reputation_awarded: Mapped[int] = mapped_column(Integer, default=0)
    cash_awarded: Mapped[int] = mapped_column(Integer, default=0)
    payout_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    dispute: Mapped[str] = mapped_column(Text, default='')
    mediation: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    program: Mapped[Program] = relationship(back_populates='reports')
    hacker: Mapped[User] = relationship(back_populates='reports')

class Verification(Base):
    __tablename__ = 'verifications'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)

class AuditEvent(Base):
    __tablename__ = 'audit_events'
    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    subject: Mapped[str] = mapped_column(String(100))
    action: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)

class AppSetting(Base):
    __tablename__ = 'app_settings'
    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(Text)

class RateLimit(Base):
    __tablename__ = 'rate_limits'
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    window_start: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer, default=0)

class PasswordReset(Base):
    __tablename__ = 'password_resets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    token_version: Mapped[int] = mapped_column(Integer)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
