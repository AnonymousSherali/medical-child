# NeuroMonitor - Yangi tug'ilganlar neyrodiagnostika tizimi

## Loyiha haqida

NeuroMonitor - chala tug'ilgan yangi tug'ilgan chaqaloqlarda markaziy asab tizimining perinatal shikastlanishlarini diagnostika qilishda neyro-spetsifik oqsillarning klinik ahamiyatini o'rganish va monitoring qilish uchun mo'ljallangan tibbiy axborot tizimi.

## Maqsad

Chala tug'ilgan yangi tug'ilganlar markaziy asab tizimidagi perinatal shikastlanishlarni erta aniqlash va monitoring qilish uchun zamonaviy raqamli platforma yaratish, neyro-spetsifik oqsillar (NSE, S100B va boshqalar) ko'rsatkichlarini kuzatish va tahlil qilish.

## Asosiy imkoniyatlar

### 1. Bemor ma'lumotlarini boshqarish
- Yangi tug'ilganlarni ro'yxatga olish (karta raqami, jinsi, tug'ilgan sana)
- Tug'ilish parametrlari: gestatsion yoshi, og'irligi, bo'yi, bosh aylanasi, Apgar
- Ona ma'lumotlari va tibbiy tarix yuritish
- Ism, familiya, karta raqami bo'yicha qidiruv va status filtri
- Chala tug'ilganlarni avtomatik belgilash (< 37 hafta)

### 2. Monitoring tizimi
- Bemor uchun monitoring sessiyasini boshlash va yakunlash
- Hayotiy ko'rsatkichlar: yurak urishi, nafas olish, harorat, qon bosimi, SpO2
- Nevrologik baholash: ong darajasi, mushak tonusi, reflekslar, tutqanoq faolligi
- Kiritilgan qiymatlarni fiziologik chegaralar bo'yicha tekshirish

### 3. Laboratoriya
- Tahlil buyurtmalarini yaratish va holatini kuzatish
- Neyro-spetsifik oqsillar natijalari: NSE, S100B, GFAP
- Me'yoriy diapazon asosida chetlashishni avtomatik aniqlash
- Qon tahlili ko'rsatkichlari: Hb, RBC, WBC, PLT, glyukoza, kreatinin, bilirubin
- Tur va holat bo'yicha filtrlash

### 4. Analitika va hisobotlar
- Umumiy ko'rsatkichlar: bemorlar, tahlillar, chetlashgan natijalar, faol monitoring
- Klinik o'rtachalar: gestatsion yosh, tug'ilish og'irligi, chala tug'ilganlar soni
- Neyro-oqsillar bo'yicha taqsimot va chetlashish ulushi
- CSV eksport (Excel'da ochiladi): bemorlar va neyro-oqsil natijalari

### 5. Foydalanuvchilar va xavfsizlik
- Rolga asoslangan hisoblar: shifokor, hamshira, laborant, administrator
- Barcha sahifalar autentifikatsiya talab qiladi
- CSRF, XSS va SQL injection himoyasi (Django standart mexanizmlari)
- Admin panel barcha modellar uchun sozlangan

### Rejadagi imkoniyatlar (hozircha amalga oshirilmagan)
- PDF formatda hisobot generatsiyasi
- Grafik/diagrammalar (Chart.js)
- Celery orqali fon vazifalari va avtomatik ogohlantirishlar
- Sun'iy intellekt asosida xavf darajasini prognozlash
- Laboratoriya tizimlaridan avtomatik import (REST API)

## Texnologiyalar

### Hozirda ishlatilayotgan
- **Django 4.2** - asosiy web framework
- **SQLite** - development ma'lumotlar bazasi (PostgreSQL ixtiyoriy)
- **django-crispy-forms + crispy-bootstrap5** - forma renderi
- **Bootstrap 5** - responsive dizayn (CDN)
- **Font Awesome 6** - ikonkalar (CDN)

### Ixtiyoriy / production uchun
- **PostgreSQL** - production ma'lumotlar bazasi (`requirements-full.txt`)
- **Django REST Framework** - RESTful API
- **Celery + Redis** - asinxron vazifalar
- **Pandas / NumPy / SciPy** - kengaytirilgan statistik tahlil
- **Matplotlib / Seaborn** - vizualizatsiya

## Testlar

```bash
python manage.py test
```

39 ta test: modellar, forma validatsiyasi, view'lar va admin sahifalari.

## O'rnatish

### Talablar

**Minimal (Development):**
- Python 3.9+
- SQLite (Python bilan birga keladi)
- pip va virtualenv

**To'liq (Production):**
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- pip va virtualenv

### Requirements fayllar

Loyihada 2 xil requirements fayl mavjud:
- **requirements.txt** - Asosiy kutubxonalar (Development, SQLite) - **TAVSIYA ETILADI!**
- **requirements-full.txt** - Barcha kutubxonalar (Production, PostgreSQL, Celery)

### Bosqichma-bosqich o'rnatish

1. Repositoriyani klonlash:
```bash
git clone https://github.com/AnonymousSherali/medical-child.git
cd medical-child
```

2. Virtual muhit yaratish va faollashtirish:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

3. Bog'liqliklarni o'rnatish:

**Development uchun (tavsiya etiladi):**
```bash
pip install -r requirements.txt
```

**Production uchun:**
```bash
pip install -r requirements-full.txt
```

4. Ma'lumotlar bazasini sozlash:

**Development (SQLite - default):**
```bash
# Hech narsa qilish kerak emas, SQLite avtomatik ishlatiladi
```

**Production (PostgreSQL - ixtiyoriy):**
```bash
# PostgreSQL da yangi baza yarating
createdb neuromonitor_db

# .env faylini yarating va sozlang
cp .env.example .env
# .env faylida DB_NAME, DB_USER, DB_PASSWORD ni to'ldiring
```

5. Migratsiyalarni bajarish:
```bash
python manage.py migrate
```

6. Superuser yaratish:
```bash
python manage.py createsuperuser
```

7. Statik fayllarni yig'ish:
```bash
python manage.py collectstatic
```

8. Serverni ishga tushirish:
```bash
python manage.py runserver
```

Brauzerda `http://localhost:8000` manziliga o'ting.

## Loyiha tuzilishi

```
medical-child/
├── apps/
│   ├── patients/          # Bemorlar moduli
│   ├── monitoring/        # Monitoring tizimi
│   ├── laboratory/        # Laboratoriya moduli
│   ├── analytics/         # Analitika va hisobotlar
│   └── users/            # Foydalanuvchilar va huquqlar
├── config/               # Django sozlamalari
├── static/              # Statik fayllar (CSS, JS, rasmlar)
├── templates/           # HTML shablonlar
├── media/              # Yuklangan fayllar
├── requirements.txt    # Python bog'liqliklari
└── manage.py          # Django boshqaruv skripti
```

## Foydalanish

### Admin panel
Admin panelga kirish: `http://localhost:8000/admin`
- Foydalanuvchilarni boshqarish
- Tizim sozlamalari
- Ma'lumotlar bazasini to'g'ridan-to'g'ri tahrirlash

### Asosiy funktsiyalar

1. **Bemor qo'shish**: Dashboard → Bemorlar → Yangi bemor
2. **Monitoring boshlash**: Bemor kartasida → Monitoring → Yangi sessiya
3. **Tahlil kiritish**: Bemor kartasida → Laboratoriya → Yangi tahlil
4. **Hisobot olish**: Analitika → Hisobotlar → Export

## Xavfsizlik

- Barcha parollar hashlangan holda saqlanadi
- HTTPS protokoli qo'llab-quvvatlanadi
- CSRF himoyasi yoqilgan
- SQL injection himoyasi (Django ORM)
- XSS himoyasi (Django templating)
- Foydalanuvchilar huquqlari bo'yicha nazorat

## Hissa qo'shish

Loyihaga hissa qo'shmoqchi bo'lsangiz:

1. Fork qiling
2. Yangi branch yarating (`git checkout -b feature/AmazingFeature`)
3. O'zgarishlaringizni commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Branch ga push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching

## Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil ma'lumot uchun `LICENSE` faylini ko'ring.

## Muallif va aloqa

**Loyiha muallifi**: AnonymousSherali

Savollar yoki takliflar bo'lsa:
- GitHub Issues: [Issues sahifasi](https://github.com/AnonymousSherali/medical-child/issues)
- Email: support@neuromonitor.uz

## Minnatdorchilik

- Tibbiy maslahat uchun: Respublika Perinatologiya Markazi
- Ilmiy rahbarlik: O'zbekiston Pediatriya Instituti
- Texnik qo'llab-quvvatlash: Django va Python hamjamiyati

---

**Eslatma**: Bu tizim faqat ilmiy tadqiqot va tibbiy xodimlarni qo'llab-quvvatlash maqsadida ishlab chiqilgan. Yakuniy diagnostik qarorlar faqat malakali shifokorlar tomonidan qabul qilinishi kerak.
