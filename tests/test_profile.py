from test_platform import platform

def test_profile_updates_only_own_public_fields(platform):
    client,tokens,*_=platform
    body={'bio':'Security researcher','github':'https://github.com/example','tryhackme':'','hackthebox':''}
    assert client.put('/api/auth/profile',json=body).status_code==401
    assert client.put('/api/auth/profile',headers=tokens['owner'],json=body).status_code==403
    result=client.put('/api/auth/profile',headers=tokens['hunter'],json=body)
    assert result.status_code==200,result.text
    assert client.get('/api/auth/me',headers=tokens['hunter']).json()['bio']==body['bio']
    assert client.get('/api/auth/me',headers=tokens['otherhunter']).json()['bio']==''
    assert client.put('/api/auth/profile',headers=tokens['hunter'],json={**body,'role':'superadmin'}).status_code==422
    assert client.put('/api/auth/profile',headers=tokens['hunter'],json={**body,'github':'javascript:alert(1)'}).status_code==422
    assert client.put('/api/auth/profile',headers=tokens['hunter'],json={**body,'bio':'x'*2001}).status_code==422
    assert client.put('/api/auth/profile',headers=tokens['hunter'],json={'bio':'','github':'','tryhackme':'','hackthebox':''}).json()['user']['github']==''

def test_username_availability_and_authoritative_save(platform):
    client,tokens,*_=platform
    path='/api/auth/username-availability'
    assert client.get(path,params={'username':'newname'}).status_code==401
    for name,available in [('HUNTER',True),('OtherHunter',False),('superadmin',False),('new_handle',True)]:
        result=client.get(path,headers=tokens['hunter'],params={'username':name})
        assert result.status_code==200,result.text
        assert result.json()['available'] is available
    assert client.get(path,headers=tokens['hunter'],params={'username':'bad name'}).status_code==422
    body={'current_password':'Strong-Test-Password-123!','username':'OTHERHUNTER'}
    assert client.put('/api/auth/account',headers=tokens['hunter'],json=body).status_code==409
    body['username']='new_handle'
    assert client.put('/api/auth/account',headers=tokens['hunter'],json=body).status_code==200
    assert client.get('/api/auth/me').json()['username']=='new_handle'
