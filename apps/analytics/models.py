from django.db import models
from django.conf import settings
from apps.patients.models import Patient


class Report(models.Model):
    """
    Analitik hisobot
    """
    REPORT_TYPE_CHOICES = [
        ('patient_summary', 'Bemor xulosasi'),
        ('neuroprotein_trend', 'Neyro-oqsillar trendi'),
        ('statistical', 'Statistik hisobot'),
        ('custom', 'Maxsus hisobot'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Sarlavha'
    )
    report_type = models.CharField(
        max_length=30,
        choices=REPORT_TYPE_CHOICES,
        verbose_name='Hisobot turi'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Tavsif'
    )

    # Filtrlar
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Bemor',
        help_text='Ma\'lum bemor uchun hisobot'
    )
    date_from = models.DateField(
        null=True,
        blank=True,
        verbose_name='Sanadan'
    )
    date_to = models.DateField(
        null=True,
        blank=True,
        verbose_name='Sanagacha'
    )

    # Hisobot fayli
    file = models.FileField(
        upload_to='reports/%Y/%m/',
        null=True,
        blank=True,
        verbose_name='Fayl'
    )
    file_type = models.CharField(
        max_length=10,
        choices=[('pdf', 'PDF'), ('xlsx', 'Excel')],
        default='pdf',
        verbose_name='Fayl turi'
    )

    # Meta
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Yaratgan foydalanuvchi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan sana'
    )
    is_generated = models.BooleanField(
        default=False,
        verbose_name='Yaratilgan'
    )

    class Meta:
        verbose_name = 'Hisobot'
        verbose_name_plural = 'Hisobotlar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"


class Statistics(models.Model):
    """
    Statistik ma'lumotlar
    """
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Sana'
    )
    total_patients = models.IntegerField(
        default=0,
        verbose_name='Jami bemorlar'
    )
    active_patients = models.IntegerField(
        default=0,
        verbose_name='Faol bemorlar'
    )
    total_tests = models.IntegerField(
        default=0,
        verbose_name='Jami tahlillar'
    )
    abnormal_results = models.IntegerField(
        default=0,
        verbose_name='Me\'yordan chetlashgan natijalar'
    )

    class Meta:
        verbose_name = 'Statistika'
        verbose_name_plural = 'Statistikalar'
        ordering = ['-date']

    def __str__(self):
        return f"Statistika - {self.date}"
