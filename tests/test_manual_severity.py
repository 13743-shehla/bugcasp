import pytest
from sqlalchemy import create_engine, text, select
from test_platform import platform, submit
from app.database import migrate_manual_severity
from app.models import Program

@pytest.mark.parametrize('severity,cash,points',[('Low',50,50),('Medium',150,150),('High',500,400),('Critical',1500,800)])
def test_reviewer_controls_reward(platform,severity,cash,points):
    client,tokens,*_=platform
    rid=submit(platform).json()['id'];endpoint=f'/api/company/reports/{rid}/status'
    assert client.put(endpoint,headers=tokens['owner'],json={'status':'Triaged'}).status_code==422
    assert client.put(endpoint,headers=tokens['hunter'],json={'status':'Triaged','severity':severity}).status_code==403
    assert client.put(endpoint,headers=tokens['otherowner'],json={'status':'Triaged','severity':severity}).status_code==404
    assert client.put(endpoint,headers=tokens['owner'],json={'status':'Triaged','severity':'Unknown'}).status_code==422
    assert client.put(endpoint,headers=tokens['owner'],json={'status':'Triaged','severity':severity}).status_code==200
    result=client.put(endpoint,headers=tokens['owner'],json={'status':'Resolved'}).json()
    assert result['cash_awarded']==cash and result['reputation_awarded']==points
    other='Low' if severity!='Low' else 'Critical'
    assert client.put(endpoint,headers=tokens['owner'],json={'status':'Resolved','severity':other}).status_code==409
    assert client.put(endpoint,headers=tokens['owner'],json={'status':'Resolved'}).json()['cash_awarded']==cash


def test_points_program_uses_reviewed_severity(platform):
    client,tokens,sessions,*_=platform
    with sessions() as db:
        db.get(Program,1).bounty_type='points';db.commit()
    rid=submit(platform).json()['id']
    result=client.put(f'/api/admin/reports/{rid}/status',headers=tokens['admin'],json={'status':'Resolved','severity':'Critical','note':'Evidence reviewed'}).json()
    assert result['cash_awarded']==0 and result['reputation_awarded']==1500


def test_migrate_keeps_existing_rewards_and_marks_new_unreviewed():
    engine=create_engine('sqlite://')
    with engine.begin() as c:
        c.execute(text('CREATE TABLE reports (id INTEGER PRIMARY KEY,status TEXT,reputation_awarded INTEGER)'))
        c.execute(text("INSERT INTO reports VALUES (1,'New',0),(2,'Triaged',0),(3,'Resolved',400)"))
        migrate_manual_severity(c);migrate_manual_severity(c)
        assert c.execute(text('SELECT severity_reviewed FROM reports ORDER BY id')).scalars().all()==[0,1,1]
