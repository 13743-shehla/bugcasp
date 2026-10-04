from io import BytesIO
from datetime import timedelta
from PIL import Image
from sqlalchemy import select, text, create_engine, inspect
from test_platform import platform, submit
from app.models import User, MediaImage, AuditEvent, now
from app.database import migrate_admin_suite


def picture():
    out=BytesIO();Image.new('RGB',(800,600),'blue').save(out,'PNG');return out.getvalue()

def test_avatar_logo_validation_and_replacement(platform):
    client,tokens,sessions,ids,_=platform
    upload=lambda who,content:client.post('/api/profile-image',headers=tokens[who],files={'image':('photo.png',content,'image/png')})
    assert client.post('/api/profile-image',files={'image':('photo.png',picture())}).status_code==401
    assert upload('admin',picture()).status_code==403
    assert upload('hunter',b'<svg onload="alert(1)"></svg>').status_code==422
    assert upload('hunter',b'x'*(2*1024*1024+1)).status_code==413
    result=upload('hunter',picture());assert result.status_code==200,result.text
    first=result.json()['url']
    response=client.get(first);assert response.headers['content-type']=='image/png'
    with Image.open(BytesIO(response.content)) as photo:assert max(photo.size)<=384
    assert client.get('/api/auth/me',headers=tokens['hunter']).json()['avatar_url']==first
    assert client.get('/api/auth/me',headers=tokens['otherhunter']).json()['avatar_url'] is None
    second=upload('hunter',picture()).json()['url'];assert second!=first
    assert client.get(first).status_code==404
    logo=upload('owner',picture()).json()['url']
    assert client.get('/api/hacker/programs').json()[0]['logo_url']==logo
    assert client.get('/api/company/profile',headers=tokens['owner']).json()['logo_url']==logo
    assert client.post('/api/profile-image/remove',headers=tokens['hunter']).status_code==200
    assert client.get(second).status_code==404
    assert client.get(logo).status_code==200

def test_block_revoke_restore_and_expiry(platform):
    client,tokens,sessions,ids,_=platform
    path=f"/api/admin/users/{ids['hunter']}/block"
    assert client.put(path,headers=tokens['owner'],json={'days':2,'reason':'Test reason'}).status_code==403
    assert client.put(path,headers=tokens['admin'],json={'days':2,'reason':'Test reason'}).status_code==200
    assert client.get('/api/auth/me',headers=tokens['hunter']).status_code==401
    assert client.post('/api/auth/login',json={'identifier':'hunter','password':'Strong-Test-Password-123!'}).status_code==403
    assert client.put(f"/api/admin/users/{ids['admin']}/block",headers=tokens['admin'],json={'days':1,'reason':'Test'}).status_code==409
    assert client.put(path,headers=tokens['admin'],json={'days':0,'reason':'Restored'}).status_code==200
    assert client.get('/api/auth/me',headers=tokens['hunter']).status_code==401
    assert client.post('/api/auth/login',json={'identifier':'hunter','password':'Strong-Test-Password-123!'}).status_code==200
    with sessions() as db:
        db.get(User,ids['hunter']).blocked_until=now()-timedelta(seconds=1);db.commit()
    assert client.post('/api/auth/login',json={'identifier':'hunter','password':'Strong-Test-Password-123!'}).status_code==200

def test_company_block_hides_programs(platform):
    client,tokens,_,ids,_=platform
    assert client.put(f"/api/admin/users/{ids['owner']}/block",headers=tokens['admin'],json={'days':1,'reason':'Investigation'}).status_code==200
    assert client.get('/api/hacker/programs').json()==[]
    assert submit(platform).status_code==404

def test_program_suspension_cannot_be_bypassed(platform):
    client,tokens,*_=platform
    path='/api/admin/programs/1/suspension'
    assert client.put(path,headers=tokens['admin'],json={'suspended':True,'reason':'Scope needs review'}).status_code==200
    assert client.get('/api/hacker/programs').json()==[]
    assert client.put('/api/company/programs/1/active',headers=tokens['owner'],json={'is_active':True}).status_code==409
    own=client.get('/api/company/my-programs',headers=tokens['owner']).json()[0]
    assert own['suspension_reason']=='Scope needs review'
    assert client.put(path,headers=tokens['admin'],json={'suspended':False,'reason':'Scope reviewed'}).status_code==200
    assert len(client.get('/api/hacker/programs').json())==1

def test_dispute_discussion_and_notifications(platform):
    client,tokens,*_=platform
    rid=submit(platform).json()['id'];path=f'/api/reports/{rid}/messages'
    assert client.get(path,headers=tokens['otherhunter']).status_code==404
    assert client.post(path,headers=tokens['otherowner'],json={'body':'Unauthorized'}).status_code==404
    for who in ('hunter','owner','admin'):
        assert client.post(path,headers=tokens[who],json={'body':who+' explanation'}).status_code==200
    assert len(client.get(path,headers=tokens['hunter']).json())==3
    assert client.post(f'/api/hacker/reports/{rid}/dispute',headers=tokens['hunter'],json={'note':'Please review this decision'}).status_code==200
    assert client.get('/api/admin/notifications',headers=tokens['admin']).json()['disputes']==1
    assert client.get('/api/admin/disputes',headers=tokens['admin']).json()['total']==1
    result=client.put(f'/api/admin/disputes/{rid}/resolve',headers=tokens['admin'],json={'reason':'Evidence reviewed; decision explained.'})
    assert result.status_code==200,result.text
    assert client.get('/api/admin/notifications',headers=tokens['admin']).json()['disputes']==0
    report=client.get('/api/hacker/my-reports',headers=tokens['hunter']).json()[0]
    assert report['mediation']=='Evidence reviewed; decision explained.'
    assert not report['dispute_open']
    assert client.get('/api/admin/disputes?state=closed',headers=tokens['admin']).json()['total']==1
    assert client.post(f'/api/hacker/reports/{rid}/dispute',headers=tokens['hunter'],json={'note':'New evidence for consideration'}).status_code==200
    assert client.get('/api/admin/disputes',headers=tokens['admin']).json()['total']==1

def test_announcements_audit_stats_permissions(platform):
    client,tokens,*_=platform
    for path in ('users','overview','notifications','disputes','history','programs','announcements'):
        assert client.get('/api/admin/'+path,headers=tokens['hunter']).status_code==403
    body={'title':'Maintenance','body':'Scheduled maintenance notice','active':False}
    result=client.post('/api/admin/announcements',headers=tokens['admin'],json=body);assert result.status_code==200
    aid=result.json()['id'];assert client.get('/api/announcements').json()==[]
    body['active']=True
    assert client.put(f'/api/admin/announcements/{aid}',headers=tokens['admin'],json=body).status_code==200
    assert client.get('/api/announcements').json()[0]['title']=='Maintenance'
    body['active']=False
    client.put(f'/api/admin/announcements/{aid}',headers=tokens['admin'],json=body)
    assert client.get('/api/announcements').json()==[]
    audit=client.get('/api/admin/history?q=announcement',headers=tokens['admin']).json()
    assert audit['total']==3
    assert all(e['actor']=='admin' for e in audit['items'])
    assert client.get('/api/admin/overview',headers=tokens['admin']).json()['users']==5
    assert client.get('/api/admin/overview?start=2000-01-01&end=2001-01-01',headers=tokens['admin']).json()['users']==0
    assert client.get('/api/admin/overview?start=2026-02-01&end=2026-01-01',headers=tokens['admin']).status_code==422
    rows=client.get('/api/admin/users?q=hunter&role=hacker',headers=tokens['admin']).json()
    assert rows['total']==2
    assert 'password_hash' not in rows['items'][0]

def test_legacy_migration_is_idempotent(tmp_path):
    engine=create_engine('sqlite:///'+str(tmp_path/'old.db'))
    with engine.begin() as conn:
        for table in ('users','companies','programs'):
            conn.execute(text(f'CREATE TABLE {table} (id INTEGER PRIMARY KEY)'))
        conn.execute(text("CREATE TABLE reports (id INTEGER PRIMARY KEY, dispute TEXT, mediation TEXT)"))
        conn.execute(text("INSERT INTO reports VALUES (1,'Please review',''),(2,'Please review','Done')"))
        migrate_admin_suite(conn);migrate_admin_suite(conn)
        assert conn.execute(text('SELECT dispute_open FROM reports ORDER BY id')).scalars().all()==[1,0]
        assert 'avatar_id' in {c['name'] for c in inspect(conn).get_columns('users')}
    engine.dispose()
