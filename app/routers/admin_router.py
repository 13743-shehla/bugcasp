from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..auth import roles
from ..database import get_db
from ..models import User, Company, Program, Report, AuditEvent
from ..schemas import Approval, StatusUpdate
from ..services import company_view, program_view, report_view, update_status

router = APIRouter(prefix='/api/admin', tags=['Admin'], dependencies=[Depends(roles('superadmin'))])

@router.get('/pending-companies')
def companies(db: Session = Depends(get_db)):
    return [company_view(c) for c in db.scalars(select(Company).join(User).where(Company.review_state == 'pending', User.is_email_verified.is_(True)))]

@router.get('/pending-programs')
def programs(db: Session = Depends(get_db)):
    return [program_view(p) for p in db.scalars(select(Program).where(Program.review_state == 'pending'))]

@router.post('/approve-company/{company_id}')
def approve_company(company_id: int, data: Approval, db: Session = Depends(get_db), user: User = Depends(roles('superadmin'))):
    company = db.get(Company, company_id)
    if not company:
        raise HTTPException(404, 'Company not found.')
    if data.approved and not company.user.is_email_verified:
        raise HTTPException(409, 'Company contact must verify their email first.')
    company.is_approved = data.approved
    company.review_state = 'approved' if data.approved else 'rejected'
    company.review_note = data.note
    db.add(AuditEvent(actor_id=user.id, subject=f'company:{company_id}', action=f'{company.review_state}: {data.note}'))
    db.commit()
    return company_view(company)

@router.post('/approve-program/{program_id}')
def approve_program(program_id: int, data: Approval, db: Session = Depends(get_db), user: User = Depends(roles('superadmin'))):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(404, 'Program not found.')
    if data.approved and not program.company.is_approved:
        raise HTTPException(409, 'Approve the company first.')
    program.is_approved = data.approved
    program.review_state = 'approved' if data.approved else 'rejected'
    program.review_note = data.note
    db.add(AuditEvent(actor_id=user.id, subject=f'program:{program_id}', action=f'{program.review_state}: {data.note}'))
    db.commit()
    return program_view(program)

@router.get('/all-reports')
def all_reports(db: Session = Depends(get_db)):
    return [report_view(r) for r in db.scalars(select(Report).order_by(Report.id.desc()))]

@router.put('/reports/{report_id}/status')
def status(report_id: int, data: StatusUpdate, db: Session = Depends(get_db), user: User = Depends(roles('superadmin'))):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(404, 'Report not found.')
    return update_status(db, report, user, data)

@router.get('/analytics')
def analytics(db: Session = Depends(get_db)):
    totals = dict(db.execute(select(Program.currency, func.sum(Report.cash_awarded)).join(Report).where(Report.payout_paid.is_(True)).group_by(Program.currency)).all())
    total_paid = totals.get('AZN', 0)
    return {'total_payouts': total_paid, 'payouts_by_currency': totals, 'currency': 'AZN', 'active_programs': db.scalar(select(func.count(Program.id)).join(Company).where(Program.is_approved.is_(True), Program.is_active.is_(True), Company.is_approved.is_(True))), 'pending_reports': db.scalar(select(func.count(Report.id)).where(Report.status.in_(['New', 'Triaged']))), 'researchers': db.scalar(select(func.count(User.id)).where(User.role == 'hacker', User.is_email_verified.is_(True))), 'top_researchers': [{'username': u.username, 'reputation_score': u.reputation_score} for u in db.scalars(select(User).where(User.role == 'hacker', User.is_email_verified.is_(True)).order_by(User.reputation_score.desc()).limit(5))]}

@router.get('/audit')
def audit(db: Session = Depends(get_db)):
    return [{'actor_id': e.actor_id, 'subject': e.subject, 'action': e.action, 'created_at': e.created_at} for e in db.scalars(select(AuditEvent).order_by(AuditEvent.id.desc()).limit(200))]
