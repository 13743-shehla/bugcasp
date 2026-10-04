'use strict';
(() => {
const messages = {
  "Proqramlar": {
    "az": "Proqramlar",
    "en": "Programs",
    "ru": "Программы"
  },
  "Hesabatlarım": {
    "az": "Hesabatlarım",
    "en": "My reports",
    "ru": "Мои отчёты"
  },
  "Şərəf lövhəsi": {
    "az": "Şərəf lövhəsi",
    "en": "Leaderboard",
    "ru": "Рейтинг"
  },
  "Şirkət portalı": {
    "az": "Şirkət portalı",
    "en": "Company portal",
    "ru": "Кабинет компании"
  },
  "Admin paneli": {
    "az": "Admin paneli",
    "en": "Admin panel",
    "ru": "Панель администратора"
  },
  "Hesab sazlamaları": {
    "az": "Hesab sazlamaları",
    "en": "Account settings",
    "ru": "Настройки аккаунта"
  },
  "Tədqiqatçı": {
    "az": "Tədqiqatçı",
    "en": "Researcher",
    "ru": "Исследователь"
  },
  "Şirkət sahibi": {
    "az": "Şirkət sahibi",
    "en": "Company owner",
    "ru": "Владелец компании"
  },
  "Platforma admini": {
    "az": "Platforma admini",
    "en": "Platform administrator",
    "ru": "Администратор платформы"
  },
  "Daxil ol": {
    "az": "Daxil ol",
    "en": "Sign in",
    "ru": "Войти"
  },
  "Qeydiyyat": {
    "az": "Qeydiyyat",
    "en": "Register",
    "ru": "Регистрация"
  },
  "Sazlamalar": {
    "az": "Sazlamalar",
    "en": "Settings",
    "ru": "Настройки"
  },
  "Çıxış": {
    "az": "Çıxış",
    "en": "Sign out",
    "ru": "Выйти"
  },
  "İŞ SAHƏSİ": {
    "az": "İŞ SAHƏSİ",
    "en": "WORKSPACE",
    "ru": "РАБОЧЕЕ ПРОСТРАНСТВО"
  },
  "İş sahəsi": {
    "az": "İş sahəsi",
    "en": "Workspace",
    "ru": "Рабочее пространство"
  },
  "Əsas naviqasiya": {
    "az": "Əsas naviqasiya",
    "en": "Main navigation",
    "ru": "Основная навигация"
  },
  "SECURITY COMMUNITY": {
    "az": "SECURITY COMMUNITY",
    "en": "SECURITY COMMUNITY",
    "ru": "СООБЩЕСТВО БЕЗОПАСНОСТИ"
  },
  "BUGCASP PLATFORMASI": {
    "az": "BUGCASP PLATFORMASI",
    "en": "BUGCASP PLATFORM",
    "ru": "ПЛАТФОРМА BUGCASP"
  },
  "Birlikdə daha təhlükəsiz.": {
    "az": "Birlikdə daha təhlükəsiz.",
    "en": "Safer together.",
    "ru": "Вместе безопаснее."
  },
  "Məsuliyyətli araşdırma.": {
    "az": "Məsuliyyətli araşdırma.",
    "en": "Responsible research.",
    "ru": "Ответственное исследование."
  },
  "Real təsir.": {
    "az": "Real təsir.",
    "en": "Real impact.",
    "ru": "Реальный результат."
  },
  "BugCasp — Təhlükəsizlik platforması": {
    "az": "BugCasp — Təhlükəsizlik platforması",
    "en": "BugCasp — Security platform",
    "ru": "BugCasp — Платформа безопасности"
  },
  "BugCasp yüklənir…": {
    "az": "BugCasp yüklənir…",
    "en": "Loading BugCasp…",
    "ru": "Загрузка BugCasp…"
  },
  "Yüklənir…": {
    "az": "Yüklənir…",
    "en": "Loading…",
    "ru": "Загрузка…"
  },
  "Yalnız icazə verilən hədəfləri araşdırın.": {
    "az": "Yalnız icazə verilən hədəfləri araşdırın.",
    "en": "Only test authorized targets.",
    "ru": "Проверяйте только разрешённые цели."
  },
  "Dil seçimi": {
    "az": "Dil seçimi",
    "en": "Language",
    "ru": "Язык"
  },
  "☾ Qaranlıq rejim": {
    "az": "☾ Qaranlıq rejim",
    "en": "☾ Dark mode",
    "ru": "☾ Тёмная тема"
  },
  "☀ Açıq rejim": {
    "az": "☀ Açıq rejim",
    "en": "☀ Light mode",
    "ru": "☀ Светлая тема"
  },
  "Qaranlıq rejimə keç": {
    "az": "Qaranlıq rejimə keç",
    "en": "Switch to dark mode",
    "ru": "Включить тёмную тему"
  },
  "Açıq rejimə keç": {
    "az": "Açıq rejimə keç",
    "en": "Switch to light mode",
    "ru": "Включить светлую тему"
  },
  "Qaranlıq rejim": {
    "az": "Qaranlıq rejim",
    "en": "Dark mode",
    "ru": "Тёмная тема"
  },
  "Bağla": {
    "az": "Bağla",
    "en": "Close",
    "ru": "Закрыть"
  },
  "Ləğv et": {
    "az": "Ləğv et",
    "en": "Cancel",
    "ru": "Отмена"
  },
  "Geri": {
    "az": "Geri",
    "en": "Back",
    "ru": "Назад"
  },
  "Göndər": {
    "az": "Göndər",
    "en": "Send",
    "ru": "Отправить"
  },
  "Qeyd": {
    "az": "Qeyd",
    "en": "Note",
    "ru": "Примечание"
  },
  "Bax": {
    "az": "Bax",
    "en": "View",
    "ru": "Просмотр"
  },
  "ARAŞDIR · HESABAT VER · TƏSİR YARAT": {
    "az": "ARAŞDIR · HESABAT VER · TƏSİR YARAT",
    "en": "RESEARCH · REPORT · MAKE AN IMPACT",
    "ru": "ИССЛЕДУЙ · СООБЩАЙ · ПОМОГАЙ"
  },
  "Növbəti hədəfinizi tapın.": {
    "az": "Növbəti hədəfinizi tapın.",
    "en": "Find your next target.",
    "ru": "Найдите следующую цель."
  },
  "Təsdiqlənmiş proqramları araşdırın və təhlükəsizliyə töhfə verin.": {
    "az": "Təsdiqlənmiş proqramları araşdırın və təhlükəsizliyə töhfə verin.",
    "en": "Explore approved programs and help improve security.",
    "ru": "Изучайте одобренные программы и повышайте безопасность."
  },
  "Proqram yarat": {
    "az": "Proqram yarat",
    "en": "Create program",
    "ru": "Создать программу"
  },
  "Hesabat göndər": {
    "az": "Hesabat göndər",
    "en": "Submit report",
    "ru": "Отправить отчёт"
  },
  "İcmaya qoşul": {
    "az": "İcmaya qoşul",
    "en": "Join the community",
    "ru": "Присоединиться"
  },
  "Bacarıqlarınızla fərq yaradın.": {
    "az": "Bacarıqlarınızla fərq yaradın.",
    "en": "Make a difference with your skills.",
    "ru": "Примените свои навыки с пользой."
  },
  "Əhatə dairəsini yoxlayın, zəiflikləri məsuliyyətlə bildirin və töhfənizə görə mükafat qazanın.": {
    "az": "Əhatə dairəsini yoxlayın, zəiflikləri məsuliyyətlə bildirin və töhfənizə görə mükafat qazanın.",
    "en": "Check the scope, report vulnerabilities responsibly and earn rewards for your contribution.",
    "ru": "Изучите область тестирования, ответственно сообщайте об уязвимостях и получайте награды."
  },
  "Aktiv proqramlar": {
    "az": "Aktiv proqramlar",
    "en": "Active programs",
    "ru": "Активные программы"
  },
  "Təsdiqlənmiş hədəflər": {
    "az": "Təsdiqlənmiş hədəflər",
    "en": "Approved targets",
    "ru": "Одобренные цели"
  },
  "Pul mükafatlı": {
    "az": "Pul mükafatlı",
    "en": "Cash rewards",
    "ru": "Денежные награды"
  },
  "Bug bounty proqramları": {
    "az": "Bug bounty proqramları",
    "en": "Bug bounty programs",
    "ru": "Программы bug bounty"
  },
  "Ən yüksək mükafat": {
    "az": "Ən yüksək mükafat",
    "en": "Highest reward",
    "ru": "Максимальная награда"
  },
  "Kritik tapıntılar üçün": {
    "az": "Kritik tapıntılar üçün",
    "en": "For critical findings",
    "ru": "За критические уязвимости"
  },
  "Reputasiya proqramları": {
    "az": "Reputasiya proqramları",
    "en": "Reputation programs",
    "ru": "Репутационные программы"
  },
  "Təcrübənizi sübut edin": {
    "az": "Təcrübənizi sübut edin",
    "en": "Prove your skills",
    "ru": "Покажите свои навыки"
  },
  "Proqramları kəşf edin": {
    "az": "Proqramları kəşf edin",
    "en": "Explore programs",
    "ru": "Найти программы"
  },
  "Proqram axtar": {
    "az": "Proqram axtar",
    "en": "Search programs",
    "ru": "Поиск программ"
  },
  "Proqram və ya şirkət axtar…": {
    "az": "Proqram və ya şirkət axtar…",
    "en": "Search programs or companies…",
    "ru": "Поиск программ или компаний…"
  },
  "Mükafat növü": {
    "az": "Mükafat növü",
    "en": "Reward type",
    "ru": "Тип награды"
  },
  "Bütün mükafatlar": {
    "az": "Bütün mükafatlar",
    "en": "All rewards",
    "ru": "Все награды"
  },
  "Pul mükafatı": {
    "az": "Pul mükafatı",
    "en": "Cash reward",
    "ru": "Денежная награда"
  },
  "Reputasiya xalı": {
    "az": "Reputasiya xalı",
    "en": "Reputation points",
    "ru": "Баллы репутации"
  },
  "Reputasiya": {
    "az": "Reputasiya",
    "en": "Reputation",
    "ru": "Репутация"
  },
  "Aktiv": {
    "az": "Aktiv",
    "en": "Active",
    "ru": "Активна"
  },
  "Təsdiqlənib ✓": {
    "az": "Təsdiqlənib ✓",
    "en": "Approved ✓",
    "ru": "Одобрено ✓"
  },
  "MÜKAFAT ARALIĞI": {
    "az": "MÜKAFAT ARALIĞI",
    "en": "REWARD RANGE",
    "ru": "ДИАПАЗОН НАГРАД"
  },
  "Ətraflı bax →": {
    "az": "Ətraflı bax →",
    "en": "View details →",
    "ru": "Подробнее →"
  },
  "xal": {
    "az": "xal",
    "en": "points",
    "ru": "баллов"
  },
  "Proqram tapılmadı": {
    "az": "Proqram tapılmadı",
    "en": "No programs found",
    "ru": "Программы не найдены"
  },
  "Proqramlar təsdiqləndikdə burada görünəcək. Axtarış filtrlərini də yoxlaya bilərsiniz.": {
    "az": "Proqramlar təsdiqləndikdə burada görünəcək. Axtarış filtrlərini də yoxlaya bilərsiniz.",
    "en": "Approved programs will appear here. You can also check your search filters.",
    "ru": "Одобренные программы появятся здесь. Также проверьте фильтры поиска."
  },
  "Hər proqramın əhatə dairəsi və qaydaları fərqlidir. Testə başlamazdan əvvəl onları oxuyun.": {
    "az": "Hər proqramın əhatə dairəsi və qaydaları fərqlidir. Testə başlamazdan əvvəl onları oxuyun.",
    "en": "Each program has its own scope and rules. Read them before testing.",
    "ru": "У каждой программы своя область тестирования и правила. Прочитайте их до начала проверки."
  },
  "BUGCASP İCMASI": {
    "az": "BUGCASP İCMASI",
    "en": "BUGCASP COMMUNITY",
    "ru": "СООБЩЕСТВО BUGCASP"
  },
  "Həll olunmuş tapıntılar. Ölçülə bilən töhfələr.": {
    "az": "Həll olunmuş tapıntılar. Ölçülə bilən töhfələr.",
    "en": "Resolved findings. Measurable contributions.",
    "ru": "Устранённые уязвимости. Измеримый вклад."
  },
  "Təhlükəsizlik tədqiqatçısı": {
    "az": "Təhlükəsizlik tədqiqatçısı",
    "en": "Security researcher",
    "ru": "Исследователь безопасности"
  },
  "TƏDQİQATÇI MƏRKƏZİ": {
    "az": "TƏDQİQATÇI MƏRKƏZİ",
    "en": "RESEARCHER HUB",
    "ru": "КАБИНЕТ ИССЛЕДОВАТЕЛЯ"
  },
  "Tapıntılarınızın baxış və həll prosesini izləyin.": {
    "az": "Tapıntılarınızın baxış və həll prosesini izləyin.",
    "en": "Track the review and resolution of your findings.",
    "ru": "Следите за проверкой и устранением найденных уязвимостей."
  },
  "Təqdim etdiyiniz tapıntılar": {
    "az": "Təqdim etdiyiniz tapıntılar",
    "en": "Your submitted findings",
    "ru": "Ваши отправленные отчёты"
  },
  "Baxışdadır": {
    "az": "Baxışdadır",
    "en": "Under review",
    "ru": "На проверке"
  },
  "İlkin baxış gözləyir": {
    "az": "İlkin baxış gözləyir",
    "en": "Awaiting initial review",
    "ru": "Ожидают первичной проверки"
  },
  "Həll olunub": {
    "az": "Həll olunub",
    "en": "Resolved",
    "ru": "Устранено"
  },
  "Təsdiqlənmiş töhfələr": {
    "az": "Təsdiqlənmiş töhfələr",
    "en": "Verified contributions",
    "ru": "Подтверждённый вклад"
  },
  "Hesab üzrə ümumi xal": {
    "az": "Hesab üzrə ümumi xal",
    "en": "Total account points",
    "ru": "Общее количество баллов"
  },
  "HESABAT": {
    "az": "HESABAT",
    "en": "REPORT",
    "ru": "ОТЧЁТ"
  },
  "PROQRAM": {
    "az": "PROQRAM",
    "en": "PROGRAM",
    "ru": "ПРОГРАММА"
  },
  "CİDDİLİK": {
    "az": "CİDDİLİK",
    "en": "SEVERITY",
    "ru": "КРИТИЧНОСТЬ"
  },
  "STATUS": {
    "az": "STATUS",
    "en": "STATUS",
    "ru": "СТАТУС"
  },
  "Hələ hesabat yoxdur.": {
    "az": "Hələ hesabat yoxdur.",
    "en": "No reports yet.",
    "ru": "Отчётов пока нет."
  },
  "Qiymətləndirilməyib": {
    "az": "Qiymətləndirilməyib",
    "en": "Not assessed",
    "ru": "Не оценено"
  },
  "ŞİRKƏT PORTALI": {
    "az": "ŞİRKƏT PORTALI",
    "en": "COMPANY PORTAL",
    "ru": "КАБИНЕТ КОМПАНИИ"
  },
  "Təhlükəsizlik iş sahəsi": {
    "az": "Təhlükəsizlik iş sahəsi",
    "en": "Security workspace",
    "ru": "Рабочее пространство безопасности"
  },
  "Proqramlarınızı və daxil olan hesabatları idarə edin.": {
    "az": "Proqramlarınızı və daxil olan hesabatları idarə edin.",
    "en": "Manage your programs and incoming reports.",
    "ru": "Управляйте программами и входящими отчётами."
  },
  "Şirkət statusu:": {
    "az": "Şirkət statusu:",
    "en": "Company status:",
    "ru": "Статус компании:"
  },
  "Proqram yaratmaq üçün platforma təsdiqi gözlənilir.": {
    "az": "Proqram yaratmaq üçün platforma təsdiqi gözlənilir.",
    "en": "Platform approval is required before creating programs.",
    "ru": "Для создания программ требуется одобрение платформы."
  },
  "Şirkətinizin proqramları": {
    "az": "Şirkətinizin proqramları",
    "en": "Your company’s programs",
    "ru": "Программы вашей компании"
  },
  "Yeni hesabatlar": {
    "az": "Yeni hesabatlar",
    "en": "New reports",
    "ru": "Новые отчёты"
  },
  "Bağlanmış tapıntılar": {
    "az": "Bağlanmış tapıntılar",
    "en": "Resolved findings",
    "ru": "Закрытые отчёты"
  },
  "Ödənilmiş mükafat": {
    "az": "Ödənilmiş mükafat",
    "en": "Paid rewards",
    "ru": "Выплаченные награды"
  },
  "Şirkət tərəfindən təsdiqlənib": {
    "az": "Şirkət tərəfindən təsdiqlənib",
    "en": "Confirmed by the company",
    "ru": "Подтверждено компанией"
  },
  "Proqramlarım": {
    "az": "Proqramlarım",
    "en": "My programs",
    "ru": "Мои программы"
  },
  "TƏSDİQ": {
    "az": "TƏSDİQ",
    "en": "APPROVAL",
    "ru": "ОДОБРЕНИЕ"
  },
  "VƏZİYYƏT": {
    "az": "VƏZİYYƏT",
    "en": "STATE",
    "ru": "СОСТОЯНИЕ"
  },
  "Dayandırılıb": {
    "az": "Dayandırılıb",
    "en": "Paused",
    "ru": "Приостановлена"
  },
  "Dayandır": {
    "az": "Dayandır",
    "en": "Pause",
    "ru": "Приостановить"
  },
  "Aktiv et": {
    "az": "Aktiv et",
    "en": "Activate",
    "ru": "Активировать"
  },
  "Hələ proqram yaradılmayıb.": {
    "az": "Hələ proqram yaradılmayıb.",
    "en": "No programs created yet.",
    "ru": "Программ пока нет."
  },
  "Daxil olan hesabatlar": {
    "az": "Daxil olan hesabatlar",
    "en": "Incoming reports",
    "ru": "Входящие отчёты"
  },
  "PLATFORMA İDARƏETMƏSİ": {
    "az": "PLATFORMA İDARƏETMƏSİ",
    "en": "PLATFORM MANAGEMENT",
    "ru": "УПРАВЛЕНИЕ ПЛАТФОРМОЙ"
  },
  "Müraciətləri yoxlayın, hesabatları izləyin və mübahisələri həll edin.": {
    "az": "Müraciətləri yoxlayın, hesabatları izləyin və mübahisələri həll edin.",
    "en": "Review applications, track reports and resolve disputes.",
    "ru": "Проверяйте заявки, отслеживайте отчёты и разрешайте споры."
  },
  "Ümumi ödəniş": {
    "az": "Ümumi ödəniş",
    "en": "Total payouts",
    "ru": "Общие выплаты"
  },
  "Şirkətlərin qeydə aldığı ödənişlər": {
    "az": "Şirkətlərin qeydə aldığı ödənişlər",
    "en": "Payouts recorded by companies",
    "ru": "Выплаты, отмеченные компаниями"
  },
  "Təsdiqlənmiş proqramlar": {
    "az": "Təsdiqlənmiş proqramlar",
    "en": "Approved programs",
    "ru": "Одобренные программы"
  },
  "Açıq hesabatlar": {
    "az": "Açıq hesabatlar",
    "en": "Open reports",
    "ru": "Открытые отчёты"
  },
  "New və Triaged": {
    "az": "New və Triaged",
    "en": "New and triaged",
    "ru": "Новые и проверенные"
  },
  "Tədqiqatçılar": {
    "az": "Tədqiqatçılar",
    "en": "Researchers",
    "ru": "Исследователи"
  },
  "E-poçtu təsdiqlənmiş": {
    "az": "E-poçtu təsdiqlənmiş",
    "en": "Email verified",
    "ru": "С подтверждённой почтой"
  },
  "Şirkət təsdiqləri": {
    "az": "Şirkət təsdiqləri",
    "en": "Company approvals",
    "ru": "Одобрение компаний"
  },
  "ŞİRKƏT": {
    "az": "ŞİRKƏT",
    "en": "COMPANY",
    "ru": "КОМПАНИЯ"
  },
  "SAHƏ": {
    "az": "SAHƏ",
    "en": "INDUSTRY",
    "ru": "ОТРАСЛЬ"
  },
  "QƏRAR": {
    "az": "QƏRAR",
    "en": "DECISION",
    "ru": "РЕШЕНИЕ"
  },
  "Təsdiqlə": {
    "az": "Təsdiqlə",
    "en": "Approve",
    "ru": "Одобрить"
  },
  "Rədd et": {
    "az": "Rədd et",
    "en": "Reject",
    "ru": "Отклонить"
  },
  "Gözləyən şirkət yoxdur.": {
    "az": "Gözləyən şirkət yoxdur.",
    "en": "No companies awaiting review.",
    "ru": "Нет компаний на проверке."
  },
  "Proqram təsdiqləri": {
    "az": "Proqram təsdiqləri",
    "en": "Program approvals",
    "ru": "Одобрение программ"
  },
  "Əhatə dairəsi:": {
    "az": "Əhatə dairəsi:",
    "en": "Scope:",
    "ru": "Область тестирования:"
  },
  "İstisnalar:": {
    "az": "İstisnalar:",
    "en": "Exclusions:",
    "ru": "Исключения:"
  },
  "Qaydalar:": {
    "az": "Qaydalar:",
    "en": "Rules:",
    "ru": "Правила:"
  },
  "Mükafat:": {
    "az": "Mükafat:",
    "en": "Reward:",
    "ru": "Награда:"
  },
  "Gözləyən proqram yoxdur.": {
    "az": "Gözləyən proqram yoxdur.",
    "en": "No programs awaiting review.",
    "ru": "Нет программ на проверке."
  },
  "Bütün hesabatlar": {
    "az": "Bütün hesabatlar",
    "en": "All reports",
    "ru": "Все отчёты"
  },
  "Ən fəal tədqiqatçılar": {
    "az": "Ən fəal tədqiqatçılar",
    "en": "Top researchers",
    "ru": "Лучшие исследователи"
  },
  "Hələ məlumat yoxdur.": {
    "az": "Hələ məlumat yoxdur.",
    "en": "No data yet.",
    "ru": "Данных пока нет."
  },
  "ƏHATƏ DAİRƏSİ": {
    "az": "ƏHATƏ DAİRƏSİ",
    "en": "IN SCOPE",
    "ru": "В ОБЛАСТИ ТЕСТИРОВАНИЯ"
  },
  "ƏHATƏ DAİRƏSİNDƏN KƏNAR": {
    "az": "ƏHATƏ DAİRƏSİNDƏN KƏNAR",
    "en": "OUT OF SCOPE",
    "ru": "ВНЕ ОБЛАСТИ ТЕСТИРОВАНИЯ"
  },
  "ARAŞDIRMA QAYDALARI": {
    "az": "ARAŞDIRMA QAYDALARI",
    "en": "RESEARCH RULES",
    "ru": "ПРАВИЛА ИССЛЕДОВАНИЯ"
  },
  "BugCasp-a qoşulun": {
    "az": "BugCasp-a qoşulun",
    "en": "Join BugCasp",
    "ru": "Присоединиться к BugCasp"
  },
  "Hesabınıza daxil olun": {
    "az": "Hesabınıza daxil olun",
    "en": "Sign in to your account",
    "ru": "Войдите в аккаунт"
  },
  "Şirkət": {
    "az": "Şirkət",
    "en": "Company",
    "ru": "Компания"
  },
  "İstifadəçi adı": {
    "az": "İstifadəçi adı",
    "en": "Username",
    "ru": "Имя пользователя"
  },
  "E-poçt ünvanı": {
    "az": "E-poçt ünvanı",
    "en": "Email address",
    "ru": "Электронная почта"
  },
  "İstifadəçi adı və ya e-poçt": {
    "az": "İstifadəçi adı və ya e-poçt",
    "en": "Username or email",
    "ru": "Имя пользователя или почта"
  },
  "Şifrə": {
    "az": "Şifrə",
    "en": "Password",
    "ru": "Пароль"
  },
  "Şirkət adı": {
    "az": "Şirkət adı",
    "en": "Company name",
    "ru": "Название компании"
  },
  "Fəaliyyət sahəsi": {
    "az": "Fəaliyyət sahəsi",
    "en": "Industry",
    "ru": "Отрасль"
  },
  "Əsas sayt": {
    "az": "Əsas sayt",
    "en": "Website",
    "ru": "Сайт"
  },
  "Haqqınızda": {
    "az": "Haqqınızda",
    "en": "About you",
    "ru": "О себе"
  },
  "GitHub profili": {
    "az": "GitHub profili",
    "en": "GitHub profile",
    "ru": "Профиль GitHub"
  },
  "TryHackMe profili": {
    "az": "TryHackMe profili",
    "en": "TryHackMe profile",
    "ru": "Профиль TryHackMe"
  },
  "Hack The Box profili": {
    "az": "Hack The Box profili",
    "en": "Hack The Box profile",
    "ru": "Профиль Hack The Box"
  },
  "E-poçt domeni yoxlanılır, hesab məktubdakı keçidlə aktivləşir. Şifrə: ən azı 12 simvol.": {
    "az": "E-poçt domeni yoxlanılır, hesab məktubdakı keçidlə aktivləşir. Şifrə: ən azı 12 simvol.",
    "en": "We check your email domain. Activate your account using the email link. Password: at least 12 characters.",
    "ru": "Домен почты проверяется. Активируйте аккаунт по ссылке в письме. Пароль: не менее 12 символов."
  },
  "Hesabım var": {
    "az": "Hesabım var",
    "en": "I have an account",
    "ru": "У меня есть аккаунт"
  },
  "Hesab yarat": {
    "az": "Hesab yarat",
    "en": "Create account",
    "ru": "Создать аккаунт"
  },
  "Qeydiyyatdan keç": {
    "az": "Qeydiyyatdan keç",
    "en": "Register",
    "ru": "Зарегистрироваться"
  },
  "Şifrəni unutmuşam": {
    "az": "Şifrəni unutmuşam",
    "en": "Forgot password",
    "ru": "Забыли пароль"
  },
  "Təsdiq məktubunu yenidən göndər": {
    "az": "Təsdiq məktubunu yenidən göndər",
    "en": "Resend verification email",
    "ru": "Отправить письмо повторно"
  },
  "Şifrənin bərpası": {
    "az": "Şifrənin bərpası",
    "en": "Password recovery",
    "ru": "Восстановление пароля"
  },
  "Hesabın e-poçtu": {
    "az": "Hesabın e-poçtu",
    "en": "Account email",
    "ru": "Почта аккаунта"
  },
  "Təsdiqlənmiş e-poçtunuza 30 dəqiqə etibarlı keçid göndəriləcək.": {
    "az": "Təsdiqlənmiş e-poçtunuza 30 dəqiqə etibarlı keçid göndəriləcək.",
    "en": "A link valid for 30 minutes will be sent to your verified email.",
    "ru": "На подтверждённую почту будет отправлена ссылка, действующая 30 минут."
  },
  "Bərpa keçidi göndər": {
    "az": "Bərpa keçidi göndər",
    "en": "Send recovery link",
    "ru": "Отправить ссылку"
  },
  "Yeni şifrə təyin et": {
    "az": "Yeni şifrə təyin et",
    "en": "Set a new password",
    "ru": "Задать новый пароль"
  },
  "Yeni şifrə": {
    "az": "Yeni şifrə",
    "en": "New password",
    "ru": "Новый пароль"
  },
  "Şifrəni təkrarla": {
    "az": "Şifrəni təkrarla",
    "en": "Repeat password",
    "ru": "Повторите пароль"
  },
  "Ən azı 12 simvol. Köhnə giriş sessiyaları bağlanacaq.": {
    "az": "Ən azı 12 simvol. Köhnə giriş sessiyaları bağlanacaq.",
    "en": "At least 12 characters. Previous sessions will be signed out.",
    "ru": "Не менее 12 символов. Предыдущие сеансы будут завершены."
  },
  "Şifrəni yenilə": {
    "az": "Şifrəni yenilə",
    "en": "Update password",
    "ru": "Обновить пароль"
  },
  "Yeni keçid istə": {
    "az": "Yeni keçid istə",
    "en": "Request a new link",
    "ru": "Запросить новую ссылку"
  },
  "E-poçt təsdiqləndi": {
    "az": "E-poçt təsdiqləndi",
    "en": "Email verified",
    "ru": "Почта подтверждена"
  },
  "Hesabınız aktivləşdi. İndi daxil ola bilərsiniz.": {
    "az": "Hesabınız aktivləşdi. İndi daxil ola bilərsiniz.",
    "en": "Your account is active. You can now sign in.",
    "ru": "Аккаунт активирован. Теперь можно войти."
  },
  "Xoş gəldiniz məktubu:": {
    "az": "Xoş gəldiniz məktubu:",
    "en": "Welcome email:",
    "ru": "Приветственное письмо:"
  },
  "Təsdiq alınmadı": {
    "az": "Təsdiq alınmadı",
    "en": "Verification failed",
    "ru": "Подтверждение не удалось"
  },
  "Proqram seçin": {
    "az": "Proqram seçin",
    "en": "Select a program",
    "ru": "Выберите программу"
  },
  "Aktiv proqram yoxdur.": {
    "az": "Aktiv proqram yoxdur.",
    "en": "No active programs.",
    "ru": "Нет активных программ."
  },
  "Zəiflik hesabatı": {
    "az": "Zəiflik hesabatı",
    "en": "Vulnerability report",
    "ru": "Отчёт об уязвимости"
  },
  "Hesabat başlığı": {
    "az": "Hesabat başlığı",
    "en": "Report title",
    "ru": "Заголовок отчёта"
  },
  "CWE / OWASP kateqoriyası": {
    "az": "CWE / OWASP kateqoriyası",
    "en": "CWE / OWASP category",
    "ru": "Категория CWE / OWASP"
  },
  "SÜBUT FAYLI": {
    "az": "SÜBUT FAYLI",
    "en": "EVIDENCE FILE",
    "ru": "ФАЙЛ С ДОКАЗАТЕЛЬСТВОМ"
  },
  "PDF və ya TXT faylını buraya sürüşdürün": {
    "az": "PDF və ya TXT faylını buraya sürüşdürün",
    "en": "Drop a PDF or TXT file here",
    "ru": "Перетащите файл PDF или TXT сюда"
  },
  "Yalnız .pdf və .txt · maksimum 4 MB": {
    "az": "Yalnız .pdf və .txt · maksimum 4 MB",
    "en": "Only .pdf and .txt · up to 4 MB",
    "ru": "Только .pdf и .txt · до 4 МБ"
  },
  "Sübut faylı seç": {
    "az": "Sübut faylı seç",
    "en": "Choose evidence file",
    "ru": "Выберите файл"
  },
  "Təkrarlama addımlarını və təsiri sübut faylında izah edin.": {
    "az": "Təkrarlama addımlarını və təsiri sübut faylında izah edin.",
    "en": "Describe the reproduction steps and impact in the evidence file.",
    "ru": "Опишите шаги воспроизведения и влияние в файле."
  },
  "Hesabatı göndər": {
    "az": "Hesabatı göndər",
    "en": "Submit report",
    "ru": "Отправить отчёт"
  },
  "Yeni bug bounty proqramı": {
    "az": "Yeni bug bounty proqramı",
    "en": "New bug bounty program",
    "ru": "Новая программа bug bounty"
  },
  "01 · Əsas məlumatlar": {
    "az": "01 · Əsas məlumatlar",
    "en": "01 · Basic details",
    "ru": "01 · Основные сведения"
  },
  "02 · Mükafat və qaydalar": {
    "az": "02 · Mükafat və qaydalar",
    "en": "02 · Rewards and rules",
    "ru": "02 · Награды и правила"
  },
  "Proqram adı": {
    "az": "Proqram adı",
    "en": "Program name",
    "ru": "Название программы"
  },
  "Hədəf URL": {
    "az": "Hədəf URL",
    "en": "Target URL",
    "ru": "URL цели"
  },
  "Əhatə dairəsindəki aktivlər": {
    "az": "Əhatə dairəsindəki aktivlər",
    "en": "In-scope assets",
    "ru": "Активы в области тестирования"
  },
  "Əhatə dairəsindən kənar": {
    "az": "Əhatə dairəsindən kənar",
    "en": "Out of scope",
    "ru": "Вне области тестирования"
  },
  "Davam et →": {
    "az": "Davam et →",
    "en": "Continue →",
    "ru": "Продолжить →"
  },
  "Pul mükafatı (AZN — manat)": {
    "az": "Pul mükafatı (AZN — manat)",
    "en": "Cash reward (AZN — manat)",
    "ru": "Денежная награда (AZN — манат)"
  },
  "LOW mükafatı": {
    "az": "LOW mükafatı",
    "en": "Low severity reward",
    "ru": "Награда за низкую критичность"
  },
  "MEDIUM mükafatı": {
    "az": "MEDIUM mükafatı",
    "en": "Medium severity reward",
    "ru": "Награда за среднюю критичность"
  },
  "HIGH mükafatı": {
    "az": "HIGH mükafatı",
    "en": "High severity reward",
    "ru": "Награда за высокую критичность"
  },
  "CRITICAL mükafatı": {
    "az": "CRITICAL mükafatı",
    "en": "Critical severity reward",
    "ru": "Награда за критическую уязвимость"
  },
  "Araşdırma qaydaları (RoE)": {
    "az": "Araşdırma qaydaları (RoE)",
    "en": "Rules of engagement (RoE)",
    "ru": "Правила тестирования (RoE)"
  },
  "Proqram admin təsdiqindən sonra ictimai siyahıya əlavə olunacaq.": {
    "az": "Proqram admin təsdiqindən sonra ictimai siyahıya əlavə olunacaq.",
    "en": "The program will be listed after admin approval.",
    "ru": "Программа появится в списке после одобрения администратором."
  },
  "Təsdiqə göndər": {
    "az": "Təsdiqə göndər",
    "en": "Submit for approval",
    "ru": "Отправить на одобрение"
  },
  "Təkrarlama addımları": {
    "az": "Təkrarlama addımları",
    "en": "Steps to reproduce",
    "ru": "Шаги воспроизведения"
  },
  "Təsir analizi": {
    "az": "Təsir analizi",
    "en": "Impact analysis",
    "ru": "Оценка влияния"
  },
  "HTTP sorğu / cavab": {
    "az": "HTTP sorğu / cavab",
    "en": "HTTP request / response",
    "ru": "HTTP-запрос / ответ"
  },
  "Mübahisə": {
    "az": "Mübahisə",
    "en": "Dispute",
    "ru": "Спор"
  },
  "Admin qeydi": {
    "az": "Admin qeydi",
    "en": "Admin note",
    "ru": "Примечание администратора"
  },
  "▤ Sübut faylını aç": {
    "az": "▤ Sübut faylını aç",
    "en": "▤ Open evidence",
    "ru": "▤ Открыть доказательство"
  },
  "reputasiya xalı": {
    "az": "reputasiya xalı",
    "en": "reputation points",
    "ru": "баллов репутации"
  },
  "ödənilib": {
    "az": "ödənilib",
    "en": "paid",
    "ru": "выплачено"
  },
  "mükafat təsdiqlənib": {
    "az": "mükafat təsdiqlənib",
    "en": "reward approved",
    "ru": "награда подтверждена"
  },
  "HESABATIN İDARƏ EDİLMƏSİ": {
    "az": "HESABATIN İDARƏ EDİLMƏSİ",
    "en": "REPORT MANAGEMENT",
    "ru": "УПРАВЛЕНИЕ ОТЧЁТОМ"
  },
  "Status": {
    "az": "Status",
    "en": "Status",
    "ru": "Статус"
  },
  "Təhlükə dərəcəsi": {
    "az": "Təhlükə dərəcəsi",
    "en": "Severity",
    "ru": "Критичность"
  },
  "Dərəcə seçin": {
    "az": "Dərəcə seçin",
    "en": "Select severity",
    "ru": "Выберите критичность"
  },
  "Mediation qeydi": {
    "az": "Mediation qeydi",
    "en": "Mediation note",
    "ru": "Примечание по спору"
  },
  "Baxış qeydi": {
    "az": "Baxış qeydi",
    "en": "Review note",
    "ru": "Примечание к проверке"
  },
  "Xarici ödənişi qeydə al": {
    "az": "Xarici ödənişi qeydə al",
    "en": "Record external payment",
    "ru": "Отметить внешнюю выплату"
  },
  "Statusu yenilə": {
    "az": "Statusu yenilə",
    "en": "Update status",
    "ru": "Обновить статус"
  },
  "Admin baxışı istə": {
    "az": "Admin baxışı istə",
    "en": "Request admin review",
    "ru": "Запросить проверку администратора"
  },
  "Sübut sənədi": {
    "az": "Sübut sənədi",
    "en": "Evidence document",
    "ru": "Документ с доказательством"
  },
  "Sübut sənədinə baxış": {
    "az": "Sübut sənədinə baxış",
    "en": "Evidence viewer",
    "ru": "Просмотр доказательства"
  },
  "Faylı endir": {
    "az": "Faylı endir",
    "en": "Download file",
    "ru": "Скачать файл"
  },
  "Hesabata qayıt": {
    "az": "Hesabata qayıt",
    "en": "Back to report",
    "ru": "Вернуться к отчёту"
  },
  "Təsdiq qərarı": {
    "az": "Təsdiq qərarı",
    "en": "Approval decision",
    "ru": "Решение об одобрении"
  },
  "Rədd qərarı": {
    "az": "Rədd qərarı",
    "en": "Rejection decision",
    "ru": "Решение об отклонении"
  },
  "Müraciəti təsdiqləmək": {
    "az": "Müraciəti təsdiqləmək",
    "en": "Approve the application",
    "ru": "Одобрить заявку"
  },
  "Müraciəti rədd etmək": {
    "az": "Müraciəti rədd etmək",
    "en": "Reject the application",
    "ru": "Отклонить заявку"
  },
  "üçün qərarınızı qeydə alın.": {
    "az": "üçün qərarınızı qeydə alın.",
    "en": "— record your decision.",
    "ru": "— укажите причину решения."
  },
  "Qərarı saxla": {
    "az": "Qərarı saxla",
    "en": "Save decision",
    "ru": "Сохранить решение"
  },
  "E-poçt": {
    "az": "E-poçt",
    "en": "Email",
    "ru": "Электронная почта"
  },
  "Mübahisənin səbəbi": {
    "az": "Mübahisənin səbəbi",
    "en": "Reason for dispute",
    "ru": "Причина спора"
  },
  "Adminə göndər": {
    "az": "Adminə göndər",
    "en": "Send to admin",
    "ru": "Отправить администратору"
  },
  "Ödənişi qeydə al": {
    "az": "Ödənişi qeydə al",
    "en": "Record payment",
    "ru": "Отметить выплату"
  },
  "Bu əməliyyat pul köçürmür. Yalnız ayrıca etdiyiniz ödənişi qeydə alır.": {
    "az": "Bu əməliyyat pul köçürmür. Yalnız ayrıca etdiyiniz ödənişi qeydə alır.",
    "en": "This does not transfer money. It records a payment made separately.",
    "ru": "Это действие не переводит деньги, а отмечает выплату, выполненную отдельно."
  },
  "Tədqiqatçıya ödənişin edildiyini təsdiqləyirəm.": {
    "az": "Tədqiqatçıya ödənişin edildiyini təsdiqləyirəm.",
    "en": "I confirm the researcher has been paid.",
    "ru": "Подтверждаю выплату исследователю."
  },
  "Ödənilmiş kimi işarələ": {
    "az": "Ödənilmiş kimi işarələ",
    "en": "Mark as paid",
    "ru": "Отметить как выплаченное"
  },
  "HESABIN İDARƏ EDİLMƏSİ": {
    "az": "HESABIN İDARƏ EDİLMƏSİ",
    "en": "ACCOUNT MANAGEMENT",
    "ru": "УПРАВЛЕНИЕ АККАУНТОМ"
  },
  "İstifadəçi adınızı və şifrənizi buradan dəyişin.": {
    "az": "İstifadəçi adınızı və şifrənizi buradan dəyişin.",
    "en": "Change your username and password here.",
    "ru": "Здесь можно изменить имя пользователя и пароль."
  },
  "Admin hesabınız e-poçta bağlı deyil. İstifadəçi adı və şifrə ilə daxil olursunuz.": {
    "az": "Admin hesabınız e-poçta bağlı deyil. İstifadəçi adı və şifrə ilə daxil olursunuz.",
    "en": "Your admin account has no email. Sign in with your username and password.",
    "ru": "У аккаунта администратора нет почты. Вход по имени пользователя и паролю."
  },
  "E-poçt:": {
    "az": "E-poçt:",
    "en": "Email:",
    "ru": "Почта:"
  },
  "Dəyişiklikdən sonra digər sessiyalar bağlanacaq.": {
    "az": "Dəyişiklikdən sonra digər sessiyalar bağlanacaq.",
    "en": "Other sessions will be signed out after the change.",
    "ru": "После изменения другие сеансы будут завершены."
  },
  "Cari şifrə": {
    "az": "Cari şifrə",
    "en": "Current password",
    "ru": "Текущий пароль"
  },
  "Yeni şifrəni təkrarlayın": {
    "az": "Yeni şifrəni təkrarlayın",
    "en": "Repeat new password",
    "ru": "Повторите новый пароль"
  },
  "Şifrəni dəyişmək istəmirsinizsə, yeni şifrə xanalarını boş saxlayın. Yeni şifrə ən azı 8 simvol olmalıdır.": {
    "az": "Şifrəni dəyişmək istəmirsinizsə, yeni şifrə xanalarını boş saxlayın. Yeni şifrə ən azı 8 simvol olmalıdır.",
    "en": "Leave the new password fields empty to keep your password. A new password must have at least 8 characters.",
    "ru": "Оставьте поля нового пароля пустыми, чтобы сохранить пароль. Новый пароль должен содержать не менее 8 символов."
  },
  "Dəyişiklikləri saxla": {
    "az": "Dəyişiklikləri saxla",
    "en": "Save changes",
    "ru": "Сохранить изменения"
  },
  "Məlumat yüklənmədi": {
    "az": "Məlumat yüklənmədi",
    "en": "Could not load data",
    "ru": "Не удалось загрузить данные"
  },
  "Yenidən yoxla": {
    "az": "Yenidən yoxla",
    "en": "Try again",
    "ru": "Повторить"
  },
  "E-poçtunuzu yoxlayın": {
    "az": "E-poçtunuzu yoxlayın",
    "en": "Check your email",
    "ru": "Проверьте почту"
  },
  "Girişə qayıt": {
    "az": "Girişə qayıt",
    "en": "Back to sign in",
    "ru": "Вернуться ко входу"
  },
  "E-poçtunuzu təsdiqləyin": {
    "az": "E-poçtunuzu təsdiqləyin",
    "en": "Verify your email",
    "ru": "Подтвердите почту"
  },
  "Qeydiyyat alındı. Hesab yalnız e-poçt təsdiqindən sonra aktivləşəcək.": {
    "az": "Qeydiyyat alındı. Hesab yalnız e-poçt təsdiqindən sonra aktivləşəcək.",
    "en": "Registration received. Your account activates after email verification.",
    "ru": "Регистрация принята. Аккаунт активируется после подтверждения почты."
  },
  "Təsdiq keçidi e-poçt ünvanınıza göndərildi.": {
    "az": "Təsdiq keçidi e-poçt ünvanınıza göndərildi.",
    "en": "A verification link was sent to your email.",
    "ru": "Ссылка для подтверждения отправлена на почту."
  },
  "Məktub göndərilmədi. Administrator e-poçt xidmətinin sazlamalarını tamamladıqdan sonra yenidən göndərməyi yoxlayın.": {
    "az": "Məktub göndərilmədi. Administrator e-poçt xidmətinin sazlamalarını tamamladıqdan sonra yenidən göndərməyi yoxlayın.",
    "en": "Email was not sent. Try again after the administrator configures the email service.",
    "ru": "Письмо не отправлено. Повторите после настройки почтового сервиса администратором."
  },
  "Yenidən göndər": {
    "az": "Yenidən göndər",
    "en": "Resend",
    "ru": "Отправить повторно"
  },
  "Poçt serveri yoxlanılır…": {
    "az": "Poçt serveri yoxlanılır…",
    "en": "Checking mail server…",
    "ru": "Проверка почтового сервера…"
  },
  "Poçt serveri tapıldı. Ünvan məktubdakı keçidlə təsdiqlənəcək.": {
    "az": "Poçt serveri tapıldı. Ünvan məktubdakı keçidlə təsdiqlənəcək.",
    "en": "Mail server found. Verify the address using the email link.",
    "ru": "Почтовый сервер найден. Подтвердите адрес по ссылке в письме."
  },
  "Şifrələr uyğun gəlmir.": {
    "az": "Şifrələr uyğun gəlmir.",
    "en": "Passwords do not match.",
    "ru": "Пароли не совпадают."
  },
  "Yeni şifrələr uyğun deyil.": {
    "az": "Yeni şifrələr uyğun deyil.",
    "en": "New passwords do not match.",
    "ru": "Новые пароли не совпадают."
  },
  "Şifrəniz yeniləndi. Yeni şifrə ilə daxil olun.": {
    "az": "Şifrəniz yeniləndi. Yeni şifrə ilə daxil olun.",
    "en": "Password updated. Sign in with your new password.",
    "ru": "Пароль обновлён. Войдите с новым паролем."
  },
  "Hesab gözləmədədirsə, yeni məktub tələb edildi.": {
    "az": "Hesab gözləmədədirsə, yeni məktub tələb edildi.",
    "en": "If the account is pending, a new email has been requested.",
    "ru": "Если аккаунт ожидает подтверждения, запрошено новое письмо."
  },
  "Sübut faylını əlavə edin.": {
    "az": "Sübut faylını əlavə edin.",
    "en": "Please attach an evidence file.",
    "ru": "Прикрепите файл с доказательством."
  },
  "Hesabat göndərildi.": {
    "az": "Hesabat göndərildi.",
    "en": "Report submitted.",
    "ru": "Отчёт отправлен."
  },
  "Proqram təsdiq üçün göndərildi.": {
    "az": "Proqram təsdiq üçün göndərildi.",
    "en": "Program submitted for approval.",
    "ru": "Программа отправлена на одобрение."
  },
  "Təhlükə dərəcəsini seçin.": {
    "az": "Təhlükə dərəcəsini seçin.",
    "en": "Select a severity level.",
    "ru": "Выберите критичность."
  },
  "Hesabat statusu yeniləndi.": {
    "az": "Hesabat statusu yeniləndi.",
    "en": "Report status updated.",
    "ru": "Статус отчёта обновлён."
  },
  "Qərar saxlanıldı.": {
    "az": "Qərar saxlanıldı.",
    "en": "Decision saved.",
    "ru": "Решение сохранено."
  },
  "Admin baxışı tələb edildi.": {
    "az": "Admin baxışı tələb edildi.",
    "en": "Admin review requested.",
    "ru": "Запрошена проверка администратора."
  },
  "Xarici ödəniş qeydə alındı.": {
    "az": "Xarici ödəniş qeydə alındı.",
    "en": "External payment recorded.",
    "ru": "Внешняя выплата отмечена."
  },
  "Proqramın vəziyyəti yeniləndi.": {
    "az": "Proqramın vəziyyəti yeniləndi.",
    "en": "Program state updated.",
    "ru": "Состояние программы обновлено."
  },
  "Fayla giriş mümkün deyil.": {
    "az": "Fayla giriş mümkün deyil.",
    "en": "Cannot access the file.",
    "ru": "Нет доступа к файлу."
  },
  "Yalnız boş olmayan .pdf və .txt faylları qəbul edilir (maksimum 4 MB).": {
    "az": "Yalnız boş olmayan .pdf və .txt faylları qəbul edilir (maksimum 4 MB).",
    "en": "Only non-empty .pdf and .txt files are accepted (up to 4 MB).",
    "ru": "Принимаются только непустые файлы .pdf и .txt (до 4 МБ)."
  },
  "Hesabınıza daxil olun.": {
    "az": "Hesabınıza daxil olun.",
    "en": "Sign in to your account.",
    "ru": "Войдите в аккаунт."
  },
  "Hesabatlarınızı görmək üçün tədqiqatçı hesabına daxil olun.": {
    "az": "Hesabatlarınızı görmək üçün tədqiqatçı hesabına daxil olun.",
    "en": "Sign in as a researcher to view your reports.",
    "ru": "Войдите как исследователь, чтобы увидеть отчёты."
  },
  "Şirkət hesabına daxil olun.": {
    "az": "Şirkət hesabına daxil olun.",
    "en": "Sign in to your company account.",
    "ru": "Войдите в аккаунт компании."
  },
  "Admin girişi tələb olunur.": {
    "az": "Admin girişi tələb olunur.",
    "en": "Admin access required.",
    "ru": "Требуется вход администратора."
  },
  "Proqram yaratmaq üçün şirkət hesabı tələb olunur.": {
    "az": "Proqram yaratmaq üçün şirkət hesabı tələb olunur.",
    "en": "A company account is required to create programs.",
    "ru": "Для создания программ нужен аккаунт компании."
  },
  "Server cavabı oxunmadı.": {
    "az": "Server cavabı oxunmadı.",
    "en": "Could not read server response.",
    "ru": "Не удалось прочитать ответ сервера."
  },
  "Sorğu alınmadı.": {
    "az": "Sorğu alınmadı.",
    "en": "Request failed.",
    "ru": "Не удалось выполнить запрос."
  },
  "İnterfeys önizləməsi": {
    "az": "İnterfeys önizləməsi",
    "en": "Interface preview",
    "ru": "Предпросмотр интерфейса"
  },
  "Rol": {
    "az": "Rol",
    "en": "Role",
    "ru": "Роль"
  },
  "Qonaq": {
    "az": "Qonaq",
    "en": "Guest",
    "ru": "Гость"
  },
  "Admin": {
    "az": "Admin",
    "en": "Admin",
    "ru": "Администратор"
  },
  "Nümunə məlumatları. Dəyişikliklər saxlanılmır, e-poçt göndərilmir.": {
    "az": "Nümunə məlumatları. Dəyişikliklər saxlanılmır, e-poçt göndərilmir.",
    "en": "Sample data. Changes are not saved and no email is sent.",
    "ru": "Пример данных. Изменения не сохраняются, письма не отправляются."
  },
  "Hesabat": {
    "az": "Hesabat",
    "en": "Report",
    "ru": "Отчёт"
  },
  "Təhlükəsizliyi gücləndirən tədqiqatçılar.": {
    "az": "Təhlükəsizliyi gücləndirən tədqiqatçılar.",
    "en": "Researchers strengthening security.",
    "ru": "Исследователи, повышающие безопасность."
  },
  "Reputasiya xalları yalnız hesabat həll olunduqda verilir.": {
    "az": "Reputasiya xalları yalnız hesabat həll olunduqda verilir.",
    "en": "Reputation points are awarded only when a report is resolved.",
    "ru": "Баллы репутации начисляются только после устранения уязвимости."
  },
  "HALL OF FAME": {
    "az": "HALL OF FAME",
    "en": "HALL OF FAME",
    "ru": "ЗАЛ СЛАВЫ"
  },
  "SIRA": {
    "az": "SIRA",
    "en": "RANK",
    "ru": "МЕСТО"
  },
  "TƏDQİQATÇI": {
    "az": "TƏDQİQATÇI",
    "en": "RESEARCHER",
    "ru": "ИССЛЕДОВАТЕЛЬ"
  },
  "HƏLL OLUNMUŞ": {
    "az": "HƏLL OLUNMUŞ",
    "en": "RESOLVED",
    "ru": "УСТРАНЕНО"
  },
  "REPUTASİYA": {
    "az": "REPUTASİYA",
    "en": "REPUTATION",
    "ru": "РЕПУТАЦИЯ"
  },
  "hesabat": {
    "az": "hesabat",
    "en": "reports",
    "ru": "отчётов"
  },
  "İlk təsdiqlənmiş tədqiqatçıları gözləyirik.": {
    "az": "İlk təsdiqlənmiş tədqiqatçıları gözləyirik.",
    "en": "Awaiting the first verified researchers.",
    "ru": "Ожидаем первых подтверждённых исследователей."
  },
  "Triage prosesi": {
    "az": "Triage prosesi",
    "en": "Triage process",
    "ru": "Первичная проверка"
  },
  "Server sazlanması tamamlanmayıb və ya baza əlçatan deyil.": {
    "az": "Server sazlanması tamamlanmayıb və ya baza əlçatan deyil.",
    "en": "Server setup is incomplete or the database is unavailable.",
    "ru": "Настройка сервера не завершена или база данных недоступна."
  },
  "Əvvəl təhlükə dərəcəsini seçin.": {
    "az": "Əvvəl təhlükə dərəcəsini seçin.",
    "en": "Select a severity level first.",
    "ru": "Сначала выберите критичность."
  },
  "Mükafat hesablandıqdan sonra təhlükə dərəcəsi dəyişdirilə bilməz.": {
    "az": "Mükafat hesablandıqdan sonra təhlükə dərəcəsi dəyişdirilə bilməz.",
    "en": "Severity cannot be changed after rewards have been calculated.",
    "ru": "Критичность нельзя менять после начисления награды."
  },
  "Bu istifadəçi adı platforma sahibi üçün ayrılıb.": {
    "az": "Bu istifadəçi adı platforma sahibi üçün ayrılıb.",
    "en": "This username is reserved for the platform owner.",
    "ru": "Это имя зарезервировано для владельца платформы."
  },
  "İstifadəçi adı, e-poçt və ya şifrə yanlışdır.": {
    "az": "İstifadəçi adı, e-poçt və ya şifrə yanlışdır.",
    "en": "Incorrect username, email or password.",
    "ru": "Неверное имя пользователя, почта или пароль."
  },
  "Cari şifrə yanlışdır.": {
    "az": "Cari şifrə yanlışdır.",
    "en": "Current password is incorrect.",
    "ru": "Текущий пароль неверен."
  },
  "Bu istifadəçi adı ayrılıb.": {
    "az": "Bu istifadəçi adı ayrılıb.",
    "en": "This username is reserved.",
    "ru": "Это имя пользователя зарезервировано."
  },
  "Hesab başqa sorğuda yenilənib. Yenidən daxil olun.": {
    "az": "Hesab başqa sorğuda yenilənib. Yenidən daxil olun.",
    "en": "Your account was updated in another request. Sign in again.",
    "ru": "Аккаунт обновлён в другом запросе. Войдите повторно."
  },
  "Bu istifadəçi adı artıq istifadə olunur.": {
    "az": "Bu istifadəçi adı artıq istifadə olunur.",
    "en": "This username is already in use.",
    "ru": "Это имя пользователя уже занято."
  },
  "Başlıq, kateqoriya və sübut faylı tələb olunur.": {
    "az": "Başlıq, kateqoriya və sübut faylı tələb olunur.",
    "en": "Title, category and evidence file are required.",
    "ru": "Нужны заголовок, категория и файл с доказательством."
  },
  "Sübut faylı boş olmamalı və 4 MB həddini keçməməlidir.": {
    "az": "Sübut faylı boş olmamalı və 4 MB həddini keçməməlidir.",
    "en": "The evidence file must not be empty or exceed 4 MB.",
    "ru": "Файл не должен быть пустым или превышать 4 МБ."
  },
  "Çox sayda cəhd edildi. Bir az sonra yenidən yoxlayın.": {
    "az": "Çox sayda cəhd edildi. Bir az sonra yenidən yoxlayın.",
    "en": "Too many attempts. Try again later.",
    "ru": "Слишком много попыток. Повторите позже."
  },
  "Bərpa keçidi etibarsızdır və ya vaxtı bitib. Yeni keçid istəyin.": {
    "az": "Bərpa keçidi etibarsızdır və ya vaxtı bitib. Yeni keçid istəyin.",
    "en": "The recovery link is invalid or expired. Request a new link.",
    "ru": "Ссылка восстановления недействительна или устарела. Запросите новую."
  },
  "Bu e-poçtla təsdiqlənmiş hesab varsa, bərpa keçidi göndərilməsi istənildi. Gələnlər və spam qovluğunu yoxlayın.": {
    "az": "Bu e-poçtla təsdiqlənmiş hesab varsa, bərpa keçidi göndərilməsi istənildi. Gələnlər və spam qovluğunu yoxlayın.",
    "en": "If a verified account uses this email, a recovery link has been requested. Check your inbox and spam folder.",
    "ru": "Если у подтверждённого аккаунта есть эта почта, запрошена ссылка восстановления. Проверьте входящие и спам."
  },
  "Hesab yeniləndi. Köhnə sessiyalar bağlandı.": {
    "az": "Hesab yeniləndi. Köhnə sessiyalar bağlandı.",
    "en": "Account updated. Previous sessions were signed out.",
    "ru": "Аккаунт обновлён. Предыдущие сеансы завершены."
  },
  "Məlumatları yoxlayıb yenidən göndərin.": {
    "az": "Məlumatları yoxlayıb yenidən göndərin.",
    "en": "Check the form details and try again.",
    "ru": "Проверьте данные формы и повторите."
  },
  "Bağlantı alınmadı. İnternet bağlantınızı yoxlayın.": {
    "az": "Bağlantı alınmadı. İnternet bağlantınızı yoxlayın.",
    "en": "Connection failed. Check your internet connection.",
    "ru": "Не удалось подключиться. Проверьте интернет-соединение."
  },
  "Sübut faylı tapılmadı.": {
    "az": "Sübut faylı tapılmadı.",
    "en": "Evidence file not found.",
    "ru": "Файл с доказательством не найден."
  },
  "Sübut fayllarının yaddaşı hələ sazlanmayıb.": {
    "az": "Sübut fayllarının yaddaşı hələ sazlanmayıb.",
    "en": "Evidence storage is not configured.",
    "ru": "Хранилище доказательств не настроено."
  },
  "Fayl yaddaşı müvəqqəti əlçatan deyil. Yenidən yoxlayın.": {
    "az": "Fayl yaddaşı müvəqqəti əlçatan deyil. Yenidən yoxlayın.",
    "en": "File storage is temporarily unavailable. Try again.",
    "ru": "Хранилище файлов временно недоступно. Повторите позже."
  },
  "Fayl və ya məxfi yaddaş qovluğu tapılmadı.": {
    "az": "Fayl və ya məxfi yaddaş qovluğu tapılmadı.",
    "en": "File or private bucket not found.",
    "ru": "Файл или закрытое хранилище не найдено."
  },
  "Fayl yaddaşına müraciət alınmadı.": {
    "az": "Fayl yaddaşına müraciət alınmadı.",
    "en": "Could not access file storage.",
    "ru": "Не удалось обратиться к хранилищу."
  },
  "Fayl yaddaşının sazlamaları oxunmadı.": {
    "az": "Fayl yaddaşının sazlamaları oxunmadı.",
    "en": "Could not read storage settings.",
    "ru": "Не удалось прочитать настройки хранилища."
  },
  "Sübut yaddaşı məxfi (Private) olmalıdır.": {
    "az": "Sübut yaddaşı məxfi (Private) olmalıdır.",
    "en": "Evidence storage must be private.",
    "ru": "Хранилище доказательств должно быть закрытым (Private)."
  },
  "Fayl yaddaşı sazlanmayıb.": {
    "az": "Fayl yaddaşı sazlanmayıb.",
    "en": "File storage is not configured.",
    "ru": "Хранилище файлов не настроено."
  },
  "Fayl 4 MB həddini keçir.": {
    "az": "Fayl 4 MB həddini keçir.",
    "en": "The file exceeds 4 MB.",
    "ru": "Файл превышает 4 МБ."
  },
  "E-poçt təsdiqi tam tətbiqdə işləyir.": {
    "az": "E-poçt təsdiqi tam tətbiqdə işləyir.",
    "en": "Email verification is available in the live app.",
    "ru": "Подтверждение почты доступно в рабочем приложении."
  },
  "Bərpa məktubu yalnız canlı saytda göndərilir.": {
    "az": "Bərpa məktubu yalnız canlı saytda göndərilir.",
    "en": "Recovery email is sent only on the live site.",
    "ru": "Письмо восстановления отправляется только на рабочем сайте."
  },
  "Şifrə bərpası yalnız canlı saytda işləyir.": {
    "az": "Şifrə bərpası yalnız canlı saytda işləyir.",
    "en": "Password recovery works only on the live site.",
    "ru": "Восстановление пароля работает только на рабочем сайте."
  },
  "Bu, interfeys önizləməsidir. Burada real hesab yaradılmır.": {
    "az": "Bu, interfeys önizləməsidir. Burada real hesab yaradılmır.",
    "en": "This is an interface preview. No real account is created.",
    "ru": "Это предпросмотр интерфейса. Реальный аккаунт не создаётся."
  },
  "Önizləmə: real DNS və e-poçt yoxlaması aparılmır.": {
    "az": "Önizləmə: real DNS və e-poçt yoxlaması aparılmır.",
    "en": "Preview: no real DNS or email checks.",
    "ru": "Предпросмотр: DNS и почта не проверяются."
  },
  "Önizləmə: hesab məlumatları dəyişdirilmir.": {
    "az": "Önizləmə: hesab məlumatları dəyişdirilmir.",
    "en": "Preview: account details are not changed.",
    "ru": "Предпросмотр: данные аккаунта не изменяются."
  },
  "Önizləmə: hesab yaradılmır. Yuxarıdakı rol seçicisini istifadə edin.": {
    "az": "Önizləmə: hesab yaradılmır. Yuxarıdakı rol seçicisini istifadə edin.",
    "en": "Preview: no account is created. Use the role selector above.",
    "ru": "Предпросмотр: аккаунт не создаётся. Используйте выбор роли выше."
  },
  "Önizləmə: məktub göndərilmir.": {
    "az": "Önizləmə: məktub göndərilmir.",
    "en": "Preview: no email is sent.",
    "ru": "Предпросмотр: письмо не отправляется."
  },
  "Nümunə hesabat əlavə edildi; səhifə yenilənəndə silinəcək.": {
    "az": "Nümunə hesabat əlavə edildi; səhifə yenilənəndə silinəcək.",
    "en": "Sample report added; it will be removed on reload.",
    "ru": "Пример отчёта добавлен; он исчезнет при перезагрузке."
  },
  "Yerli sınaq rejimi: məktub email-outbox.log faylına yazıldı. Real e-poçt göndərilmədi.": {
    "az": "Yerli sınaq rejimi: məktub email-outbox.log faylına yazıldı. Real e-poçt göndərilmədi.",
    "en": "Local test mode: the email was written to email-outbox.log. No real email was sent.",
    "ru": "Локальный тест: письмо записано в email-outbox.log. Реальное письмо не отправлено."
  },
  "New": {
    "az": "Yeni",
    "en": "New",
    "ru": "Новый"
  },
  "Triaged": {
    "az": "Yoxlanılıb",
    "en": "Triaged",
    "ru": "Проверен"
  },
  "Resolved": {
    "az": "Həll olunub",
    "en": "Resolved",
    "ru": "Устранено"
  },
  "Duplicate": {
    "az": "Təkrar",
    "en": "Duplicate",
    "ru": "Дубликат"
  },
  "Informative": {
    "az": "Məlumat xarakterli",
    "en": "Informative",
    "ru": "Информационный"
  },
  "Not Applicable": {
    "az": "Tətbiq edilmir",
    "en": "Not applicable",
    "ru": "Неприменимо"
  },
  "Low": {
    "az": "Aşağı",
    "en": "Low",
    "ru": "Низкая"
  },
  "Medium": {
    "az": "Orta",
    "en": "Medium",
    "ru": "Средняя"
  },
  "High": {
    "az": "Yüksək",
    "en": "High",
    "ru": "Высокая"
  },
  "Critical": {
    "az": "Kritik",
    "en": "Critical",
    "ru": "Критическая"
  },
  "pending": {
    "az": "Gözləyir",
    "en": "Pending",
    "ru": "Ожидает проверки"
  },
  "approved": {
    "az": "Təsdiqlənib",
    "en": "Approved",
    "ru": "Одобрено"
  },
  "rejected": {
    "az": "Rədd edilib",
    "en": "Rejected",
    "ru": "Отклонено"
  },
  "Other": {
    "az": "Digər",
    "en": "Other",
    "ru": "Другое"
  },
  "Sign in required.": {
    "az": "Daxil olmaq tələb olunur.",
    "en": "Sign in required.",
    "ru": "Необходимо войти."
  },
  "Invalid or expired session.": {
    "az": "Sessiya etibarsızdır və ya vaxtı bitib.",
    "en": "Invalid or expired session.",
    "ru": "Сеанс недействителен или истёк."
  },
  "This action is not available for your role.": {
    "az": "Rolunuz bu əməliyyata icazə vermir.",
    "en": "This action is not available for your role.",
    "ru": "Это действие недоступно для вашей роли."
  },
  "Company not found.": {
    "az": "Şirkət tapılmadı.",
    "en": "Company not found.",
    "ru": "Компания не найдена."
  },
  "Your company must be approved before creating programs.": {
    "az": "Proqram yaratmazdan əvvəl şirkət təsdiqlənməlidir.",
    "en": "Your company must be approved before creating programs.",
    "ru": "Перед созданием программ компания должна быть одобрена."
  },
  "Active program not found.": {
    "az": "Aktiv proqram tapılmadı.",
    "en": "Active program not found.",
    "ru": "Активная программа не найдена."
  },
  "Program not found.": {
    "az": "Proqram tapılmadı.",
    "en": "Program not found.",
    "ru": "Программа не найдена."
  },
  "Report not found.": {
    "az": "Hesabat tapılmadı.",
    "en": "Report not found.",
    "ru": "Отчёт не найден."
  },
  "Invalid status transition. Triage new reports before resolving them.": {
    "az": "Status keçidi yanlışdır. Həll etməzdən əvvəl hesabatı yoxlayın.",
    "en": "Invalid status transition. Triage new reports before resolving them.",
    "ru": "Недопустимый переход статуса. Сначала проверьте новый отчёт."
  },
  "Please record a mediation note for this change.": {
    "az": "Bu dəyişiklik üçün baxış qeydi yazın.",
    "en": "Please record a mediation note for this change.",
    "ru": "Укажите примечание к этому изменению."
  },
  "The report changed. Refresh and try again.": {
    "az": "Hesabat dəyişib. Səhifəni yeniləyib təkrar yoxlayın.",
    "en": "The report changed. Refresh and try again.",
    "ru": "Отчёт изменился. Обновите страницу и повторите."
  },
  "Email or handle already registered.": {
    "az": "E-poçt və ya istifadəçi adı artıq qeydiyyatdadır.",
    "en": "Email or username already registered.",
    "ru": "Почта или имя пользователя уже зарегистрированы."
  },
  "Verify your email before signing in.": {
    "az": "Girişdən əvvəl e-poçtunuzu təsdiqləyin.",
    "en": "Verify your email before signing in.",
    "ru": "Подтвердите почту перед входом."
  },
  "This verification link is invalid or expired. Request a new one.": {
    "az": "Təsdiq keçidi etibarsızdır və ya vaxtı bitib. Yenisini istəyin.",
    "en": "This verification link is invalid or expired. Request a new one.",
    "ru": "Ссылка недействительна или истекла. Запросите новую."
  },
  "This link has already been used.": {
    "az": "Bu keçid artıq istifadə olunub.",
    "en": "This link has already been used.",
    "ru": "Эта ссылка уже использована."
  },
  "Only resolved cash rewards can be marked paid.": {
    "az": "Yalnız həll olunmuş pul mükafatı ödənilmiş sayıla bilər.",
    "en": "Only resolved cash rewards can be marked paid.",
    "ru": "Выплаченными можно отметить только денежные награды по закрытым отчётам."
  },
  "Attachment not found.": {
    "az": "Sübut faylı tapılmadı.",
    "en": "Attachment not found.",
    "ru": "Вложение не найдено."
  },
  "Only .pdf and .txt files are accepted.": {
    "az": "Yalnız PDF və TXT faylları qəbul edilir.",
    "en": "Only .pdf and .txt files are accepted.",
    "ru": "Принимаются только файлы PDF и TXT."
  },
  "TXT evidence must be UTF-8 plain text.": {
    "az": "TXT faylı UTF-8 mətn formatında olmalıdır.",
    "en": "TXT evidence must be UTF-8 plain text.",
    "ru": "TXT-файл должен содержать текст UTF-8."
  },
  "Invalid PDF file.": {
    "az": "PDF faylı etibarsızdır.",
    "en": "Invalid PDF file.",
    "ru": "Некорректный PDF-файл."
  },
  "Use a readable, unencrypted PDF without scripts, forms or interactive annotations.": {
    "az": "Skriptsiz, formasız və şifrələnməmiş PDF istifadə edin.",
    "en": "Use a readable, unencrypted PDF without scripts, forms or interactive annotations.",
    "ru": "Используйте читаемый PDF без шифрования, скриптов, форм и интерактивных аннотаций."
  },
  "Disposable email addresses are not accepted.": {
    "az": "Müvəqqəti e-poçt ünvanları qəbul edilmir.",
    "en": "Disposable email addresses are not accepted.",
    "ru": "Временные почтовые адреса не принимаются."
  },
  "This domain does not accept email.": {
    "az": "Bu domen e-poçt qəbul etmir.",
    "en": "This domain does not accept email.",
    "ru": "Этот домен не принимает почту."
  },
  "This domain has no mail server.": {
    "az": "Bu domenin poçt serveri yoxdur.",
    "en": "This domain has no mail server.",
    "ru": "У домена нет почтового сервера."
  },
  "Email domain verification is temporarily unavailable. Try again.": {
    "az": "E-poçt domeninin yoxlanması müvəqqəti mümkün deyil. Yenidən yoxlayın.",
    "en": "Email domain verification is temporarily unavailable. Try again.",
    "ru": "Проверка почтового домена временно недоступна. Повторите позже."
  },
  "Company contact must verify their email first.": {
    "az": "Şirkət əlaqə ünvanı əvvəlcə təsdiqlənməlidir.",
    "en": "Company contact must verify their email first.",
    "ru": "Сначала подтвердите почту компании."
  },
  "Approve the company first.": {
    "az": "Əvvəl şirkəti təsdiqləyin.",
    "en": "Approve the company first.",
    "ru": "Сначала одобрите компанию."
  },
  "Request is too large.": {
    "az": "Sorğunun ölçüsü çox böyükdür.",
    "en": "Request is too large.",
    "ru": "Слишком большой запрос."
  },
  "Invalid request length.": {
    "az": "Sorğunun ölçüsü etibarsızdır.",
    "en": "Invalid request length.",
    "ru": "Неверный размер запроса."
  },
  "Cross-origin requests are not allowed.": {
    "az": "Başqa saytdan göndərilən sorğulara icazə verilmir.",
    "en": "Cross-origin requests are not allowed.",
    "ru": "Запросы с другого сайта запрещены."
  },
  "Ana səhifə": {
    "az": "Ana səhifə",
    "en": "Home",
    "ru": "Главная"
  },
  "TƏHLÜKƏSİZLİK BİRLİKDƏ BAŞLAYIR": {
    "az": "TƏHLÜKƏSİZLİK BİRLİKDƏ BAŞLAYIR",
    "en": "SECURITY STARTS TOGETHER",
    "ru": "БЕЗОПАСНОСТЬ НАЧИНАЕТСЯ ВМЕСТЕ"
  },
  "Zəifliyi tap.": {
    "az": "Zəifliyi tap.",
    "en": "Find the weakness.",
    "ru": "Найди уязвимость."
  },
  "Güvəni gücləndir.": {
    "az": "Güvəni gücləndir.",
    "en": "Build stronger trust.",
    "ru": "Укрепи доверие."
  },
  "BugCasp şirkətləri və təhlükəsizlik tədqiqatçılarını bir araya gətirən bug bounty platformasıdır. Tapıntıları məsuliyyətlə paylaşın, rəqəmsal dünyanı daha təhlükəsiz edin.": {
    "az": "BugCasp şirkətləri və təhlükəsizlik tədqiqatçılarını bir araya gətirən bug bounty platformasıdır. Tapıntıları məsuliyyətlə paylaşın, rəqəmsal dünyanı daha təhlükəsiz edin.",
    "en": "BugCasp is a bug bounty platform connecting companies with security researchers. Share findings responsibly and make the digital world safer.",
    "ru": "BugCasp — платформа bug bounty, объединяющая компании и исследователей безопасности. Ответственно сообщайте об уязвимостях и делайте цифровой мир безопаснее."
  },
  "Tədqiqatçı kimi qoşul": {
    "az": "Tədqiqatçı kimi qoşul",
    "en": "Join as a researcher",
    "ru": "Стать исследователем"
  },
  "Şirkətimi qorumaq istəyirəm": {
    "az": "Şirkətimi qorumaq istəyirəm",
    "en": "Protect my company",
    "ru": "Защитить компанию"
  },
  "Proqramları araşdır": {
    "az": "Proqramları araşdır",
    "en": "Explore programs",
    "ru": "Изучить программы"
  },
  "Tapıntı": {
    "az": "Tapıntı",
    "en": "Finding",
    "ru": "Находка"
  },
  "Təsdiq": {
    "az": "Təsdiq",
    "en": "Validation",
    "ru": "Проверка"
  },
  "Mükafat": {
    "az": "Mükafat",
    "en": "Reward",
    "ru": "Награда"
  },
  "İnsan bacarığı. Daha güclü müdafiə.": {
    "az": "İnsan bacarığı. Daha güclü müdafiə.",
    "en": "Human expertise. Stronger defense.",
    "ru": "Опыт людей. Более сильная защита."
  },
  "İcazəli araşdırma": {
    "az": "İcazəli araşdırma",
    "en": "Authorized research",
    "ru": "Разрешённые исследования"
  },
  "Məxfi hesabatlar": {
    "az": "Məxfi hesabatlar",
    "en": "Private reports",
    "ru": "Конфиденциальные отчёты"
  },
  "Şəffaf qiymətləndirmə": {
    "az": "Şəffaf qiymətləndirmə",
    "en": "Transparent review",
    "ru": "Прозрачная оценка"
  },
  "BİZ KİMİK?": {
    "az": "BİZ KİMİK?",
    "en": "WHO WE ARE",
    "ru": "КТО МЫ"
  },
  "Təhlükəsizliyə ortaq töhfə.": {
    "az": "Təhlükəsizliyə ortaq töhfə.",
    "en": "A shared commitment to security.",
    "ru": "Общий вклад в безопасность."
  },
  "Bir tərəfdə qorunmalı məhsullar, digər tərəfdə zəiflikləri görə bilən insanlar. BugCasp bu əməkdaşlıq üçün ortaq məkan yaradır.": {
    "az": "Bir tərəfdə qorunmalı məhsullar, digər tərəfdə zəiflikləri görə bilən insanlar. BugCasp bu əməkdaşlıq üçün ortaq məkan yaradır.",
    "en": "Products that need protecting. People who can spot their weaknesses. BugCasp gives them a place to work together.",
    "ru": "Продукты, которым нужна защита, и люди, способные найти их слабые места. BugCasp создаёт пространство для их сотрудничества."
  },
  "Bacarığını real təsirə çevir.": {
    "az": "Bacarığını real təsirə çevir.",
    "en": "Turn your skills into real impact.",
    "ru": "Преврати навыки в результат."
  },
  "İcazəli proqramları seç, qaydaları oxu və tapdığın zəifliyi sübut faylı ilə bildir. Təsdiqlənmiş hesabatlarla reputasiya və proqramın şərtlərinə uyğun mükafat qazan.": {
    "az": "İcazəli proqramları seç, qaydaları oxu və tapdığın zəifliyi sübut faylı ilə bildir. Təsdiqlənmiş hesabatlarla reputasiya və proqramın şərtlərinə uyğun mükafat qazan.",
    "en": "Choose authorized programs, read the rules and submit findings with evidence. Earn reputation and rewards for validated reports under each program’s terms.",
    "ru": "Выбирай разрешённые программы, читай правила и отправляй отчёты с доказательствами. Получай репутацию и награды за подтверждённые отчёты по условиям программы."
  },
  "Tədqiqatçı hesabı yarat": {
    "az": "Tədqiqatçı hesabı yarat",
    "en": "Create a researcher account",
    "ru": "Создать аккаунт исследователя"
  },
  "Məhsuluna yeni gözlə bax.": {
    "az": "Məhsuluna yeni gözlə bax.",
    "en": "See your product with fresh eyes.",
    "ru": "Взгляни на продукт по-новому."
  },
  "Proqramını yarat, araşdırma sərhədlərini və mükafatları müəyyən et. Gələn hesabatları bir yerdə yoxla, qiymətləndir və həll prosesini idarə et.": {
    "az": "Proqramını yarat, araşdırma sərhədlərini və mükafatları müəyyən et. Gələn hesabatları bir yerdə yoxla, qiymətləndir və həll prosesini idarə et.",
    "en": "Create a program, define its scope and set rewards. Review incoming reports in one place and manage them through resolution.",
    "ru": "Создай программу, определи границы исследования и награды. Проверяй отчёты в одном месте и управляй процессом устранения уязвимостей."
  },
  "Şirkət hesabı yarat": {
    "az": "Şirkət hesabı yarat",
    "en": "Create a company account",
    "ru": "Создать аккаунт компании"
  },
  "NECƏ İŞLƏYİR?": {
    "az": "NECƏ İŞLƏYİR?",
    "en": "HOW IT WORKS",
    "ru": "КАК ЭТО РАБОТАЕТ"
  },
  "Tapıntıdan həllə, üç addım.": {
    "az": "Tapıntıdan həllə, üç addım.",
    "en": "From finding to fix in three steps.",
    "ru": "От находки до решения за три шага."
  },
  "Proqramı seç": {
    "az": "Proqramı seç",
    "en": "Choose a program",
    "ru": "Выбери программу"
  },
  "Hədəfləri, icazə verilən testləri və proqramın qaydalarını öyrən.": {
    "az": "Hədəfləri, icazə verilən testləri və proqramın qaydalarını öyrən.",
    "en": "Review the targets, permitted tests and program rules.",
    "ru": "Изучи цели, разрешённые тесты и правила программы."
  },
  "Hesabatını göndər": {
    "az": "Hesabatını göndər",
    "en": "Submit your report",
    "ru": "Отправь отчёт"
  },
  "Tapıntını adlandır, kateqoriyanı seç və sübut faylını əlavə et.": {
    "az": "Tapıntını adlandır, kateqoriyanı seç və sübut faylını əlavə et.",
    "en": "Name your finding, choose a category and attach your evidence.",
    "ru": "Назови находку, выбери категорию и приложи доказательства."
  },
  "Nəticəni izlə": {
    "az": "Nəticəni izlə",
    "en": "Track the outcome",
    "ru": "Следи за результатом"
  },
  "Şirkətin baxışını, hesabatın statusunu və təsdiqlənmiş mükafatını hesabından izlə.": {
    "az": "Şirkətin baxışını, hesabatın statusunu və təsdiqlənmiş mükafatını hesabından izlə.",
    "en": "Follow the company’s review, report status and approved reward from your account.",
    "ru": "Отслеживай проверку компанией, статус отчёта и подтверждённую награду в аккаунте."
  },
  "NÖVBƏTİ ADDIM SƏNİNDİR": {
    "az": "NÖVBƏTİ ADDIM SƏNİNDİR",
    "en": "YOUR NEXT MOVE",
    "ru": "СЛЕДУЮЩИЙ ШАГ ЗА ТОБОЙ"
  },
  "Daha təhlükəsiz gələcəyə qoşul.": {
    "az": "Daha təhlükəsiz gələcəyə qoşul.",
    "en": "Be part of a safer future.",
    "ru": "Стань частью безопасного будущего."
  },
  "İstər zəiflikləri tap, istər məhsulunu qoru.": {
    "az": "İstər zəiflikləri tap, istər məhsulunu qoru.",
    "en": "Find vulnerabilities or protect your product.",
    "ru": "Находи уязвимости или защищай свой продукт."
  },
  "İndi hesab yarat": {
    "az": "İndi hesab yarat",
    "en": "Create your account",
    "ru": "Создать аккаунт"
  },
  "Profilim": {
    "az": "Profilim",
    "en": "My profile",
    "ru": "Мой профиль"
  },
  "ŞƏXSİ PROFİL": {
    "az": "ŞƏXSİ PROFİL",
    "en": "PERSONAL PROFILE",
    "ru": "ЛИЧНЫЙ ПРОФИЛЬ"
  },
  "Haqqınızda məlumatı və profil keçidlərinizi yeniləyin.": {
    "az": "Haqqınızda məlumatı və profil keçidlərinizi yeniləyin.",
    "en": "Update your bio and profile links.",
    "ru": "Обновите информацию о себе и ссылки на профили."
  },
  "Profili saxla": {
    "az": "Profili saxla",
    "en": "Save profile",
    "ru": "Сохранить профиль"
  },
  "İstifadəçi adını və şifrəni hesab sazlamalarında dəyişə bilərsiniz.": {
    "az": "İstifadəçi adını və şifrəni hesab sazlamalarında dəyişə bilərsiniz.",
    "en": "Change your username and password in account settings.",
    "ru": "Изменить имя пользователя и пароль можно в настройках аккаунта."
  },
  "3–40 simvol: latın hərfləri, rəqəmlər, _ və -.": {
    "az": "3–40 simvol: latın hərfləri, rəqəmlər, _ və -.",
    "en": "3–40 characters: Latin letters, numbers, _ and -.",
    "ru": "3–40 символов: латинские буквы, цифры, _ и -."
  },
  "İstifadəçi adı yoxlanılır…": {
    "az": "İstifadəçi adı yoxlanılır…",
    "en": "Checking username…",
    "ru": "Проверяем имя пользователя…"
  },
  "Bu istifadəçi adı uyğundur.": {
    "az": "Bu istifadəçi adı uyğundur.",
    "en": "This username is available.",
    "ru": "Это имя пользователя доступно."
  },
  "Ad yoxlanmadı. Saxlayarkən yenidən yoxlanacaq.": {
    "az": "Ad yoxlanmadı. Saxlayarkən yenidən yoxlanacaq.",
    "en": "Could not check the name. It will be checked when you save.",
    "ru": "Не удалось проверить имя. Оно будет проверено при сохранении."
  },
  "Tədqiqatçı hesabı tələb olunur.": {
    "az": "Tədqiqatçı hesabı tələb olunur.",
    "en": "A researcher account is required.",
    "ru": "Требуется аккаунт исследователя."
  },
  "Profil yeniləndi.": {
    "az": "Profil yeniləndi.",
    "en": "Profile updated.",
    "ru": "Профиль обновлён."
  },
  "Önizləmə: dəyişikliklər səhifə yenilənənədək saxlanılır.": {
    "az": "Önizləmə: dəyişikliklər səhifə yenilənənədək saxlanılır.",
    "en": "Preview: changes last until the page is reloaded.",
    "ru": "Предпросмотр: изменения сохраняются до перезагрузки страницы."
  },
  "Admin bölmələri": {
    "az": "Admin bölmələri",
    "en": "Admin sections",
    "ru": "Разделы администратора"
  },
  "İcmal": {
    "az": "İcmal",
    "en": "Overview",
    "ru": "Обзор"
  },
  "İstifadəçilər": {
    "az": "İstifadəçilər",
    "en": "Users",
    "ru": "Пользователи"
  },
  "Statistika": {
    "az": "Statistika",
    "en": "Statistics",
    "ru": "Статистика"
  },
  "Mübahisələr": {
    "az": "Mübahisələr",
    "en": "Disputes",
    "ru": "Споры"
  },
  "Əməliyyat tarixçəsi": {
    "az": "Əməliyyat tarixçəsi",
    "en": "Activity history",
    "ru": "История действий"
  },
  "Bildiriş mərkəzi": {
    "az": "Bildiriş mərkəzi",
    "en": "Notifications",
    "ru": "Уведомления"
  },
  "Sayt elanları": {
    "az": "Sayt elanları",
    "en": "Site announcements",
    "ru": "Объявления сайта"
  },
  "Proqram nəzarəti": {
    "az": "Proqram nəzarəti",
    "en": "Program controls",
    "ru": "Управление программами"
  },
  "Şirkət loqosu": {
    "az": "Şirkət loqosu",
    "en": "Company logo",
    "ru": "Логотип компании"
  },
  "Profil şəkli": {
    "az": "Profil şəkli",
    "en": "Profile picture",
    "ru": "Фото профиля"
  },
  "JPG, PNG və WebP · maksimum 2 MB. Şəkil ictimai görünəcək.": {
    "az": "JPG, PNG və WebP · maksimum 2 MB. Şəkil ictimai görünəcək.",
    "en": "JPG, PNG and WebP · up to 2 MB. The image will be public.",
    "ru": "JPG, PNG и WebP · до 2 МБ. Изображение будет общедоступным."
  },
  "Şəkil seçin": {
    "az": "Şəkil seçin",
    "en": "Choose an image",
    "ru": "Выберите изображение"
  },
  "Şəkli yüklə": {
    "az": "Şəkli yüklə",
    "en": "Upload image",
    "ru": "Загрузить изображение"
  },
  "Şəkli sil": {
    "az": "Şəkli sil",
    "en": "Remove image",
    "ru": "Удалить изображение"
  },
  "Məlumat yoxdur.": {
    "az": "Məlumat yoxdur.",
    "en": "No records found.",
    "ru": "Записей нет."
  },
  "Əvvəlki": {
    "az": "Əvvəlki",
    "en": "Previous",
    "ru": "Предыдущая"
  },
  "Növbəti": {
    "az": "Növbəti",
    "en": "Next",
    "ru": "Следующая"
  },
  "Axtarış": {
    "az": "Axtarış",
    "en": "Search",
    "ru": "Поиск"
  },
  "Bütün rollar": {
    "az": "Bütün rollar",
    "en": "All roles",
    "ru": "Все роли"
  },
  "Axtar": {
    "az": "Axtar",
    "en": "Search",
    "ru": "Найти"
  },
  "Bu əməliyyat üçün canlı hesabla daxil olun.": {
    "az": "Bu əməliyyat üçün canlı hesabla daxil olun.",
    "en": "Sign in to a live account for this action.",
    "ru": "Для этого действия войдите в настоящий аккаунт."
  },
  "İstifadəçi": {
    "az": "İstifadəçi",
    "en": "User",
    "ru": "Пользователь"
  },
  "Vəziyyət": {
    "az": "Vəziyyət",
    "en": "State",
    "ru": "Состояние"
  },
  "Əməliyyat": {
    "az": "Əməliyyat",
    "en": "Action",
    "ru": "Действие"
  },
  "Bloklanıb": {
    "az": "Bloklanıb",
    "en": "Blocked",
    "ru": "Заблокирован"
  },
  "Profilə bax": {
    "az": "Profilə bax",
    "en": "View profile",
    "ru": "Посмотреть профиль"
  },
  "Bloku aç": {
    "az": "Bloku aç",
    "en": "Unblock",
    "ru": "Разблокировать"
  },
  "Blokla": {
    "az": "Blokla",
    "en": "Block",
    "ru": "Заблокировать"
  },
  "Admin dayandırıb": {
    "az": "Admin dayandırıb",
    "en": "Suspended by admin",
    "ru": "Приостановлено администратором"
  },
  "Məhdudiyyəti qaldır": {
    "az": "Məhdudiyyəti qaldır",
    "en": "Lift restriction",
    "ru": "Снять ограничение"
  },
  "Tarix": {
    "az": "Tarix",
    "en": "Date",
    "ru": "Дата"
  },
  "Obyekt": {
    "az": "Obyekt",
    "en": "Subject",
    "ru": "Объект"
  },
  "Başlanğıc tarixi": {
    "az": "Başlanğıc tarixi",
    "en": "Start date",
    "ru": "Начальная дата"
  },
  "Son tarix": {
    "az": "Son tarix",
    "en": "End date",
    "ru": "Конечная дата"
  },
  "Filtrlə": {
    "az": "Filtrlə",
    "en": "Filter",
    "ru": "Фильтровать"
  },
  "Sıfırla": {
    "az": "Sıfırla",
    "en": "Reset",
    "ru": "Сбросить"
  },
  "Tarix filtri qeydlərin yaradılma tarixinə görə tətbiq olunur (UTC). Statuslar cari vəziyyəti göstərir.": {
    "az": "Tarix filtri qeydlərin yaradılma tarixinə görə tətbiq olunur (UTC). Statuslar cari vəziyyəti göstərir.",
    "en": "Dates filter records by creation time (UTC). Statuses reflect their current state.",
    "ru": "Даты фильтруют записи по времени создания (UTC). Статусы отражают текущее состояние."
  },
  "Şirkətlər": {
    "az": "Şirkətlər",
    "en": "Companies",
    "ru": "Компании"
  },
  "Hesabatlar": {
    "az": "Hesabatlar",
    "en": "Reports",
    "ru": "Отчёты"
  },
  "Gözləyən şirkətlər": {
    "az": "Gözləyən şirkətlər",
    "en": "Pending companies",
    "ru": "Ожидающие компании"
  },
  "Gözləyən proqramlar": {
    "az": "Gözləyən proqramlar",
    "en": "Pending programs",
    "ru": "Ожидающие программы"
  },
  "Seçilmiş hesabatlar üzrə": {
    "az": "Seçilmiş hesabatlar üzrə",
    "en": "For selected reports",
    "ru": "По выбранным отчётам"
  },
  "Gözləyən işlər": {
    "az": "Gözləyən işlər",
    "en": "Pending tasks",
    "ru": "Ожидающие задачи"
  },
  "Qərar verilən müraciətlər siyahıdan avtomatik çıxır.": {
    "az": "Qərar verilən müraciətlər siyahıdan avtomatik çıxır.",
    "en": "Handled requests leave this list automatically.",
    "ru": "Обработанные заявки автоматически исчезают из списка."
  },
  "Admin baxışı tələb olunur": {
    "az": "Admin baxışı tələb olunur",
    "en": "Admin review required",
    "ru": "Требуется проверка администратора"
  },
  "Yenilə": {
    "az": "Yenilə",
    "en": "Refresh",
    "ru": "Обновить"
  },
  "Açıq": {
    "az": "Açıq",
    "en": "Open",
    "ru": "Открыт"
  },
  "Bağlanmış": {
    "az": "Bağlanmış",
    "en": "Closed",
    "ru": "Закрыт"
  },
  "Yeni elan": {
    "az": "Yeni elan",
    "en": "New announcement",
    "ru": "Новое объявление"
  },
  "Başlıq": {
    "az": "Başlıq",
    "en": "Title",
    "ru": "Заголовок"
  },
  "Yayımlanıb": {
    "az": "Yayımlanıb",
    "en": "Published",
    "ru": "Опубликовано"
  },
  "Qaralama": {
    "az": "Qaralama",
    "en": "Draft",
    "ru": "Черновик"
  },
  "Redaktə et": {
    "az": "Redaktə et",
    "en": "Edit",
    "ru": "Редактировать"
  },
  "Blok müddəti (gün)": {
    "az": "Blok müddəti (gün)",
    "en": "Block duration (days)",
    "ru": "Срок блокировки (дней)"
  },
  "İstifadəçini blokla": {
    "az": "İstifadəçini blokla",
    "en": "Block user",
    "ru": "Заблокировать пользователя"
  },
  "Proqramı dayandır": {
    "az": "Proqramı dayandır",
    "en": "Suspend program",
    "ru": "Приостановить программу"
  },
  "Səbəb": {
    "az": "Səbəb",
    "en": "Reason",
    "ru": "Причина"
  },
  "Sayt elanı": {
    "az": "Sayt elanı",
    "en": "Site announcement",
    "ru": "Объявление сайта"
  },
  "Mətn": {
    "az": "Mətn",
    "en": "Text",
    "ru": "Текст"
  },
  "Saytda göstər": {
    "az": "Saytda göstər",
    "en": "Show on site",
    "ru": "Показывать на сайте"
  },
  "Yadda saxla": {
    "az": "Yadda saxla",
    "en": "Save",
    "ru": "Сохранить"
  },
  "Hesabat müzakirəsi": {
    "az": "Hesabat müzakirəsi",
    "en": "Report discussion",
    "ru": "Обсуждение отчёта"
  },
  "İzahınız": {
    "az": "İzahınız",
    "en": "Your explanation",
    "ru": "Ваше пояснение"
  },
  "Hələ mesaj yoxdur.": {
    "az": "Hələ mesaj yoxdur.",
    "en": "No messages yet.",
    "ru": "Сообщений пока нет."
  },
  "İstifadəçi profili": {
    "az": "İstifadəçi profili",
    "en": "User profile",
    "ru": "Профиль пользователя"
  },
  "E-poçt təsdiqlənib": {
    "az": "E-poçt təsdiqlənib",
    "en": "Email verified",
    "ru": "Почта подтверждена"
  },
  "E-poçt təsdiqlənməyib": {
    "az": "E-poçt təsdiqlənməyib",
    "en": "Email unverified",
    "ru": "Почта не подтверждена"
  },
  "Mübahisəni bağla": {
    "az": "Mübahisəni bağla",
    "en": "Close dispute",
    "ru": "Закрыть спор"
  },
  "Qərar və əsaslandırma": {
    "az": "Qərar və əsaslandırma",
    "en": "Decision and reasoning",
    "ru": "Решение и обоснование"
  },
  "Bu qərar tərəflərə görünəcək. Hesabat statusu ayrıca dəyişdirilir.": {
    "az": "Bu qərar tərəflərə görünəcək. Hesabat statusu ayrıca dəyişdirilir.",
    "en": "Both parties will see this decision. Report status is changed separately.",
    "ru": "Обе стороны увидят это решение. Статус отчёта изменяется отдельно."
  },
  "Şəkil boş olmamalı və 2 MB həddini keçməməlidir.": {
    "az": "Şəkil boş olmamalı və 2 MB həddini keçməməlidir.",
    "en": "The image must not be empty or exceed 2 MB.",
    "ru": "Изображение не должно быть пустым или превышать 2 МБ."
  },
  "Şəkil yeniləndi.": {
    "az": "Şəkil yeniləndi.",
    "en": "Image updated.",
    "ru": "Изображение обновлено."
  },
  "Şirkət portalında yüklədiyiniz loqo proqramın başlığında görünür.": {
    "az": "Şirkət portalında yüklədiyiniz loqo proqramın başlığında görünür.",
    "en": "The logo uploaded in the company portal appears in the program header.",
    "ru": "Логотип из кабинета компании отображается в заголовке программы."
  },
  "Şirkətin izahı": {
    "az": "Şirkətin izahı",
    "en": "Company explanation",
    "ru": "Пояснение компании"
  },
  "Müzakirə və izahlar": {
    "az": "Müzakirə və izahlar",
    "en": "Discussion and explanations",
    "ru": "Обсуждение и пояснения"
  },
  "JPG, PNG və ya WebP şəkli seçin (maksimum 16 meqapiksel).": {
    "az": "JPG, PNG və ya WebP şəkli seçin (maksimum 16 meqapiksel).",
    "en": "Choose a JPG, PNG or WebP image (up to 16 megapixels).",
    "ru": "Выберите JPG, PNG или WebP (до 16 мегапикселей)."
  },
  "Şəkil tapılmadı.": {
    "az": "Şəkil tapılmadı.",
    "en": "Image not found.",
    "ru": "Изображение не найдено."
  },
  "İstifadəçi tapılmadı.": {
    "az": "İstifadəçi tapılmadı.",
    "en": "User not found.",
    "ru": "Пользователь не найден."
  },
  "Admin hesabı bloklana bilməz.": {
    "az": "Admin hesabı bloklana bilməz.",
    "en": "Admin accounts cannot be blocked.",
    "ru": "Аккаунт администратора нельзя заблокировать."
  },
  "Proqram admin tərəfindən dayandırılıb.": {
    "az": "Proqram admin tərəfindən dayandırılıb.",
    "en": "The program was suspended by an admin.",
    "ru": "Программа приостановлена администратором."
  },
  "Tarix aralığı yanlışdır.": {
    "az": "Tarix aralığı yanlışdır.",
    "en": "Invalid date range.",
    "ru": "Неверный диапазон дат."
  },
  "Mübahisə artıq bağlanıb.": {
    "az": "Mübahisə artıq bağlanıb.",
    "en": "The dispute is already closed.",
    "ru": "Спор уже закрыт."
  },
  "Elan tapılmadı.": {
    "az": "Elan tapılmadı.",
    "en": "Announcement not found.",
    "ru": "Объявление не найдено."
  },
  "Hesab müvəqqəti bloklanıb:": {
    "az": "Hesab müvəqqəti bloklanıb:",
    "en": "Account temporarily blocked:",
    "ru": "Аккаунт временно заблокирован:"
  }
};

const supported = ['az','en','ru'];
const key = 'bugcasp-language';
let language = 'az';
try { const saved = localStorage.getItem(key); if (supported.includes(saved)) language = saved; } catch (_) {}
document.documentElement.lang = language;
const originals = new WeakMap();
const attributes = new WeakMap();
const escapeRegex = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
// Replace original UI phrases once, longest first; never translate user-authored content.
const pattern = new RegExp('(?<![\\p{L}\\p{N}_])(' + Object.keys(messages).sort((a,b)=>b.length-a.length).map(escapeRegex).join('|') + ')(?![\\p{L}\\p{N}_])', 'gu');
function translate(source) { return source.replace(pattern, match => messages[match][language]); }
function skip(element) { return !element || element.closest('[translate="no"],script,style,textarea,pre,code,svg'); }
function translateText(node) {
  if (skip(node.parentElement)) return;
  const current = node.nodeValue;
  let record = originals.get(node);
  if (!record || current !== record.rendered) record = {source:current};
  const result = translate(record.source);
  if (current !== result) node.nodeValue = result;
  record.rendered = result; originals.set(node,record);
}
function translateAttributes(element) {
  if (skip(element)) return;
  let records = attributes.get(element);
  if (!records) { records = {}; attributes.set(element,records); }
  for (const name of ['placeholder','aria-label','title','alt']) {
    const current = element.getAttribute(name);
    if (current === null) { delete records[name]; continue; }
    let record = records[name];
    if (!record || current !== record.rendered) record = {source:current};
    const result = translate(record.source);
    if (current !== result) element.setAttribute(name,result);
    record.rendered = result; records[name] = record;
  }
}
let observer;
function refresh() {
  if (!document.body) return;
  observer?.disconnect();
  const walker = document.createTreeWalker(document.documentElement, NodeFilter.SHOW_TEXT);
  let node; while ((node = walker.nextNode())) translateText(node);
  document.querySelectorAll('[placeholder],[aria-label],[title],[alt]').forEach(translateAttributes);
  document.querySelectorAll('[data-language-select]').forEach(selector=>{selector.value=language;});
  observer?.observe(document.documentElement,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['placeholder','aria-label','title','alt']});
}
function setLanguage(value,save=true) {
  if (!supported.includes(value)) return;
  // Flush any pending UI mutations before switching languages.
  language = value; document.documentElement.lang = value;
  if (save) try { localStorage.setItem(key,value); } catch (_) {}
  refresh();
}
window.BugCaspI18n = {translate,setLanguage,get language(){return language;}};
document.addEventListener('DOMContentLoaded',()=>{
  observer = new MutationObserver(refresh);
  document.addEventListener('change',event=>{if(event.target.matches('[data-language-select]'))setLanguage(event.target.value);});
  refresh();
});
window.addEventListener('storage',event=>{
  if (event.key === key || event.key === null) setLanguage(supported.includes(event.newValue)?event.newValue:'az',false);
});
})();
