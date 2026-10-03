from datetime import timedelta
import hashlib
from sqlalchemy import select
from test_platform import platform
from app.models import PasswordReset, now, User
from app.routers import auth_router


def test_password_reset_once_revokes_sessions(platform, monkeypatch):
    client, tokens, sessions, ids, _ = platform
    sent=[]
    monkeypatch.setattr(auth_router, 'send_password_reset', lambda user, token: sent.append((user.email,token)))
    known=client.post('/api/auth/forgot-password',json={'email':'hunter@example.org'})
    unknown=client.post('/api/auth/forgot-password',json={'email':'absent@example.org'})
    assert known.status_code == unknown.status_code == 200
    assert known.json()==unknown.json() and len(sent)==1
    token=sent[0][1]
    with sessions() as db:
        record=db.scalar(select(PasswordReset))
        assert record.token_hash==hashlib.sha256(token.encode()).hexdigest()
        assert record.token_hash!=token
    payload={'token':token,'new_password':'New-Strong-Password-456!'}
    assert client.post('/api/auth/reset-password',json={**payload,'new_password':'short'}).status_code==422
    assert client.post('/api/auth/reset-password',json=payload).status_code==200
    assert client.post('/api/auth/reset-password',json=payload).status_code==400
    assert client.get('/api/auth/me',headers=tokens['hunter']).status_code==401
    assert client.post('/api/auth/login',json={'identifier':'hunter','password':'Strong-Test-Password-123!'}).status_code==401
    assert client.post('/api/auth/login',json={'identifier':'hunter','password':payload['new_password']}).status_code==200


def test_expired_replaced_and_stale_reset_links(platform,monkeypatch):
    client,tokens,sessions,ids,_=platform
    sent=[]
    monkeypatch.setattr(auth_router,'send_password_reset',lambda user,token:sent.append(token))
    for _ in range(2):client.post('/api/auth/forgot-password',json={'email':'hunter@example.org'})
    def reset(token):return client.post('/api/auth/reset-password',json={'token':token,'new_password':'Another-Strong-Password-456!'})
    assert reset(sent[0]).status_code==400
    with sessions() as db:
        db.scalar(select(PasswordReset)).expires_at=now()-timedelta(seconds=1);db.commit()
    assert reset(sent[1]).status_code==400
    client.post('/api/auth/forgot-password',json={'email':'hunter@example.org'})
    with sessions() as db:
        db.get(User,ids['hunter']).token_version+=1;db.commit()
    assert reset(sent[-1]).status_code==400


def test_unverified_account_cannot_reset(platform,monkeypatch):
    client,tokens,sessions,ids,_=platform
    sent=[]
    monkeypatch.setattr(auth_router,'send_password_reset',lambda *args:sent.append(args))
    with sessions() as db:
        db.get(User,ids['hunter']).is_email_verified=False;db.commit()
    assert client.post('/api/auth/forgot-password',json={'email':'hunter@example.org'}).status_code==200
    assert not sent
