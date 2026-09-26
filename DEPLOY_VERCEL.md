# BugCasp-ı Vercel-də yerləşdirmək

Paket 10 nəfərlik şəxsi sınaq üçün Vercel Hobby, Supabase Free və Brevo Free ilə işləməyə uyğunlaşdırılıb. Ödənişli plan seçməyin. Xidmətlərin pulsuz limitləri və qaydaları dəyişə bilər; qeydiyyat zamanı göstərilən planı yoxlayın. Heç bir ödənişli abunə bu paket tərəfindən açılmır.

## 1. Faylları hazırlayın

`bugcasp_vercel.zip` arxivini açın. İçərisindəki `app`, `static`, `pyproject.toml`, `vercel.json` və digər faylları yeni GitHub deposunun kökünə yükləyin. Şəxsi depo istifadə edə bilərsiniz.

**Ayrıca verilmiş `bugcasp_vercel.private.env` faylını GitHub-a yükləməyin.** Orada giriş açarı və ilkin admin şifrəsinin heşi var. Bu faylı yalnız Vercel-in Environment Variables sazlamalarına daxil etmək üçün saxlayın. `.env.example` isə boş nümunədir və depoda qala bilər.

## 2. Supabase Free

1. Yeni, boş Supabase layihəsi yaradın və bazanın şifrəsini saxlayın.
2. **Connect → Transaction pooler** bağlantısını götürün. Port `6543` olmalıdır. Ünvan və istifadəçi adını paneldən olduğu kimi köçürün; server adını təxmin etməyin.
3. Bağlantıdakı şifrə yerini baza şifrəsi ilə əvəz edin. Şifrədə `@`, `:`, `/`, `#`, `%` varsa URL üçün kodlaşdırılmalıdır. Alınmış bağlantını `DATABASE_URL` kimi istifadə edin. Tətbiq SSL və pooler uyğunluğunu özü sazlayır.
4. **Storage** bölməsində `bugcasp-evidence` adlı **Private** bucket yaradın. Public seçimini açmayın. Fayl ölçüsü limitini 4 MiB, MIME növlərini `application/pdf,text/plain` təyin edə bilərsiniz.
5. Layihənin URL-ni `SUPABASE_URL`, server üçün **legacy service_role** açarını `SUPABASE_SERVICE_ROLE_KEY` kimi götürün. `anon` və ya publishable açar uyğun deyil. Service role açarını saytda, brauzer kodunda və GitHub-da paylaşmayın.

Tətbiq cədvəlləri ilk açılışda yaradır, anonim Data API girişini bağlayır. Storage üçün açıq oxuma siyasəti yaratmaq lazım deyil. Bu təlimat mövcud məlumatların miqrasiyasını etmir.

## 3. Brevo Free

Brevo-da göndərən e-poçt ünvanını təsdiqləyin və API açarı yaradın. `BREVO_API_KEY` və `EMAIL_FROM_ADDRESS` dəyərlərini doldurun. Hesabın məktub göndərməsinə icazə verildiyinə əmin olun.

Bu ünvan istifadəçilərə qeydiyyat məktubları göndərmək üçündür; **admin hesabına e-poçt bağlanmır**. Brevo Free üçün sənədləşdirilmiş limit gündə 300 məktubdur. SMTP əvəzinə HTTPS API istifadə olunur.

## 4. Vercel

1. GitHub deposunu **Add New → Project** ilə import edin. Hobby planını seçin.
2. Layihənin kökü `pyproject.toml` və `vercel.json` olan qovluq olmalıdır. Framework **FastAPI** olmalıdır; ayrıca statik Output Directory yazmayın.
3. **Environment Variables** bölməsinə ayrıca məxfi fayldakı dəyərləri daxil edin. Bütün `YOUR-PROJECT`, `PROJECT_REF`, `PASSWORD`, `POOLER_HOST` nümunələrini real dəyərlərlə əvəz edin; boş açarları doldurun.
4. `APP_URL` saytın tam istehsal ünvanı olmalıdır, məsələn `https://bugcasp-test.vercel.app`. Sonuna səhifə yolu əlavə etməyin. Ünvan deploy zamanı fərqli alınarsa `APP_URL`-ni düzəldib yenidən deploy edin.
5. Dəyərləri **Production** mühitinə tətbiq edin. Preview üçün ayrıca baza və uyğun `APP_URL` sazlamadan sınaq ünvanından istifadə etməyin.
6. Deploy edin. Sazlamalar dəyişəndə yeni deployment yaradılmalıdır.

Məcburi dəyərlər:

| Ad | Dəyər |
|---|---|
| APP_URL | Saytın HTTPS ünvanı |
| JWT_SECRET | Məxfi fayldakı hazır təsadüfi dəyər |
| DATABASE_URL | Supabase Transaction pooler bağlantısı |
| STORAGE_BACKEND | supabase |
| SUPABASE_URL | Supabase layihə URL-si |
| SUPABASE_SERVICE_ROLE_KEY | Server service_role açarı |
| SUPABASE_STORAGE_BUCKET | bugcasp-evidence |
| EMAIL_PROVIDER | brevo |
| BREVO_API_KEY | Brevo API açarı |
| EMAIL_FROM_ADDRESS | Brevo-da təsdiqlənmiş göndərən |
| EMAIL_FROM_NAME | BugCasp |
| COOKIE_SECURE | true |
| DEV_EMAIL_LOG | false |
| BOOTSTRAP_ADMIN_USERNAME | superadmin |
| BOOTSTRAP_ADMIN_PASSWORD_HASH | Məxfi fayldakı tam heş |

Vercel `VERCEL=1` dəyişənini özü verir. Panelə heş daxil edəndə `$` simvollarını saxlayın, dəyərin ətrafına dırnaq əlavə etməyin.

## 5. Admin və son yoxlama

İlk uğurlu baza bağlantısında `superadmin` bir dəfə yaradılır. **Daxil ol** pəncərəsinə bu adı və söhbətdə verdiyiniz şifrəni daxil edin. Şifrə yazdığınız formada, əks-sləş işarəsi daxil olmaqla saxlanılıb. E-poçt istənmir.

**Sazlamalar** bölməsindən adı və şifrəni sonradan dəyişə bilərsiniz. Təkrar deploy hesabı sıfırlamır. E-poçt bağlanmadığı üçün e-poçtla şifrə bərpası yoxdur; yeni şifrəni saxlayın.

Yoxlayın:

- `/api/health` ünvanında `status: ok` görünür.
- Admin girişi və admin paneli açılır.
- Sınaq istifadəçisinə təsdiq məktubu çatır və link işləyir.
- Şirkət proqramı admin təsdiqindən keçir.
- Kiçik PDF/TXT hesabat əlavə olunur və yalnız icazəli hesablar faylı aça bilir.

`503` olarsa Vercel sazlamalarını, Supabase bağlantısını və layihənin pauzada olub-olmadığını yoxlayın. `403` giriş/saxlama zamanı görünərsə brauzerdəki sayt ünvanı ilə `APP_URL` uyğunluğunu yoxlayın. Məktub gəlmirsə Brevo göndərən təsdiqini və gündəlik limiti yoxlayın.

## Pulsuz planın sərhədləri

Vercel Hobby şəxsi, qeyri-kommersiya istifadə üçündür. Supabase Free layihələri fəaliyyətsizlikdən sonra pauzaya düşə bilər; baza və fayllar plan limitlərinə tabedir. Fayl yükləmələri Vercel sorğu/cavab limitinə uyğun olaraq 4 MiB ilə məhdudlaşdırılıb. Daimi fasiləsiz xidmətə zəmanət verilmir.

Rəsmi sənədlər: [Vercel FastAPI](https://vercel.com/docs/frameworks/backend/fastapi), [Vercel limitləri](https://vercel.com/docs/functions/limitations), [Supabase bağlantısı](https://supabase.com/docs/guides/database/connecting-to-postgres), [Supabase Storage](https://supabase.com/docs/guides/storage/security/access-control), [Brevo API](https://developers.brevo.com/reference/send-transac-email).
