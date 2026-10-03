from sqlalchemy import create_engine, text, select
from test_platform import platform, submit
from app.models import Company, Program
from app.database import migrate_currency


def test_two_companies_can_register_without_tax_id(platform):
    client, tokens, sessions, ids, _ = platform
    for n in range(2):
        response = client.post('/api/auth/register', json=dict(username=f'newcompany{n}', email=f'company{n}@example.org', password='Strong-Password-123!', role='company', company_name='New Company', industry='SaaS', website_url='https://example.org'))
        assert response.status_code == 201, response.text
        assert response.json()['is_email_verified'] is False
    assert 'tax_id' not in client.get('/api/company/profile', headers=tokens['owner']).json()
    with sessions() as db:
        rows = db.scalars(select(Company).where(Company.company_name == 'New Company')).all()
        assert len(rows) == 2 and rows[0].tax_id != rows[1].tax_id
        assert all(not c.is_approved for c in rows)


def test_new_program_azn_and_report_currency(platform):
    client, tokens, sessions, ids, _ = platform
    response = client.post('/api/company/programs', headers=tokens['owner'], json=dict(title='Manat program', target_url='https://example.org', in_scope='example.org', out_of_scope='Other hosts', rules='Only your own test accounts', bounty_type='cash', reward_low=50, reward_medium=150, reward_high=500, reward_critical=1500))
    assert response.status_code == 201, response.text
    assert response.json()['currency'] == 'AZN'
    report = submit(platform).json()
    assert report['currency'] == 'AZN'
    for state in ('Triaged', 'Resolved'):
        response = client.put(f"/api/company/reports/{report['id']}/status", headers=tokens['owner'], json={'status':state})
        assert response.status_code == 200
    assert response.json()['cash_awarded'] == 500
    assert response.json()['currency'] == 'AZN'
    client.post(f"/api/company/reports/{report['id']}/mark-paid", headers=tokens['owner'])
    stats = client.get('/api/admin/analytics', headers=tokens['admin']).json()
    assert stats['payouts_by_currency'] == {'AZN':500}
    with sessions() as db:
        db.get(Program, 1).currency = 'USD'
        db.commit()
    stats = client.get('/api/admin/analytics', headers=tokens['admin']).json()
    assert stats['payouts_by_currency'] == {'USD':500}
    assert stats['total_payouts'] == 0


def test_existing_currency_migration_is_idempotent():
    engine = create_engine('sqlite://')
    with engine.begin() as conn:
        conn.execute(text('CREATE TABLE programs (id INTEGER PRIMARY KEY, reward_high INTEGER)'))
        conn.execute(text('INSERT INTO programs VALUES (1, 500)'))
        migrate_currency(conn)
        migrate_currency(conn)
        assert conn.execute(text('SELECT currency, reward_high FROM programs')).one() == ('USD', 500)
