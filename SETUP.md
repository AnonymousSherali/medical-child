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

## Tezkor ishga tushirish

### 1. Repositoriyani klonlash
```bash
git clone https://github.com/AnonymousSherali/medical-child.git
cd medical-child
```

### 2. Virtual muhit yaratish
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Bog'liqliklarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Migratsiyalarni bajarish
```bash
python manage.py makemigrations
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

## Test ma'lumotlar

Test uchun admin orqali demo ma'lumotlar qo'shing:
1. Admin panelga kiring: http://localhost:8000/admin
2. Users → Custom users → Add custom user
3. Patients → Patients → Add patient
4. Laboratory → Lab tests → Add lab test

## Muammolarni hal qilish

### Migratsiya xatolari
```bash
python manage.py makemigrations users
python manage.py makemigrations patients
python manage.py migrate
```

### Static fayllar ko'rinmasa
```bash
python manage.py collectstatic
```

### Import xatolari
```bash
pip install -r requirements.txt
```

## Yordam

Savollar yoki muammolar bo'lsa:
- GitHub Issues: https://github.com/AnonymousSherali/medical-child/issues
- Email: support@neuromonitor.uz

---

**Eslatma**: Bu development versiyasi. Production uchun qo'shimcha xavfsizlik sozlamalari kerak.
