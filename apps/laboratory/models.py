from django.db import models
from django.conf import settings
from apps.patients.models import Patient


class LabTest(models.Model):
    """
    Laboratoriya tahlili
    """
    TEST_TYPE_CHOICES = [
        ('nse', 'NSE (Neyron-spetsifik enolaza)'),
        ('s100b', 'S100B oqsili'),
        ('gfap', 'GFAP (Gliafibrillyar kislotali oqsil)'),
        ('blood', 'Qon tahlili'),
        ('csf', 'Miya-orqa suyuqligi tahlili'),
        ('other', 'Boshqa'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='lab_tests',
        verbose_name='Bemor'
    )
    test_type = models.CharField(
        max_length=20,
        choices=TEST_TYPE_CHOICES,
        verbose_name='Tahlil turi'
    )
    test_date = models.DateTimeField(
        verbose_name='Tahlil sanasi'
    )
    sample_collected_date = models.DateTimeField(
        verbose_name='Namuna olingan sana'
    )

    # Status
    is_completed = models.BooleanField(
        default=False,
        verbose_name='Tugallangan'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Izohlar'
    )

    # Meta
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ordered_tests',
        verbose_name='Buyurtma bergan'
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='performed_tests',
        verbose_name='Bajargan laborant',
        blank=True
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
        verbose_name = 'Laboratoriya tahlili'
        verbose_name_plural = 'Laboratoriya tahillari'
        ordering = ['-test_date']

    def __str__(self):
        return f"{self.patient} - {self.get_test_type_display()} ({self.test_date.strftime('%Y-%m-%d')})"


class NeuroProteinResult(models.Model):
    """
    Neyro-spetsifik oqsillar natijalari
    """
    PROTEIN_TYPE_CHOICES = [
        ('nse', 'NSE'),
        ('s100b', 'S100B'),
        ('gfap', 'GFAP'),
    ]

    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE,
        related_name='neuro_protein_results',
        verbose_name='Laboratoriya tahlili'
    )
    protein_type = models.CharField(
        max_length=20,
        choices=PROTEIN_TYPE_CHOICES,
        verbose_name='Oqsil turi'
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name='Qiymat'
    )
    unit = models.CharField(
        max_length=20,
        verbose_name='O\'lchov birligi',
        help_text='Masalan: ng/ml, pg/ml'
    )
    reference_range_min = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name='Me\'yoriy diapazon (min)',
        null=True,
        blank=True
    )
    reference_range_max = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name='Me\'yoriy diapazon (max)',
        null=True,
        blank=True
    )
    is_abnormal = models.BooleanField(
        default=False,
        verbose_name='Me\'yordan chetlashgan'
    )
    interpretation = models.TextField(
        blank=True,
        verbose_name='Talqin'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan sana'
    )

    class Meta:
        verbose_name = 'Neyro-oqsil natijasi'
        verbose_name_plural = 'Neyro-oqsil natijalari'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_protein_type_display()}: {self.value} {self.unit}"

    def save(self, *args, **kwargs):
        # Avtomatik me'yordan chetlashganligini tekshirish
        if self.reference_range_min and self.reference_range_max:
            if self.value < self.reference_range_min or self.value > self.reference_range_max:
                self.is_abnormal = True
            else:
                self.is_abnormal = False
        super().save(*args, **kwargs)


class BloodTestResult(models.Model):
    """
    Qon tahlili natijalari
    """
    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE,
        related_name='blood_test_results',
        verbose_name='Laboratoriya tahlili'
    )

    # Asosiy ko'rsatkichlar
    hemoglobin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Gemoglobin (g/L)',
        null=True,
        blank=True
    )
    rbc = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Eritrotsitlar (10^12/L)',
        null=True,
        blank=True
    )
    wbc = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Leykotsitlar (10^9/L)',
        null=True,
        blank=True
    )
    platelets = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Trombotsilar (10^9/L)',
        null=True,
        blank=True
    )
    glucose = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Glyukoza (mmol/L)',
        null=True,
        blank=True
    )
    creatinine = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Kreatinin (µmol/L)',
        null=True,
        blank=True
    )
    bilirubin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Bilirubin (µmol/L)',
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True,
        verbose_name='Izohlar'
    )

    class Meta:
        verbose_name = 'Qon tahlili natijasi'
        verbose_name_plural = 'Qon tahlili natijalari'

    def __str__(self):
        return f"Qon tahlili - {self.lab_test.patient}"
