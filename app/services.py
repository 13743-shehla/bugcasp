from sqlalchemy import select, update, func
from fastapi import HTTPException
from .models import User, Company, Program, Report, AuditEvent

def user_view(user):
    return {key: getattr(user, key) for key in ('id', 'username', 'email', 'role', 'is_email_verified', 'reputation_score', 'bio', 'github', 'tryhackme', 'hackthebox')}

def program_view(program):
    result = {key: getattr(program, key) for key in ('id', 'title', 'target_url', 'in_scope', 'out_of_scope', 'rules', 'bounty_type', 'currency', 'reward_low', 'reward_medium', 'reward_high', 'reward_critical', 'is_approved', 'is_active', 'review_state', 'review_note', 'created_at')}
    result.update(company_name=program.company.company_name, industry=program.company.industry)
    return result

def report_view(report):
    result = {key: getattr(report, key) for key in ('id', 'program_id', 'title', 'cwe_category', 'severity', 'cvss_score', 'cvss_vector', 'poc_steps', 'impact', 'http_payload', 'attachment_path', 'status', 'reputation_awarded', 'cash_awarded', 'payout_paid', 'dispute', 'mediation', 'created_at')}
    result.update(program_title=report.program.title, hacker=report.hacker.username, currency=report.program.currency)
    return result

def company_view(company):
    return {key: getattr(company, key) for key in ('id', 'company_name', 'industry', 'website_url', 'is_approved', 'review_state', 'review_note', 'created_at')}

def own_company(db, user, approved=False):
    company = db.scalar(select(Company).where(Company.user_id == user.id))
    if not company:
        raise HTTPException(404, 'Company not found.')
    if approved and not company.is_approved:
        raise HTTPException(403, 'Your company must be approved before creating programs.')
    return company

def visible_program(db, program_id):
    program = db.get(Program, program_id)
    if not program or not program.is_active or not program.is_approved or not program.company.is_approved:
        raise HTTPException(404, 'Active program not found.')
    return program

def accessible_report(db, user, report_id):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(404, 'Report not found.')
    if user.role != 'superadmin' and report.hacker_id != user.id and report.program.company.user_id != user.id:
        raise HTTPException(404, 'Report not found.')
    return report

def update_status(db, report, actor, data):
    transitions = {'New': {'Triaged', 'Duplicate', 'Informative', 'Not Applicable'}, 'Triaged': {'Resolved', 'Duplicate', 'Informative', 'Not Applicable'}, 'Resolved': set(), 'Duplicate': set(), 'Informative': set(), 'Not Applicable': set()}
    old = report.status
    if data.status != old and actor.role != 'superadmin' and data.status not in transitions[old]:
        raise HTTPException(409, 'Invalid status transition. Triage new reports before resolving them.')
    if actor.role == 'superadmin' and data.status != old and not data.note.strip():
        raise HTTPException(422, 'Please record a mediation note for this change.')
    result = db.execute(update(Report).where(Report.id == report.id, Report.status == old).values(status=data.status))
    if result.rowcount != 1:
        db.rollback()
        raise HTTPException(409, 'The report changed. Refresh and try again.')
    if data.status == 'Resolved' and report.reputation_awarded == 0:
        reward = getattr(report.program, 'reward_' + report.severity.lower())
        points = max(1, reward) if report.program.bounty_type == 'points' else {'Low': 50, 'Medium': 150, 'High': 400, 'Critical': 800}[report.severity]
        won = db.execute(update(Report).where(Report.id == report.id, Report.reputation_awarded == 0).values(reputation_awarded=points, cash_awarded=reward if report.program.bounty_type == 'cash' else 0))
        if won.rowcount:
            db.execute(update(User).where(User.id == report.hacker_id).values(reputation_score=User.reputation_score + points))
    if actor.role == 'superadmin' and data.note:
        report.mediation = data.note
    db.add(AuditEvent(actor_id=actor.id, subject=f'report:{report.id}', action=f'{old} -> {data.status}: {data.note}'))
    db.commit()
    db.refresh(report)
    return report_view(report)
