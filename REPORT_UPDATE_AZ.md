# Sadələşdirilmiş hesabat

Tədqiqatçı proqramı seçdikdən sonra yalnız başlıq, CWE/OWASP kateqoriyası və məcburi PDF/TXT sübut faylı təqdim edir. Addımlar və təsir sübut faylında yazılır.

Şirkət və admin Low/Medium/High/Critical seçir. Triaged və Resolved üçün dərəcə tələb olunur. Resolved olduqda uyğun mükafat və xal bir dəfə hesablanır; bundan sonra dərəcə dəyişmir.

CVSS hesablanmır və interfeysdə göstərilmir. Köhnə hesabatların məlumatlarını itirməmək üçün əvvəlki baza sütunları saxlanılıb. Mövcud New hesabatlar yenidən qiymətləndirmə gözləyir; əvvəl yoxlanmış və mükafatlandırılmış hesabatlar qorunur. Yeni severity_reviewed sütunu ilk açılışda avtomatik əlavə olunur.

GitHub Desktop: Commit to main → Push origin. Vercel Ready olduqdan sonra Ctrl+F5. Yeni hesabatı sübut faylı ilə göndərin; şirkətdən dərəcə seçib Triaged, sonra Resolved edin.
