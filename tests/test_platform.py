"""End-to-end authorization and workflow tests; never send real email."""
import hashlib
import os
from datetime import timedelta
from io import BytesIO
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from pypdf import PdfWriter

os.environ.setdefault('JWT_SECRET', 'test-only-secret-that-is-not-used-in-production-123456')
from app.main import app
from app.database import Base, get_db
from app.models import User, Company, Program, Report, Verification, now
from app.auth import passwords, create_token, attempts
from app.routers import auth_router, hacker_router, company_router
from app.config import settings

@pytest.fixture
def platform(tmp_path, monkeypatch):
    engine = create_engine('sqlite:///' + str(tmp_path / 'test.db'), connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    sessions = sessionmaker(engine, expire_on_commit=False)
    def override():
        with sessions() as db:
            yield db
    app.dependency_overrides[get_db] = override
    monkeypatch.setattr('app.main.initialize_database', lambda: None)
    monkeypatch.setattr('app.main.SessionLocal', sessions)
    monkeypatch.setattr('app.storage.UPLOADS', tmp_path)
    monkeypatch.setattr(settings, 'vercel', False)
    monkeypatch.setattr(settings, 'storage_backend', 'local')
    monkeypatch.setattr(auth_router, 'verify_email_domain', lambda value: value.lower())
    monkeypatch.setattr(auth_router, 'send_verification', lambda *args: 'sent')
    monkeypatch.setattr(auth_router, 'send_welcome', lambda *args: 'sent')
    attempts.clear()
    with sessions() as db:
        users = {}
        for name, role in [('admin','superadmin'),('owner','company'),('otherowner','company'),('hunter','hacker'),('otherhunter','hacker')]:
            u = User(username=name,email=name+'@example.org',password_hash=passwords.hash('Strong-Test-Password-123!'),role=role,is_email_verified=True)
            db.add(u)
            db.flush()
            users[name] = u
        c = Company(user_id=users['owner'].id,company_name='Test Company',tax_id='TEST-1',industry='SaaS',website_url='https://example.org',is_approved=True,review_state='approved')
        c2 = Company(user_id=users['otherowner'].id,company_name='Other',tax_id='TEST-2',industry='SaaS',website_url='https://example.org')
        db.add_all([c,c2]);db.flush()
        p = Program(company_id=c.id,title='Test program',target_url='https://example.org',in_scope='example.org',out_of_scope='All other hosts',rules='Use your own test accounts only',bounty_type='cash',reward_low=50,reward_medium=150,reward_high=500,reward_critical=1500,is_approved=True)
        db.add(p);db.commit()
        tokens = {name: {'Authorization': 'Bearer '+create_token(u)} for name,u in users.items()}
        ids = {name:u.id for name,u in users.items()}
    with TestClient(app) as client:
        yield client, tokens, sessions, ids, tmp_path
    app.dependency_overrides.clear()
    engine.dispose()

def payload():
    return {'program_id':'1','title':'Object access vulnerability','cwe_category':'CWE-639','cvss_vector':'CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N','poc_steps':'1. Create two test accounts. 2. Compare their object permissions.','impact':'Cross-account exposure of private test data.'}

def submit(p, filename='evidence.txt', content=b'Test evidence'):
    client,tokens,*_ = p
    return client.post('/api/hacker/reports',headers=tokens['hunter'],data=payload(),files={'attachment':(filename,content)})

def test_registration_requires_mailbox_verification(platform):
    client,tokens,sessions,ids,_ = platform
    data={'username':'newhunter','email':'new@example.org','password':'New-Strong-Password-123!','role':'hacker'}
    result=client.post('/api/auth/register',json=data)
    assert result.status_code==201
    assert result.json()['is_email_verified'] is False
    assert client.post('/api/auth/login',json={'email':data['email'],'password':data['password']}).status_code==403
    with sessions() as db:
        user=db.scalar(select(User).where(User.email==data['email']))
        v=db.scalar(select(Verification).where(Verification.user_id==user.id))
        v.token_hash=hashlib.sha256(b'test-verification-token-1234567890').hexdigest();db.commit()
    verified=client.post('/api/auth/verify-email',json={'token':'test-verification-token-1234567890'})
    assert verified.status_code==200
    assert client.post('/api/auth/verify-email',json={'token':'test-verification-token-1234567890'}).status_code==400
    assert client.post('/api/auth/login',json={'email':data['email'],'password':data['password']}).status_code==200

def test_admin_role_cannot_be_self_registered(platform):
    client,*_=platform
    assert client.post('/api/auth/register',json={'username':'attacker','email':'a@example.org','password':'Very-Strong-Password-123','role':'superadmin'}).status_code==422

def test_role_and_object_authorization(platform):
    client,tokens,*_=platform
    report=submit(platform).json()
    assert client.get('/api/admin/all-reports',headers=tokens['hunter']).status_code==403
    assert client.get('/api/company/programs/1/reports',headers=tokens['otherowner']).status_code==404
    endpoint='/api/company/attachment/'+report['attachment_path']
    assert client.get(endpoint).status_code==401
    assert client.get(endpoint,headers=tokens['otherhunter']).status_code==404
    assert client.get(endpoint,headers=tokens['otherowner']).status_code==404
    for role in ('hunter','owner','admin'):
        response=client.get(endpoint,headers=tokens[role])
        assert response.status_code==200
        assert response.headers['x-content-type-options']=='nosniff'
    assert client.get('/uploads/'+report['attachment_path']).status_code==404

@pytest.mark.parametrize('filename,body',[('evidence.html',b'<h1>x</h1>'),('evidence.exe',b'MZ'),('fake.pdf',b'not pdf'),('bad.txt',b'\x00binary'),('bad.txt',b'\xff\xfe'),('empty.txt',b'')])
def test_rejects_invalid_evidence(platform,filename,body):
    assert submit(platform,filename,body).status_code in (413,422)

def test_pdf_viewer_and_size_limit(platform):
    writer=PdfWriter();writer.add_blank_page(width=300,height=300)
    stream=BytesIO();writer.write(stream)
    response=submit(platform,'proof.pdf',stream.getvalue())
    assert response.status_code==201,response.text
    client,tokens,*_=platform
    file=client.get('/api/company/attachment/'+response.json()['attachment_path'],headers=tokens['owner'])
    assert file.headers['content-type']=='application/pdf'
    assert submit(platform,'huge.txt',b'a'*(settings.max_upload_bytes+1)).status_code==413

def test_cvss_is_calculated_on_server(platform):
    response=submit(platform)
    assert response.status_code==201,response.text
    assert response.json()['cvss_score']==8.1
    assert response.json()['severity']=='High'
    client,tokens,*_=platform
    data=payload();data['cvss_vector']='invalid';data['cvss_score']='10'
    assert client.post('/api/hacker/reports',headers=tokens['hunter'],data=data).status_code==422

def test_resolution_awards_once_and_records_external_payout(platform):
    client,tokens,sessions,ids,_=platform
    rid=submit(platform).json()['id']
    endpoint=f'/api/company/reports/{rid}/status'
    assert client.put(endpoint,headers=tokens['owner'],json={'status':'Resolved'}).status_code==409
    assert client.put(endpoint,headers=tokens['owner'],json={'status':'Triaged'}).status_code==200
    first=client.put(endpoint,headers=tokens['owner'],json={'status':'Resolved'}).json()
    assert first['reputation_awarded']==400
    assert first['cash_awarded']==500
    client.put(endpoint,headers=tokens['owner'],json={'status':'Resolved'})
    with sessions() as db:
        assert db.get(User,ids['hunter']).reputation_score==400
    assert client.get('/api/admin/analytics',headers=tokens['admin']).json()['total_payouts']==0
    assert client.post(f'/api/company/reports/{rid}/mark-paid',headers=tokens['owner']).status_code==200
    assert client.get('/api/admin/analytics',headers=tokens['admin']).json()['total_payouts']==500
    assert client.get('/api/hacker/leaderboard').json()[0]['resolved_bugs']==1

def test_program_approval_and_suspension(platform):
    client,tokens,sessions,ids,_=platform
    data={'title':'New program','target_url':'https://example.org','in_scope':'example.org','out_of_scope':'Anything else','rules':'Use your own test accounts only','bounty_type':'points','reward_low':10,'reward_medium':20,'reward_high':50,'reward_critical':100}
    assert client.post('/api/company/programs',headers=tokens['otherowner'],json=data).status_code==403
    response=client.post('/api/company/programs',headers=tokens['owner'],json=data)
    assert response.status_code==201,response.text
    pid=response.json()['id']
    assert client.get(f'/api/hacker/programs/{pid}').status_code==404
    assert client.post(f'/api/admin/approve-program/{pid}',headers=tokens['admin'],json={'approved':True}).status_code==200
    assert client.get(f'/api/hacker/programs/{pid}').status_code==200
    client.put(f'/api/company/programs/{pid}/active',headers=tokens['owner'],json={'is_active':False})
    assert client.get(f'/api/hacker/programs/{pid}').status_code==404
    with sessions() as db:
        company=db.scalar(select(Company).where(Company.user_id==ids['owner']));cid=company.id
    client.post(f'/api/admin/approve-company/{cid}',headers=tokens['admin'],json={'approved':False})
    assert client.get('/api/hacker/programs').json()==[]

def test_dispute_and_mediation(platform):
    client,tokens,*_=platform
    rid=submit(platform).json()['id']
    assert client.post(f'/api/hacker/reports/{rid}/dispute',headers=tokens['otherhunter'],json={'note':'Please review this report again.'}).status_code==404
    assert client.post(f'/api/hacker/reports/{rid}/dispute',headers=tokens['hunter'],json={'note':'Please review this report again.'}).status_code==200
    endpoint=f'/api/admin/reports/{rid}/status'
    assert client.put(endpoint,headers=tokens['admin'],json={'status':'Resolved'}).status_code==422
    assert client.put(endpoint,headers=tokens['admin'],json={'status':'Resolved','note':'Reviewed evidence; report is valid.'}).status_code==200

def test_cross_origin_and_tampered_tokens(platform):
    client,tokens,*_=platform
    assert client.post('/api/auth/login',headers={'Origin':'https://attacker.example'},json={'email':'owner@example.org','password':'Strong-Test-Password-123!'}).status_code==403
    assert client.get('/api/auth/me',headers={'Authorization':tokens['admin']['Authorization']+'x'}).status_code==401

def test_chunked_body_is_bounded(platform):
    client,*_=platform
    def chunks():
        for _ in range(6):
            yield b'a'*(1024*1024)
    response=client.post('/api/auth/login',content=chunks(),headers={'Content-Type':'application/json'})
    assert response.status_code==413

def test_expired_verification_cannot_activate(platform):
    client,tokens,sessions,ids,_=platform
    token='expired-verification-token-1234567890'
    with sessions() as db:
        user=db.get(User,ids['otherhunter']);user.is_email_verified=False
        db.add(Verification(user_id=user.id,token_hash=hashlib.sha256(token.encode()).hexdigest(),expires_at=now()-timedelta(seconds=1)));db.commit()
    assert client.post('/api/auth/verify-email',json={'token':token}).status_code==400
    assert client.get('/api/auth/me',headers=tokens['otherhunter']).status_code==401

def test_email_checks():
    from app.email_verifier import verify_email_domain
    from fastapi import HTTPException
    import dns.resolver
    with pytest.raises(HTTPException): verify_email_domain('not-an-email')
    with pytest.raises(HTTPException): verify_email_domain('test@mailinator.com')
    with patch('app.email_verifier.dns.resolver.resolve',side_effect=dns.resolver.NXDOMAIN):
        with pytest.raises(HTTPException) as e: verify_email_domain('user@missing-domain-123.net')
        assert e.value.status_code==422
    with patch('app.email_verifier.dns.resolver.resolve',return_value=[type('MX',(),{'exchange':'mail.example.org.'})()]):
        assert verify_email_domain('user@example.org')=='user@example.org'
