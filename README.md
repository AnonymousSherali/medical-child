# NeuroMonitor - Yangi tug'ilganlar neyrodiagnostika tizimi

## Loyiha haqida

NeuroMonitor - chala tug'ilgan yangi tug'ilgan chaqaloqlarda markaziy asab tizimining perinatal shikastlanishlarini diagnostika qilishda neyro-spetsifik oqsillarning klinik ahamiyatini o'rganish va monitoring qilish uchun mo'ljallangan tibbiy axborot tizimi.

## Maqsad

Chala tug'ilgan yangi tug'ilganlar markaziy asab tizimidagi perinatal shikastlanishlarni erta aniqlash va monitoring qilish uchun zamonaviy raqamli platforma yaratish, neyro-spetsifik oqsillar (NSE, S100B va boshqalar) ko'rsatkichlarini kuzatish va tahlil qilish.

## Asosiy imkoniyatlar

### 1. Bemor ma'lumotlarini boshqarish
- Yangi tug'ilganlarning shaxsiy ma'lumotlarini ro'yxatga olish
- Tug'ilish tarixi, gestatsion yoshi, og'irligi va boshqa parametrlarni saqlash
- Bemor tarixi va tibbiy hujjatlarni yuritish

### 2. Real-time monitoring tizimi
- Laboratoriya tahlillar natijalarini real vaqt rejimida kiritish
- Neyro-spetsifik oqsillar (NSE, S100B, GFAP) ko'rsatkichlarini kuzatish
- Vital signs (yurak urishi, nafas olish, qon bosimi) monitoringi
- Avtomatik ogohlantirish tizimi (kritik ko'rsatkichlar bo'yicha)

### 3. Laboratoriya integratsiyasi
- Laboratoriya natijalarini avtomatik import qilish
- Ma'lumotlarni standartlashtirish va validatsiya qilish
- Tahlil natijalarini me'yoriy qiymatlar bilan solishtirish

### 4. Analitika va hisobotlar
- Bemorlarning holatini dinamikada kuzatish
- Statistik tahlillar va trендlar ko'rsatkichlari
- Neyro-spetsifik oqsillar o'zgarishining grafik tasviri
- Klinik hisobotlarni avtomatik generatsiya qilish
- Excel/PDF formatda eksport qilish

### 5. Prognozlash moduli
- Sun'iy intellekt asosida xavf darajasini baholash
- Nevrologik komplikatsiyalar ehtimolini hisoblash
- Davolash natijalarini bashorat qilish

## Texnologiyalar

### Backend
- **Django 4.x** - asosiy web framework
- **Django REST Framework** - RESTful API
- **PostgreSQL** - ma'lumotlar bazasi
- **Celery** - asinxron vazifalar (hisobotlar, export)
- **Redis** - kesh va xabarlar navbati

### Frontend
- **HTML5/CSS3** - markup va stillar
- **Bootstrap 5** - responsive dizayn
- **JavaScript/jQuery** - interaktiv interfeys
- **Chart.js** - grafik va diagrammalar
- **DataTables** - jadvallar bilan ishlash

### Ma'lumotlar tahlili
- **Pandas** - ma'lumotlarni qayta ishlash
- **NumPy** - raqamli hisoblashlar
- **SciPy** - statistik tahlil
- **Matplotlib/Seaborn** - vizualizatsiya

## O'rnatish

### Talablar
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- pip va virtualenv

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
```bash
pip install -r requirements.txt
```

4. Ma'lumotlar bazasini sozlash:
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
