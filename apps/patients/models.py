from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Patient(models.Model):
    """
    Bemor modeli - yangi tug'ilganlar ma'lumotlari
    """
    GENDER_CHOICES = [
        ('M', 'O\'g\'il'),
        ('F', 'Qiz'),
    ]

    # Asosiy ma'lumotlar
    medical_record_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Tibbiy karta raqami'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Ism'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Familiya'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Jinsi'
    )
    birth_date = models.DateTimeField(
        verbose_name='Tug\'ilgan sana va vaqt'
    )

    # Tug'ilish parametrlari
    gestational_age = models.IntegerField(
        verbose_name='Gestatsion yoshi (hafta)',
        help_text='Homiladorlik muddati haftalarda',
        validators=[MinValueValidator(20), MaxValueValidator(44)]
    )
    birth_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Tug\'ilish og\'irligi (kg)'
    )
    birth_length = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Tug\'ilish bo\'yi (cm)'
    )
    head_circumference = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Bosh aylanasi (cm)'
    )
    apgar_score_1min = models.IntegerField(
        verbose_name='Apgar (1 daqiqa)',
        help_text='Apgar ko\'rsatkichi 1 daqiqada',
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    apgar_score_5min = models.IntegerField(
        verbose_name='Apgar (5 daqiqa)',
        help_text='Apgar ko\'rsatkichi 5 daqiqada',
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Ona ma'lumotlari
    mother_name = models.CharField(
        max_length=200,
        verbose_name='Ona FIO'
    )
    mother_age = models.IntegerField(
        verbose_name='Ona yoshi'
    )
    mother_phone = models.CharField(
        max_length=20,
        verbose_name='Ona telefoni'
    )

    # Tibbiy ma'lumotlar
    diagnosis = models.TextField(
        verbose_name='Tashxis',
        blank=True
    )
    complications = models.TextField(
        verbose_name='Asoratlar',
        blank=True
    )
    treatment_plan = models.TextField(
        verbose_name='Davolash rejasi',
        blank=True
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name='Faol'
    )
    admission_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Qabul qilingan sana'
    )
    discharge_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Chiqarilgan sana'
    )

    # Meta
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_patients',
        verbose_name='Yaratgan foydalanuvchi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan sana'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yangilangan sana'
    )

    class Meta:
        verbose_name = 'Bemor'
        verbose_name_plural = 'Bemorlar'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.medical_record_number})"

    def get_absolute_url(self):
        return reverse('patient-detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age_in_days(self):
        """Bemorning yoshi kunlarda.

        Chiqarilgan bemorlar uchun chiqarish sanasidagi yoshi qaytariladi,
        faol bemorlar uchun esa bugungi yoshi.
        """
        from django.utils import timezone

        if not self.birth_date:
            return None
        end = self.discharge_date or timezone.now()
        return (end - self.birth_date).days

    @property
    def is_preterm(self):
        """37 haftadan erta tug'ilganmi (chala tug'ilgan)."""
        return self.gestational_age is not None and self.gestational_age < 37


class MedicalHistory(models.Model):
    """
    Bemor tibbiy tarixi
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_histories',
        verbose_name='Bemor'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Sana'
    )
    description = models.TextField(
        verbose_name='Tavsif'
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Shifokor'
    )

    class Meta:
        verbose_name = 'Tibbiy tarix'
        verbose_name_plural = 'Tibbiy tarix'
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient} - {self.date.strftime('%Y-%m-%d %H:%M')}"
