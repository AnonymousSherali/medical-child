# NeuroMonitor - O'rnatish qo'llanmasi

## Loyihaning hozirgi holati

Loyiha to'liq ishlab chiqilgan va ishga tushirishga tayyor. Quyidagi komponentlar yaratilgan:

### ✅ Backend (Django)
- **5 ta app**: users, patients, monitoring, laboratory, analytics
- **8+ model**: CustomUser, Patient, MonitoringSession, VitalSigns, LabTest, NeuroProteinResult va boshqalar
- **Admin panel**: Barcha modellar uchun admin interfeysi
- **Views va URLs**: CRUD operatsiyalari
- **Forms**: Validatsiya bilan

### ✅ Frontend
- **Base template**: Bootstrap 5 bilan responsive dizayn
- **Dashboard**: Statistika va bemorlar ro'yxati
- **Patient CRUD**: Bemor qo'shish, ko'rish, tahrirlash
- **Login sahifa**: Autentifikatsiya
- **Custom CSS**: Professional dizayn

### ✅ Konfiguratsiya
- **settings.py**: To'liq sozlangan
- **requirements.txt**: Barcha kerakli kutubxonalar
- **.env.example**: Muhit o'zgaruvchilari namunasi
- **.gitignore**: Git uchun sozlangan

## 🚀 Tezkor ishga tushirish (Windows/Linux/Mac)

### MUHIM: Requirements fayllar haqida

Loyihada 2 xil requirements fayl bor:
- **requirements.txt** - Asosiy kutubxonalar (Development uchun, SQLite bilan)
- **requirements-full.txt** - Barcha kutubxonalar (Production, PostgreSQL, Celery, etc.)

**Development uchun** - `requirements.txt` ishlatiladi (tavsiya etiladi!)
**Production uchun** - `requirements-full.txt` ishlatiladi

### 1. Repositoriyani klonlash
```bash
git clone https://github.com/AnonymousSherali/medical-child.git
cd medical-child
```

### 2. Virtual muhit yaratish

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Bog'liqliklarni o'rnatish

**Development uchun (tavsiya etiladi):**
```bash
pip install -r requirements.txt
```

**Production uchun (barcha kutubxonalar):**
```bash
pip install -r requirements-full.txt
```

> **Eslatma**: Agar `requirements-full.txt` dan psycopg2-binary o'rnatishda xato bo'lsa, PostgreSQL ni avval o'rnating yoki faqat `requirements.txt` ishlatiladi.

### 4. Migratsiyalarni bajarish
```bash
# Migratsiyalar repoda mavjud, shuning uchun faqat migrate yetarli
python manage.py migrate
```

### 5. Superuser yaratish
```bash
python manage.py createsuperuser
```

Kerakli ma'lumotlarni kiriting:
- Username: admin
- Email: admin@neuromonitor.uz
- Password: (xavfsiz parol)

### 6. Serverni ishga tushirish
```bash
python manage.py runserver
```

Brauzerda quyidagi manzillarni oching:
- **Asosiy sahifa**: http://localhost:8000
- **Admin panel**: http://localhost:8000/admin
- **Login**: http://localhost:8000/accounts/login/

## Loyiha tuzilishi

```
medical-child/
├── apps/
│   ├── users/              # Foydalanuvchilar
│   │   ├── models.py       # CustomUser
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── patients/           # Bemorlar
│   │   ├── models.py       # Patient, MedicalHistory
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── admin.py
│   ├── monitoring/         # Monitoring
│   │   ├── models.py       # MonitoringSession, VitalSigns
│   │   ├── views.py
│   │   └── admin.py
│   ├── laboratory/         # Laboratoriya
│   │   ├── models.py       # LabTest, NeuroProteinResult
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── admin.py
│   └── analytics/          # Analitika
│       ├── models.py       # Report, Statistics
│       ├── views.py
│       └── admin.py
├── config/
│   ├── settings.py         # Django sozlamalari
│   ├── urls.py             # Asosiy URL marshrutlar
│   └── wsgi.py
├── templates/
│   ├── base.html
│   ├── patients/
│   │   ├── dashboard.html
│   │   ├── patient_list.html
│   │   ├── patient_form.html
│   │   └── patient_detail.html
│   └── users/
│       └── login.html
├── static/
│   └── css/
│       └── style.css
├── manage.py
├── requirements.txt
└── README.md
```

## Asosiy xususiyatlar

### 1. Bemorlarni boshqarish
- Yangi tug'ilgan chaqaloqlarni ro'yxatga olish
- Tug'ilish parametrlarini saqlash (gestatsion yoshi, og'irligi, Apgar)
- Ona ma'lumotlari
- Tibbiy tarix

### 2. Monitoring tizimi
- Monitoring sessiyalarini boshqarish
- Vital signs (yurak urishi, nafas, harorat, qon bosimi)
- Nevrologik baholash
- Real-time kuzatuv

### 3. Laboratoriya
- Tahlillar buyurtmasi
- Neyro-spetsifik oqsillar (NSE, S100B, GFAP)
- Qon tahlillari
- Natijalarni avtomatik tekshirish

### 4. Analitika
- Dashboard bilan statistika
- Hisobotlar generatsiyasi
- Trendlarni kuzatish

### 5. Foydalanuvchilar
- Rol-based access (shifokor, hamshira, laborant, admin)
- Login/logout
- Profil boshqaruvi

## Keyingi qadamlar

### Database o'zgartirish (ixtiyoriy)
Hozirda SQLite ishlatilmoqda. PostgreSQL ga o'tish uchun:

1. PostgreSQL o'rnating va database yarating:
```sql
CREATE DATABASE neuromonitor_db;
CREATE USER neuromonitor WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE neuromonitor_db TO neuromonitor;
```

2. `config/settings.py` da DATABASES ni o'zgartiring:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neuromonitor_db',
        'USER': 'neuromonitor',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Migratsiyalarni qayta bajaring:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Production deployment
- DEBUG = False qiling
- SECRET_KEY ni o'zgartiring
- ALLOWED_HOSTS ni sozlang
- Static fayllarni to'plang: `python manage.py collectstatic`
- Gunicorn yoki uWSGI ishlatiladi
- Nginx reverse proxy

## Avtomatik testlar

```bash
python manage.py test                 # barchasi (39 ta)
python manage.py test apps.patients   # bitta app
```

## Test ma'lumotlar

Test uchun admin orqali demo ma'lumotlar qo'shing:
1. Admin panelga kiring: http://localhost:8000/admin
2. Users → Custom users → Add custom user
3. Patients → Patients → Add patient
4. Laboratory → Lab tests → Add lab test

## 🔧 Muammolarni hal qilish

### ❌ psycopg2-binary o'rnatish xatosi (Windows)

**Xato:**
```
Error: pg_config executable not found.
```

**Yechim 1 (Tavsiya etiladi - SQLite ishlatish):**
```bash
# Faqat asosiy kutubxonalarni o'rnating
pip install -r requirements.txt
```

**Yechim 2 (PostgreSQL kerak bo'lsa):**
1. PostgreSQL ni o'rnating: https://www.postgresql.org/download/windows/
2. PostgreSQL ning bin papkasini PATH ga qo'shing
3. `requirements-full.txt` dan o'rnating:
```bash
pip install -r requirements-full.txt
```

### ❌ crispy-bootstrap5 versiya xatosi

**Xato:**
```
ERROR: No matching distribution found for crispy-bootstrap5==2.0.0
```

**Sabab:** crispy-bootstrap5 versiyalash tizimi o'zgargan. Eski format (2.0.0) yo'q, yangi format (2024.2, 2024.10) ishlatiladi.

**Yechim:**
```bash
# Yangi versiyani ishlatiladi
pip install crispy-bootstrap5==2024.2

# Yoki requirements.txt yangilash
git pull origin claude/update-readme-content-T5XkB
pip install -r requirements.txt
```

### ❌ Pillow o'rnatish xatosi (Windows)

**Xato:**
```
KeyError: '__version__'
ERROR: Failed to build 'Pillow' when getting requirements to build wheel
```

**Sabab:** Pillow 10.2.0 versiyasi Windows'da muammoli.

**Yechim 1 (Tavsiya etiladi - Pillow'siz ishlash):**
Pillow hozirda `requirements.txt` da ixtiyoriy (izoh qilingan). Loyiha Pillow'siz ham ishlaydi. Rasm yuklash kerak bo'lganda o'rnating:
```bash
pip install "Pillow>=10.3.0"
```

**Yechim 2 (Pillow'ni alohida o'rnatish):**
```bash
# requirements.txt dan Pillow'ni olib tashlang va alohida o'rnating
pip install Pillow --upgrade
```

**Eslatma:** Loyiha asosiy funksiyalari (bemorlar, monitoring, laboratoriya) Pillow'siz ishlaydi.

### ❌ Migratsiya xatolari
```bash
# Bitta-bitta migratsiya qiling
python manage.py makemigrations users
python manage.py makemigrations patients
python manage.py makemigrations monitoring
python manage.py makemigrations laboratory
python manage.py makemigrations analytics
python manage.py migrate
```

### ❌ Static fayllar ko'rinmasa
```bash
python manage.py collectstatic --noinput
```

### ❌ Import xatolari
```bash
# requirements.txt qayta o'rnating
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ PowerShell script execution policy xatosi (Windows)

**Xato:**
```
venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled
```

**Yechim:**
```powershell
# PowerShell ni Administrator sifatida oching va quyidagini bajaring:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Yoki CMD ishlatiladi:
venv\Scripts\activate.bat
```

### ❌ "No module named 'apps'" xatosi

**Yechim:**
```bash
# manage.py faylidan ishga tushiring
python manage.py runserver

# Agar baribir xato bo'lsa, PYTHONPATH sozlang:
# Linux/Mac:
export PYTHONPATH="${PYTHONPATH}:/path/to/medical-child"

# Windows CMD:
set PYTHONPATH=%PYTHONPATH%;C:\path\to\medical-child

# Windows PowerShell:
$env:PYTHONPATH += ";C:\path\to\medical-child"
```

### ❌ Port band muammosi (Windows)

**Xato:**
```
Error: That port is already in use.
```

**Yechim:**
```bash
# Boshqa port ishlatiladi:
python manage.py runserver 8080

# Yoki band bo'lgan jarayonni to'xtating:
# Windows CMD:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

## Yordam

Savollar yoki muammolar bo'lsa:
- GitHub Issues: https://github.com/AnonymousSherali/medical-child/issues
- Email: support@neuromonitor.uz

---

**Eslatma**: Bu development versiyasi. Production uchun qo'shimcha xavfsizlik sozlamalari kerak.
