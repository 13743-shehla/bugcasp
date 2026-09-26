# Yoxlama nəticələri — 26 sentyabr 2026

- 36 avtomatik test uğurla keçdi.
- İlkin superadmin hesabı lokal sınaq bazasında yaradıldı; verilmiş şifrə ilə e-poçtsuz giriş və admin API-si yoxlandı.
- Ad/şifrə dəyişməsi, köhnə sessiyaların ləğvi, rollar, fayl icazələri, 4 MiB limiti, e-poçt təsdiqi və paylaşılmış sorğu limiti yoxlandı.
- Supabase Storage və Brevo testləri imitasiya edilmiş API cavablarından istifadə edir.
- Real PostgreSQL/Supabase/Brevo bağlantıları və Vercel deployment hələ yoxlanmayıb; hesab sazlamaları lazımdır.
- Test alətindən httpx ilə bağlı bir köhnəlmə bildirişi var; testlərə mane olmadı.
