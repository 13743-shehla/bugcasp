from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..auth import roles, current_user
from ..storage import read_evidence, media_type
from ..database import get_db
from ..models import User, Program, Report, AuditEvent
from ..schemas import ProgramCreate, StatusUpdate, ActiveUpdate
from ..services import own_company, program_view, report_view, company_view, accessible_report, update_status

router = APIRouter(prefix='/api/company', tags=['Company'])

@router.get('/profile')
def profile(db: Session = Depends(get_db), user: User = Depends(roles('company'))):
    return company_view(own_company(db, user))

@router.post('/programs', status_code=201)
def create_program(data: ProgramCreate, db: Session = Depends(get_db), user: User = Depends(roles('company'))):
    company = own_company(db, user, approved=True)
    program = Program(company_id=company.id, **data.model_dump(mode='json'))
    db.add(program)
    db.commit()
    db.refresh(program)
    return program_view(program)

@router.get('/my-programs')
def my_programs(db: Session = Depends(get_db), user: User = Depends(roles('company'))):
    company = own_company(db, user)
    return [program_view(p) for p in db.scalars(select(Program).where(Program.company_id == company.id).order_by(Program.id.desc()))]

def owned_program(db, user, program_id):
    program = db.get(Program, program_id)
    if not program or program.company.user_id != user.id:
        raise HTTPException(404, 'Program not found.')
    return program

@router.put('/programs/{program_id}/active')
def set_active(program_id: int, data: ActiveUpdate, db: Session = Depends(get_db), user: User = Depends(roles('company'))):
    program = owned_program(db, user, program_id)
    program.is_active = data.is_active
    db.commit()
    return program_view(program)

@router.get('/programs/{program_id}/reports')
def reports(program_id: int, db: Session = Depends(get_db), user: User = Depends(roles('company'))):
    owned_program(db, user, program_id)
    return [report_view(r) for r in db.scalars(select(Report).where(Report.program_id == program_id).order_by(Report.id.desc()))]

@router.get('/reports')
def all_owned_reports(db: Session = Depends(get_db), user: User = Depends(roles('company'))):
    company = own_company(db, user)
    return [report_view(r) for r in db.scalars(select(Report).join(Program).where(Program.company_id == company.id).order_by(Report.id.desc()))]

@router.put('/reports/{report_id}/status')
def status(report_id: int, data: StatusUpdate, db: Session = Depends(get_db), user: User = Depends(roles('company'))):
    report = accessible_report(db, user, report_id)
    return update_status(db, report, user, data)

@router.post('/reports/{report_id}/mark-paid')
def paid(report_id: int, db: Session = Depends(get_db), user: User = Depends(roles('company'))):
    report = accessible_report(db, user, report_id)
    if report.status != 'Resolved' or not report.cash_awarded:
        raise HTTPException(409, 'Only resolved cash rewards can be marked paid.')
    report.payout_paid = True
    db.add(AuditEvent(actor_id=user.id, subject=f'report:{report.id}', action='Company recorded external payout as paid.'))
    db.commit()
    return report_view(report)

@router.get('/attachment/{filename}')
def attachment(filename: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    report = db.scalar(select(Report).where(Report.attachment_path == filename))
    if not report:
        raise HTTPException(404, 'Attachment not found.')
    accessible_report(db, user, report.id)
    content = read_evidence(filename)
    suffix = '.pdf' if filename.endswith('.pdf') else '.txt'
    return Response(content, media_type=media_type(filename), headers={'Content-Disposition': f'inline; filename="evidence{suffix}"', 'X-Content-Type-Options': 'nosniff', 'Content-Security-Policy': "sandbox; default-src 'none'", 'Cache-Control': 'no-store'})
