# BugCasp — Vercel sınaq paketi

Azərbaycan dilində bug bounty platforması. FastAPI tətbiqi, PostgreSQL bazası, şəxsi sübut faylları və e-poçt təsdiqi ilə işləyir. Loqonuz paketə daxildir.

## Başlamaq

Yerləşdirmə addımları: [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md).

- Vercel: tətbiq; Supabase: PostgreSQL və şəxsi fayl anbarı; Brevo: təsdiq məktubları.
- Admin: `superadmin`, e-poçtsuz giriş. İlkin şifrənin heşi ayrıca məxfi sazlama faylındadır.
- Girişdən sonra **Sazlamalar** vasitəsilə istifadəçi adını və şifrəni dəyişin. Dəyişiklik əvvəlki sessiyaları etibarsız edir. Yenidən deploy şifrəni ilkin vəziyyətə qaytarmır.
- İştirakçı və şirkət qeydiyyatı üçün e-poçt təsdiqi qalır. Şirkət proqramları admin təsdiqindən keçir.
- Sübut faylları: PDF/TXT, maksimum 4 MiB. Fayllar yalnız icazəli hesablara göstərilir.
- Ödənişlər xaricdə həyata keçirilir; platforma ödəniş qeydini saxlayır, pul köçürmür.

Bu paket yeni, boş Supabase layihəsi üçündür. Əvvəlki SQLite bazasının məlumatları avtomatik köçürülmür. Bulud xidmətlərinin açarları daxil edilməyib və sayt hələ internetdə yayımlanmayıb.

## Lokal işə salma

Python 3.12 ilə virtual mühit yaradın, `pip install -r requirements.txt` işlədin. `.env` faylında `APP_URL=http://127.0.0.1:8000`, ən az 32 simvolluq `JWT_SECRET`, `BOOTSTRAP_ADMIN_USERNAME` və ayrıca verilmiş `BOOTSTRAP_ADMIN_PASSWORD_HASH` təyin edin. Lokal sınaqda `STORAGE_BACKEND=local`, `COOKIE_SECURE=false`, `VERCEL=false` istifadə edin. `DATABASE_URL` boş qalarsa lokal SQLite yaradılır.

`python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` ilə açın. Məktub göndərmək üçün Brevo sazlamaları lazımdır. Yalnız lokal sınaq üçün `DEV_EMAIL_LOG=true` məktubları lokal fayla yazır; bunu internetdə aktivləşdirməyin.

Testlər: `python -m pytest -q`. Bulud API testləri saxta cavablarla işləyir; real xidmət bağlantıları deploy zamanı ayrıca yoxlanmalıdır.
