# Şəkillər və admin bölmələri

## İstifadə
- Tədqiqatçı: Profilim → Şəkil seçin → Şəkli yüklə. Şəkil başlıqda və şərəf lövhəsində görünür.
- Şirkət: Şirkət portalı → Şirkət loqosu. Eyni loqo şirkətin bütün proqram kartlarında, proqram məlumatında və yeni proqram formasında görünür.
- JPG, PNG və WebP: maksimum 2 MB və 16 meqapiksel. Server metadata və animasiyanı çıxararaq maksimum 384×384 PNG saxlayır. Şəkillər ictimaidir; hesabat sübutları məxfi qalır.
- Admin panelində İstifadəçilər, Statistika, Mübahisələr, Əməliyyat tarixçəsi, Bildiriş mərkəzi, Sayt elanları və Proqram nəzarəti mövcuddur.
- Blok müddəti 1–365 gündür, vaxt bitdikdə yeni giriş mümkündür. Bloklama/bərpa əvvəlki sessiyaları ləğv edir. Admin hesabları bloklana bilməz.
- Admin proqram məhdudiyyəti şirkətin aktivlik seçimindən ayrıdır. Məhdudiyyət götürüldükdə şirkətin əvvəlki seçimi və proqram təsdiqi qüvvədə qalır.
- Mübahisənin bağlanması hesabat statusunu və mükafatı avtomatik dəyişmir. Qərar hər iki tərəfə görünür, status ayrıca dəyişdirilir.
- Müzakirə yalnız hesabat sahibi, aidiyyəti şirkət və admin üçün açıqdır.
- Bildiriş mərkəzi qərar gözləyən işlərin siyahısıdır; email və ya push bildirişi göndərmir. Yenilə düyməsi cari sayı gətirir.
- Elanı qaralama kimi saxlamaq, redaktə etmək, yayımlamaq və gizlətmək olur. Saytda son 10 aktiv elan göstərilir. Digər istifadəçilər yenilənməni səhifəni yenidən açanda görürlər.
- Statistika tarix filtri UTC ilə qeydin yaradılma tarixinə aiddir. Cari statuslar və həmin hesabatlara aid qeydə alınmış ödənişlər göstərilir; ödəniş tarixinə görə maliyyə hesabatı deyil.
- Profil şəkilləri və loqolar kiçildilmiş şəkildə media_images cədvəlində saxlanır. Ayrı Storage bucket lazım deyil. Ümumi Supabase baza kvotasına daxildir.

## Yayımlama
GitHub Desktop-da bütün dəyişmiş və yeni faylları commit/push edin. Vercel Pillow asılılığını quraşdırır. İlk server sorğusunda mövcud bazaya yeni sütunlar və cədvəllər avtomatik əlavə olunur; məlumat silinmir. PostgreSQL üçün mövcud RLS/anon qadağası yeni cədvəllərə də tətbiq edilir.

Əlavə mühit dəyişəni tələb olunmur. Yerli test hesabları, sınaq bazası və müvəqqəti şəkillər deploy paketinə daxil edilməyib.
