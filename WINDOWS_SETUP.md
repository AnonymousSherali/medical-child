# 🪟 Windows uchun tezkor o'rnatish qo'llanmasi

## Minimal talablar
- Windows 10/11
- Python 3.9 yoki yuqori
- Git

## ⚡ 5 daqiqada ishga tushirish

### 1. Python o'rnatilganligini tekshiring
```cmd
python --version
```
Agar o'rnatilmagan bo'lsa: https://www.python.org/downloads/

### 2. Git orqali loyihani yuklab oling
```cmd
git clone https://github.com/AnonymousSherali/medical-child.git
cd medical-child
```

### 3. Virtual muhit yarating va aktivlashtiring
```cmd
python -m venv venv
venv\Scripts\activate
```

> **Eslatma**: Agar PowerShell ishlatayotgan bo'lsangiz va xato chiqsa, CMD ishlatiladi yoki [PowerShell policy](#powershell-xatosi) ni o'zgartiring.

### 4. Kutubxonalarni o'rnating
```cmd
pip install -r requirements.txt
```

> **MUHIM**: `psycopg2-binary` xatosi chiqsa, bu normal! `requirements.txt` SQLite bilan ishlaydi.

### 5. Database yaratish
```cmd
python manage.py makemigrations
python manage.py migrate
```

### 6. Admin foydalanuvchi yaratish
```cmd
python manage.py createsuperuser
```

Ma'lumotlarni kiriting:
- **Username**: admin
- **Email**: admin@example.com
- **Password**: (xavfsiz parol kiriting)

### 7. Serverni ishga tushiring
```cmd
python manage.py runserver
```

### 8. Brauzerda oching
- **Dashboard**: http://localhost:8000
- **Admin panel**: http://localhost:8000/admin

## ✅ Muvaffaqiyatli o'rnatildi!

Endi siz:
- ✅ Admin panel orqali bemorlar qo'shishingiz mumkin
- ✅ Laboratoriya tahlillarini kiritishingiz mumkin
- ✅ Dashboard da statistikalarni ko'rishingiz mumkin

## 🔧 Tez-tez uchraydigan muammolar

### PowerShell xatosi
**Xato:**
```
Activate.ps1 cannot be loaded because running scripts is disabled
```

**Yechim 1 (CMD ishlatish):**
```cmd
venv\Scripts\activate.bat
```

**Yechim 2 (PowerShell policy o'zgartirish):**
```powershell
# PowerShell ni Administrator sifatida oching
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### psycopg2-binary xatosi
**Bu normal!** Development uchun SQLite ishlatamiz. PostgreSQL kerak bo'lsa:
1. PostgreSQL o'rnating: https://www.postgresql.org/download/windows/
2. `requirements-full.txt` ishlatiladi:
```cmd
pip install -r requirements-full.txt
```

### crispy-bootstrap5 versiya xatosi
**Xato:**
```
ERROR: No matching distribution found for crispy-bootstrap5==2.0.0
```

**Sabab:** crispy-bootstrap5 versiyalash tizimi o'zgargan (2024.2, 2024.10 formatda).

**Yechim:**
Bu xato eski requirements.txt da. Yangi versiyada tuzatilgan. Agar paydo bo'lsa:
```cmd
# requirements.txt ni yangilang
git pull origin claude/update-readme-content-T5XkB

# Yoki qo'lda o'rnating
pip install crispy-bootstrap5==2024.2
```

### Pillow xatosi (KeyError: '__version__')
**Xato:**
```
KeyError: '__version__'
ERROR: Failed to build 'Pillow' when getting requirements to build wheel
```

**Yechim:**
Pillow hozirda ixtiyoriy kutubxona. Agar rasm yuklash kerak bo'lmasa, uni o'rnatmasangiz ham bo'ladi.

**Agar Pillow kerak bo'lsa:**
```cmd
# Yangi versiyani o'rnating
pip install Pillow --upgrade

# Yoki muayyan versiya
pip install "Pillow>=10.3.0"
```

**Eslatma:** Loyiha Pillow'siz ham ishlaydi. Rasm yuklash funksiyasi kerak bo'lganda o'rnating.

### Port band bo'lsa
```cmd
# Boshqa portda ishga tushiring
python manage.py runserver 8080
```

### Migratsiya xatosi
```cmd
# Har bir app uchun alohida
python manage.py makemigrations users
python manage.py makemigrations patients
python manage.py migrate
```

## 📱 Qo'shimcha ma'lumot

Batafsil qo'llanma uchun `SETUP.md` faylini o'qing.

## 🆘 Yordam

Muammolar bo'lsa:
- GitHub Issues: https://github.com/AnonymousSherali/medical-child/issues
- SETUP.md faylini o'qing
