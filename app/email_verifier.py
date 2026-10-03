import html
import logging
import smtplib
import ssl
import httpx
from email.message import EmailMessage
import dns.resolver
from disposable_email_domains import blocklist
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from .config import settings, ROOT

logger = logging.getLogger('bugcasp.email')
brevo_client = httpx.Client(timeout=httpx.Timeout(15, connect=5), follow_redirects=False)

def verify_email_domain(address):
    try:
        result = validate_email(address, check_deliverability=False)
    except EmailNotValidError as exc:
        raise HTTPException(422, str(exc))
    domain = result.ascii_domain.lower()
    labels = domain.split('.')
    if any('.'.join(labels[i:]) in blocklist for i in range(len(labels) - 1)):
        raise HTTPException(422, 'Disposable email addresses are not accepted.')
    try:
        records = dns.resolver.resolve(domain, 'MX', lifetime=4)
        if not any(str(record.exchange).rstrip('.') for record in records):
            raise HTTPException(422, 'This domain does not accept email.')
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        raise HTTPException(422, 'This domain has no mail server.')
    except (dns.exception.DNSException, OSError):
        raise HTTPException(503, 'Email domain verification is temporarily unavailable. Try again.')
    return result.normalized.lower()

def send_email(address, subject, body):
    html_content = f'<html><body style="font:16px Arial;background:#f4f8fc;padding:32px"><div style="max-width:560px;background:white;padding:32px;border-top:4px solid #059ce4"><h1>BugCasp</h1>{body}<p>BugCasp Security Team</p></div></body></html>'
    if settings.email_provider == 'brevo':
        if not settings.brevo_api_key or not settings.email_from_address:
            logger.warning('Brevo sender is not configured; email was not sent.')
            return 'not_configured'
        try:
            response = brevo_client.post('https://api.brevo.com/v3/smtp/email',
                headers={'api-key': settings.brevo_api_key, 'Accept': 'application/json'},
                json={'sender': {'email': settings.email_from_address, 'name': settings.email_from_name},
                      'to': [{'email': address}], 'subject': subject, 'htmlContent': html_content,
                      'textContent': 'BugCasp hesabınızla bağlı məktubdur. HTML versiyasını açın.'})
            if response.status_code == 201:
                return 'sent'
            logger.warning('Brevo did not accept email: HTTP %s', response.status_code)
        except httpx.HTTPError:
            logger.warning('Brevo email service is unavailable.')
        return 'failed'
    if settings.vercel:
        return 'not_configured'
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = settings.smtp_from
    message['To'] = address
    message.set_content('Open the HTML version of this BugCasp message to continue.')
    message.add_alternative(html_content, subtype='html')
    if not settings.smtp_host:
        logger.warning('SMTP is not configured; email was not sent (%s).', subject)
        if settings.dev_email_log:
            with (ROOT / 'email-outbox.log').open('a', encoding='utf-8') as stream:
                stream.write(message.as_string() + '\n\n')
            return 'logged_locally'
        return 'not_configured'
    try:
        client = smtplib.SMTP_SSL if settings.smtp_ssl else smtplib.SMTP
        kwargs = {'context': ssl.create_default_context()} if settings.smtp_ssl else {}
        with client(settings.smtp_host, settings.smtp_port, timeout=10, **kwargs) as server:
            if settings.smtp_starttls and not settings.smtp_ssl:
                server.starttls(context=ssl.create_default_context())
            if settings.smtp_username:
                server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
        return 'sent'
    except (smtplib.SMTPException, OSError):
        logger.exception('Email delivery failed; user remains able to request a resend.')
        return 'failed'

def send_verification(user, token):
    link = settings.app_url.rstrip('/') + '/#verify=' + token
    return send_email(user.email, 'Welcome to BugCasp — verify your email', f'<h2>Welcome, {html.escape(user.username)}</h2><p>Confirm your email address to activate your account. This link expires in 30 minutes and works once.</p><p><a href="{html.escape(link, quote=True)}">Verify my email</a></p><p>If you did not register, ignore this email.</p>')

def send_welcome(user):
    return send_email(user.email, 'Welcome to BugCasp', f'<h2>Your email is verified, {html.escape(user.username)}.</h2><p>Your {html.escape(user.role)} account is ready. Company programs require platform approval before they become public.</p>')

def send_password_reset(user, token):
    link = settings.app_url.rstrip('/') + '/#reset=' + token
    return send_email(user.email, 'BugCasp — şifrənin bərpası', f'<h2>Şifrəni yenilə</h2><p>Salam, {html.escape(user.username)}.</p><p>Bu keçid 30 dəqiqə etibarlıdır və yalnız bir dəfə istifadə olunur.</p><p><a href="{html.escape(link, quote=True)}">Yeni şifrə təyin et</a></p><p>Bu sorğunu siz göndərməmisinizsə, məktubu nəzərə almayın. Şifrəniz dəyişməyib.</p>')
