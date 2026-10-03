# 3 oktyabr yeniləməsi

- Şirkət qeydiyyatı və admin şirkət siyahısından VÖEN çıxarıldı. E-poçt və şirkət təsdiqi qalır. Köhnə baza sütunu uyğunluq üçün saxlanır; yeni şirkətlərə istifadəçidən istənilməyən daxili unikal identifikator verilir.
- Yeni proqramlar AZN (manat) ilə yaradılır. Kartlar, proqram detalları, hesabat mükafatları və statistika valyutanı göstərir.
- Əvvəlki proqramların məbləği dəyişmir və USD kimi saxlanır. Fərqli valyutalar bir cəmdə toplanmır.
- İlk açılışda programs.currency sütunu avtomatik əlavə olunur. PostgreSQL-də mövcud başlanğıc kilidi eyni vaxtda təkrar miqrasiyadan qoruyur. Əlavə SQL əmri işlətməyə ehtiyac yoxdur.

Yayımlamaq üçün GitHub Desktop-da dəyişiklikləri Commit to main, sonra Push origin edin. Vercel Ready olanda brauzerdə Ctrl+F5 edin. Yeni şirkət qeydiyyatını və yeni proqramda AZN göstərilməsini canlı saytda yoxlayın.

## Şifrə bərpası

Daxil ol → Şifrəni unutmuşam: təsdiqlənmiş e-poçta Brevo ilə birdəfəlik, 30 dəqiqəlik keçid göndərilir. Yeni şifrə ən azı 12 simvoldur. Köhnə sessiyalar bağlanır. E-poçtsuz admin üçün bərpa mümkün deyil. Yeni password_resets cədvəli ilk server açılışında avtomatik yaradılır. Mövcud Brevo və APP_URL sazlamaları istifadə olunur. Canlı məktub çatdırılması deploy-dan sonra ayrıca yoxlanmalıdır.
