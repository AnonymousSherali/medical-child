from django.db import models
from django.conf import settings
from apps.patients.models import Patient


class MonitoringSession(models.Model):
    """
    Monitoring sessiyasi - bemorni kuzatish davri
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='monitoring_sessions',
        verbose_name='Bemor'
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Boshlanish sanasi'
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Tugash sanasi'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Faol'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Izohlar'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Yaratgan foydalanuvchi'
    )

    class Meta:
        verbose_name = 'Monitoring sessiyasi'
        verbose_name_plural = 'Monitoring sessiyalari'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.patient} - {self.start_date.strftime('%Y-%m-%d')}"


class VitalSigns(models.Model):
    """
    Vital signs - hayotiy ko'rsatkichlar
    """
    session = models.ForeignKey(
        MonitoringSession,
        on_delete=models.CASCADE,
        related_name='vital_signs',
        verbose_name='Sessiya'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Vaqt'
    )

    # Vital signs parametrlari
    heart_rate = models.IntegerField(
        verbose_name='Yurak urishi (bpm)',
        help_text='Minutiga urishlar soni'
    )
    respiratory_rate = models.IntegerField(
        verbose_name='Nafas olish (rpm)',
        help_text='Minutiga nafas olishlar soni'
    )
    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='Harorat (°C)'
    )
    blood_pressure_systolic = models.IntegerField(
        verbose_name='Qon bosimi (sistolik)',
        null=True,
        blank=True
    )
    blood_pressure_diastolic = models.IntegerField(
        verbose_name='Qon bosimi (diastolik)',
        null=True,
        blank=True
    )
    oxygen_saturation = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Qon kislorod to\'yinganligi (%)',
        null=True,
        blank=True
    )

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Qayd qilgan'
    )

    class Meta:
        verbose_name = 'Vital signs'
        verbose_name_plural = 'Vital signs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.session.patient} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class NeurologicalAssessment(models.Model):
    """
    Nevrologik baholash
    """
    session = models.ForeignKey(
        MonitoringSession,
        on_delete=models.CASCADE,
        related_name='neurological_assessments',
        verbose_name='Sessiya'
    )
    assessment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Baholash sanasi'
    )

    # Nevrologik holatni baholash
    consciousness_level = models.CharField(
        max_length=100,
        verbose_name='Ong darajasi'
    )
    muscle_tone = models.CharField(
        max_length=100,
        verbose_name='Mushak tonusi'
    )
    reflexes = models.TextField(
        verbose_name='Reflekslar'
    )
    seizure_activity = models.BooleanField(
        default=False,
        verbose_name='Tutqanoq faolligi'
    )
    seizure_description = models.TextField(
        blank=True,
        verbose_name='Tutqanoq tavsifi'
    )

    # Qo'shimcha ma'lumotlar
    fontanelle_status = models.CharField(
        max_length=100,
        verbose_name='Fontanel holati',
        blank=True
    )
    pupil_response = models.CharField(
        max_length=100,
        verbose_name='Ko\'z qorachiq reaktsiyasi',
        blank=True
    )

    assessment_notes = models.TextField(
        blank=True,
        verbose_name='Baholash izohlari'
    )
    assessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Baholagan shifokor'
    )

    class Meta:
        verbose_name = 'Nevrologik baholash'
        verbose_name_plural = 'Nevrologik baholashlar'
        ordering = ['-assessment_date']

    def __str__(self):
        return f"{self.session.patient} - {self.assessment_date.strftime('%Y-%m-%d')}"
