"""Private evidence storage; cloud files are never served by public URLs."""
import logging
import re
from urllib.parse import quote
import httpx
from fastapi import HTTPException
from .config import settings, UPLOADS

client = httpx.Client(timeout=httpx.Timeout(20, connect=5), follow_redirects=False)
log = logging.getLogger('bugcasp.storage')

def check_name(filename):
    if not re.fullmatch(r'[a-f0-9]{32}\.(pdf|txt)', filename):
        raise HTTPException(404, 'Sübut faylı tapılmadı.')

def media_type(filename):
    return 'application/pdf' if filename.endswith('.pdf') else 'text/plain; charset=utf-8'

def storage_request(method, path, **kwargs):
    if not settings.supabase_url.startswith('https://') or not settings.supabase_service_role_key:
        raise HTTPException(503, 'Sübut fayllarının yaddaşı hələ sazlanmayıb.')
    headers = {'apikey': settings.supabase_service_role_key, 'Authorization': 'Bearer ' + settings.supabase_service_role_key}
    headers.update(kwargs.pop('headers', {}))
    try:
        response = client.request(method, settings.supabase_url.rstrip('/') + '/storage/v1/' + path, headers=headers, **kwargs)
    except httpx.HTTPError:
        raise HTTPException(503, 'Fayl yaddaşı müvəqqəti əlçatan deyil. Yenidən yoxlayın.')
    if response.status_code == 404:
        raise HTTPException(404, 'Fayl və ya məxfi yaddaş qovluğu tapılmadı.')
    if response.is_error:
        log.warning('Storage request failed: HTTP %s', response.status_code)
        raise HTTPException(503, 'Fayl yaddaşına müraciət alınmadı.')
    return response

def private_bucket():
    bucket = quote(settings.supabase_storage_bucket, safe='')
    response = storage_request('GET', 'bucket/' + bucket)
    try:
        info = response.json()
    except ValueError:
        raise HTTPException(503, 'Fayl yaddaşının sazlamaları oxunmadı.')
    if info.get('public') is not False:
        raise HTTPException(503, 'Sübut yaddaşı məxfi (Private) olmalıdır.')
    return bucket

def save_evidence(filename, content):
    check_name(filename)
    if settings.storage_backend == 'supabase':
        bucket = private_bucket()
        storage_request('POST', 'object/' + bucket + '/' + filename, content=content,
                        headers={'Content-Type': media_type(filename), 'x-upsert': 'false', 'Cache-Control': 'no-store'})
    elif settings.storage_backend == 'local' and not settings.vercel:
        UPLOADS.mkdir(parents=True, exist_ok=True)
        (UPLOADS / filename).write_bytes(content)
    else:
        raise HTTPException(503, 'Fayl yaddaşı sazlanmayıb.')

def read_evidence(filename):
    check_name(filename)
    if settings.storage_backend == 'supabase':
        bucket = private_bucket()
        content = storage_request('GET', 'object/authenticated/' + bucket + '/' + filename).content
    elif settings.storage_backend == 'local' and not settings.vercel:
        file = UPLOADS / filename
        if not file.is_file():
            raise HTTPException(404, 'Sübut faylı tapılmadı.')
        content = file.read_bytes()
    else:
        raise HTTPException(503, 'Fayl yaddaşı sazlanmayıb.')
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(413, 'Fayl 4 MB həddini keçir.')
    return content

def delete_evidence(filename):
    check_name(filename)
    if settings.storage_backend == 'supabase':
        bucket = quote(settings.supabase_storage_bucket, safe='')
        storage_request('DELETE', 'object/' + bucket, json={'prefixes': [filename]})
    elif settings.storage_backend == 'local' and not settings.vercel:
        (UPLOADS / filename).unlink(missing_ok=True)
