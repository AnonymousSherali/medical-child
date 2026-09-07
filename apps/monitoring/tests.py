from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.patients.tests import make_patient

from .forms import MonitoringSessionForm, NeurologicalAssessmentForm, VitalSignsForm
from .models import MonitoringSession

User = get_user_model()


class MonitoringSessionFormTests(TestCase):
    def setUp(self):
        self.patient = make_patient()

    def test_valid_session(self):
        form = MonitoringSessionForm(data={'patient': self.patient.pk, 'notes': ''})
        self.assertTrue(form.is_valid())

    def test_rejects_second_active_session_for_same_patient(self):
        MonitoringSession.objects.create(patient=self.patient)
        form = MonitoringSessionForm(data={'patient': self.patient.pk, 'notes': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('patient', form.errors)

    def test_only_active_patients_selectable(self):
        discharged = make_patient(medical_record_number='MRN-003', is_active=False)
        form = MonitoringSessionForm()
        self.assertNotIn(discharged, form.fields['patient'].queryset)


class VitalSignsFormTests(TestCase):
    def _data(self, **overrides):
        data = {
            'heart_rate': 140,
            'respiratory_rate': 45,
            'temperature': '36.6',
            'blood_pressure_systolic': 70,
            'blood_pressure_diastolic': 40,
            'oxygen_saturation': '97.00',
        }
        data.update(overrides)
        return data

    def test_valid(self):
        self.assertTrue(VitalSignsForm(data=self._data()).is_valid())

    def test_rejects_impossible_temperature(self):
        form = VitalSignsForm(data=self._data(temperature='60.0'))
        self.assertFalse(form.is_valid())
        self.assertIn('temperature', form.errors)

    def test_rejects_diastolic_above_systolic(self):
        form = VitalSignsForm(
            data=self._data(blood_pressure_systolic=60, blood_pressure_diastolic=90)
        )
        self.assertFalse(form.is_valid())
        self.assertIn('blood_pressure_diastolic', form.errors)

    def test_rejects_saturation_above_100(self):
        form = VitalSignsForm(data=self._data(oxygen_saturation=Decimal('120')))
        self.assertFalse(form.is_valid())
        self.assertIn('oxygen_saturation', form.errors)


class NeurologicalAssessmentFormTests(TestCase):
    def test_seizure_requires_description(self):
        form = NeurologicalAssessmentForm(data={
            'consciousness_level': 'Hushida',
            'muscle_tone': 'Normal',
            'reflexes': 'Saqlangan',
            'seizure_activity': 'on',
            'seizure_description': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('seizure_description', form.errors)


class MonitoringViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nurse', password='secret123')
        self.client.force_login(self.user)
        self.patient = make_patient()
        self.session = MonitoringSession.objects.create(patient=self.patient, created_by=self.user)

    def test_pages_render(self):
        for url in (
            reverse('monitoring-session-list'),
            reverse('monitoring-session-create'),
            reverse('monitoring-session-detail', kwargs={'pk': self.session.pk}),
            reverse('vital-signs-create', kwargs={'session_pk': self.session.pk}),
            reverse('neurological-assessment-create', kwargs={'session_pk': self.session.pk}),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_close_session(self):
        response = self.client.post(
            reverse('monitoring-session-close', kwargs={'pk': self.session.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.session.refresh_from_db()
        self.assertFalse(self.session.is_active)
        self.assertIsNotNone(self.session.end_date)

    def test_vital_signs_records_user_and_session(self):
        url = reverse('vital-signs-create', kwargs={'session_pk': self.session.pk})
        response = self.client.post(url, {
            'heart_rate': 140,
            'respiratory_rate': 45,
            'temperature': '36.6',
            'blood_pressure_systolic': 70,
            'blood_pressure_diastolic': 40,
            'oxygen_saturation': '97.00',
        })
        self.assertEqual(response.status_code, 302)
        vitals = self.session.vital_signs.get()
        self.assertEqual(vitals.recorded_by, self.user)

    def test_missing_session_returns_404(self):
        url = reverse('vital-signs-create', kwargs={'session_pk': 9999})
        self.assertEqual(self.client.get(url).status_code, 404)
