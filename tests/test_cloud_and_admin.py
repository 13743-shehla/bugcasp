import json
from pathlib import Path
from unittest.mock import patch
import httpx
import pytest
from fastapi import HTTPException
from sqlalchemy import select, delete
from app.auth import passwords, create_token, rate_limit
from app.bootstrap import seed_admin
from app.config import settings, Settings
from app.models import User, AppSetting, RateLimit
from app import storage, email_verifier
from test_platform import platform, submit

def test_username_login_and_account_change_revoke_old_token(platform):
    client,tokens,sessions,ids,_=platform
    old='Strong-Test-Password-123!'
    response=client.post('/api/auth/login',json={'identifier':'ADMIN','password':old})
    assert response.status_code==200
    stale=response.json()['access_token']
    bad=client.put('/api/auth/account',headers=tokens['admin'],json={'current_password':'incorrect','username':'renamed_admin'})
    assert bad.status_code==403
    changed=client.put('/api/auth/account',headers=tokens['admin'],json={'current_password':old,'username':'renamed_admin','new_password':'Fresh-New-Password-456!'})
    assert changed.status_code==200,changed.text
    assert changed.json()['user']['username']=='renamed_admin'
    assert client.get('/api/auth/me',headers={'Authorization':'Bearer '+stale}).status_code==401
    assert client.post('/api/auth/login',json={'identifier':'admin','password':old}).status_code==401
    assert client.post('/api/auth/login',json={'identifier':'renamed_admin','password':'Fresh-New-Password-456!'}).status_code==200
    assert client.get('/api/admin/all-reports').status_code==200
    # A process restart must preserve the new identity and password.
    with sessions() as db:
        seed_admin(db)
        user=db.get(User,ids['admin'])
        assert user.username=='renamed_admin'
        assert passwords.verify('Fresh-New-Password-456!',user.password_hash)

def test_admin_bootstrap_without_email_is_once_only(platform,monkeypatch):
    client,tokens,sessions,ids,_=platform
    initial='Test-Initial-Admin-7!'
    monkeypatch.setattr(settings,'bootstrap_admin_username','superadmin')
    monkeypatch.setattr(settings,'bootstrap_admin_password_hash',passwords.hash(initial))
    with sessions() as db:
        db.execute(delete(User).where(User.id==ids['admin']));db.commit()
        seed_admin(db)
        owner=db.scalar(select(User).where(User.username=='superadmin'))
        assert owner.email is None
        assert owner.role=='superadmin'
        assert passwords.verify(initial,owner.password_hash)
        owner.username='newowner'
        owner.password_hash=passwords.hash('Later-Password-8!')
        db.commit()
        seed_admin(db)
        assert db.scalar(select(User).where(User.username=='superadmin')) is None
        assert passwords.verify('Later-Password-8!',owner.password_hash)
        assert db.get(AppSetting,'bootstrap_admin_id').value==str(owner.id)
    login=client.post('/api/auth/login',json={'identifier':'newowner','password':'Later-Password-8!'})
    assert login.status_code==200
    assert login.json()['user']['email'] is None

def test_bootstrap_does_not_promote_registered_hacker(platform,monkeypatch):
    _,_,sessions,ids,_=platform
    monkeypatch.setattr(settings,'bootstrap_admin_username','hunter')
    monkeypatch.setattr(settings,'bootstrap_admin_password_hash',passwords.hash('Unrelated-Password!'))
    with sessions() as db:
        db.execute(delete(User).where(User.id==ids['admin']));db.commit()
        with pytest.raises(RuntimeError): seed_admin(db)
        assert db.get(User,ids['hunter']).role=='hacker'

def test_reserved_admin_handle_and_duplicate_rename(platform):
    client,tokens,*_=platform
    data={'username':'superadmin','email':'new@example.org','password':'New-Strong-Password-123!','role':'hacker'}
    assert client.post('/api/auth/register',json=data).status_code==409
    assert client.put('/api/auth/account',headers=tokens['hunter'],json={'current_password':'Strong-Test-Password-123!','username':'superadmin'}).status_code==409
    assert client.put('/api/auth/account',headers=tokens['admin'],json={'current_password':'Strong-Test-Password-123!','username':'hunter'}).status_code==409

def test_upload_size_matches_vercel(platform):
    assert settings.max_upload_bytes==4*1024*1024
    assert settings.max_upload_bytes+200000 < 4500000
    assert submit(platform,'large.txt',b'a'*(4*1024*1024+1)).status_code==413

def cloud_storage(monkeypatch,handler):
    monkeypatch.setattr(settings,'storage_backend','supabase')
    monkeypatch.setattr(settings,'supabase_url','https://test-project.supabase.co')
    monkeypatch.setattr(settings,'supabase_service_role_key','server-only-test-key')
    monkeypatch.setattr(storage,'client',httpx.Client(transport=httpx.MockTransport(handler)))

def test_private_storage_upload_read_delete(platform,monkeypatch):
    requests=[]
    def handler(request):
        requests.append(request)
        assert request.headers['authorization']=='Bearer server-only-test-key'
        if '/bucket/' in request.url.path:return httpx.Response(200,json={'public':False})
        if request.method=='GET':return httpx.Response(200,content=b'Cloud evidence')
        return httpx.Response(200,json={})
    cloud_storage(monkeypatch,handler)
    response=submit(platform)
    assert response.status_code==201,response.text
    filename=response.json()['attachment_path']
    client,tokens,*_=platform
    assert client.get('/api/company/attachment/'+filename,headers=tokens['owner']).content==b'Cloud evidence'
    count=len(requests)
    assert client.get('/api/company/attachment/'+filename,headers=tokens['otherhunter']).status_code==404
    assert len(requests)==count # No storage request occurs before authorization.
    storage.delete_evidence(filename)
    assert json.loads(requests[-1].content)=={'prefixes':[filename]}
    assert any(r.method=='POST' and r.headers['x-upsert']=='false' for r in requests)
    assert all('/public/' not in r.url.path for r in requests)

def test_public_bucket_is_rejected(platform,monkeypatch):
    calls=[]
    def handler(request):
        calls.append(request.method)
        return httpx.Response(200,json={'public':True})
    cloud_storage(monkeypatch,handler)
    assert submit(platform).status_code==503
    assert calls==['GET']

def test_storage_error_is_not_silently_accepted(platform,monkeypatch):
    cloud_storage(monkeypatch,lambda r:httpx.Response(500,text='internal-provider-secret'))
    response=submit(platform)
    assert response.status_code==503
    assert 'internal-provider-secret' not in response.text

def test_storage_names_cannot_escape_bucket(monkeypatch):
    for name in ('../secret.txt','file.html','bad.pdf','a'*32+'.exe'):
        with pytest.raises(HTTPException):storage.read_evidence(name)

@pytest.mark.parametrize('status,result',[(201,'sent'),(401,'failed'),(429,'failed'),(500,'failed')])
def test_brevo_https_sender(monkeypatch,status,result):
    monkeypatch.setattr(settings,'email_provider','brevo')
    monkeypatch.setattr(settings,'brevo_api_key','test-secret')
    monkeypatch.setattr(settings,'email_from_address','sender@example.org')
    def handler(request):
        assert str(request.url)=='https://api.brevo.com/v3/smtp/email'
        assert request.headers['api-key']=='test-secret'
        body=json.loads(request.content)
        assert body['to']==[{'email':'recipient@example.org'}]
        assert '<h2>Hello</h2>' in body['htmlContent']
        return httpx.Response(status,json={'messageId':'test-only'})
    monkeypatch.setattr(email_verifier,'brevo_client',httpx.Client(transport=httpx.MockTransport(handler)))
    assert email_verifier.send_email('recipient@example.org','Test','<h2>Hello</h2>')==result

def test_brevo_missing_key_does_not_claim_delivery(monkeypatch):
    monkeypatch.setattr(settings,'email_provider','brevo')
    monkeypatch.setattr(settings,'brevo_api_key','')
    assert email_verifier.send_email('a@example.org','Test','x')=='not_configured'

def test_cloud_configuration_fails_closed():
    config=Settings(_env_file=None,vercel=True,jwt_secret='',database_url='sqlite:///x.db')
    assert 'JWT_SECRET' in config.cloud_errors()
    assert 'DATABASE_URL' in config.cloud_errors()
    assert 'APP_URL' in config.cloud_errors()

def test_postgres_pooler_options():
    from app.database import make_engine
    with patch('app.database.create_engine') as create:
        make_engine('postgresql://user:password@pooler.example:6543/postgres')
    args,kwargs=create.call_args
    assert args[0].startswith('postgresql+psycopg://')
    assert kwargs['pool_size']==1 and kwargs['max_overflow']==0
    assert kwargs['connect_args']['prepare_threshold'] is None
    assert kwargs['connect_args']['sslmode']=='require'

def test_serverless_rate_limit_is_shared(platform,monkeypatch):
    from starlette.requests import Request
    client,tokens,sessions,ids,_=platform
    monkeypatch.setattr(settings,'vercel',True)
    request=Request({'type':'http','method':'POST','path':'/api/auth/login','headers':[], 'client':('test-ip',1234)})
    with sessions() as db:
        rate_limit(request,'isolated-test',2,db=db)
    with sessions() as db:
        rate_limit(request,'isolated-test',2,db=db)
    with sessions() as db:
        with pytest.raises(HTTPException) as e:rate_limit(request,'isolated-test',2,db=db)
        assert e.value.status_code==429

def test_package_has_no_hardcoded_owner_password():
    root=Path(__file__).resolve().parent.parent
    for file in list((root/'app').rglob('*.py'))+list((root/'static').rglob('*.js')):
        assert 'BOOTSTRAP_ADMIN_PASSWORD_HASH=$2' not in file.read_text(encoding='utf-8')
