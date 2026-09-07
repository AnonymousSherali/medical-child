from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import PatientForm, PatientUpdateForm
from .models import Patient

User = get_user_model()


def make_patient(**overrides):
    """Testlar uchun bemor yaratish yordamchisi (boshqa applar ham ishlatadi)."""
    data = dict(
        medical_record_number='MRN-001',
        first_name='Ali',
        last_name='Valiyev',
        gender='M',
        birth_date=timezone.now() - timedelta(days=5),
        gestational_age=30,
        birth_weight=1.5,
        birth_length=40,
        head_circumference=28,
        apgar_score_1min=7,
        apgar_score_5min=8,
        mother_name='Zulfiya Valiyeva',
        mother_age=28,
        mother_phone='+998901234567',
    )
    data.update(overrides)
    return Patient.objects.create(**data)


class PatientModelTests(TestCase):
    def test_age_in_days_for_active_patient(self):
        self.assertEqual(make_patient().age_in_days, 5)

    def test_age_in_days_uses_discharge_date(self):
        # Regressiya: chiqarilgan bemor uchun avval None qaytarardi
        birth = timezone.now() - timedelta(days=30)
        patient = make_patient(
            birth_date=birth,
            is_active=False,
            discharge_date=birth + timedelta(days=10),
        )
        self.assertEqual(patient.age_in_days, 10)

    def test_is_preterm(self):
        self.assertTrue(make_patient(gestational_age=30).is_preterm)
        self.assertFalse(
            make_patient(medical_record_number='MRN-002', gestational_age=39).is_preterm
        )

    def test_full_name(self):
        self.assertEqual(make_patient().full_name, 'Ali Valiyev')


class PatientFormTests(TestCase):
    def _base_data(self):
        return {
            'medical_record_number': 'MRN-100',
            'first_name': 'Ali',
            'last_name': 'Valiyev',
            'gender': 'M',
            'birth_date': (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'gestational_age': 30,
            'birth_weight': '1.50',
            'birth_length': '40.0',
            'head_circumference': '28.0',
            'apgar_score_1min': 7,
            'apgar_score_5min': 8,
            'mother_name': 'Zulfiya',
            'mother_age': 28,
            'mother_phone': '+998901234567',
        }

    def test_create_form_has_no_status_fields(self):
        # Status maydonlari faqat tahrirlash formasida bo'lishi kerak
        self.assertNotIn('is_active', PatientForm().fields)
        self.assertNotIn('discharge_date', PatientForm().fields)
        self.assertIn('is_active', PatientUpdateForm().fields)

    def test_valid_data(self):
        self.assertTrue(PatientForm(data=self._base_data()).is_valid())

    def test_rejects_future_birth_date(self):
        data = self._base_data()
        data['birth_date'] = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        form = PatientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)

    def test_rejects_out_of_range_gestational_age(self):
        data = self._base_data()
        data['gestational_age'] = 50
        form = PatientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('gestational_age', form.errors)

    def test_rejects_out_of_range_apgar(self):
        data = self._base_data()
        data['apgar_score_1min'] = 15
        form = PatientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('apgar_score_1min', form.errors)

    def test_update_form_rejects_active_with_discharge_date(self):
        patient = make_patient()
        data = self._base_data()
        data['medical_record_number'] = patient.medical_record_number
        data['is_active'] = 'on'
        data['discharge_date'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
        form = PatientUpdateForm(data=data, instance=patient)
        self.assertFalse(form.is_valid())
        self.assertIn('is_active', form.errors)


class PatientViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='doctor', password='secret123')
        self.client.force_login(self.user)
        self.patient = make_patient()

    def test_dashboard_shows_active_patient(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.patient.medical_record_number)
        self.assertEqual(response.context['active_patient_count'], 1)

    def test_created_patient_is_active(self):
        # Regressiya: forma is_active ni False qilib yubormasligi kerak
        data = {
            'medical_record_number': 'MRN-777',
            'first_name': 'Yangi',
            'last_name': 'Bemor',
            'gender': 'F',
            'birth_date': (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'gestational_age': 32,
            'birth_weight': '1.80',
            'birth_length': '42.0',
            'head_circumference': '29.0',
            'apgar_score_1min': 8,
            'apgar_score_5min': 9,
            'mother_name': 'Ona',
            'mother_age': 30,
            'mother_phone': '+998901112233',
        }
        response = self.client.post(reverse('patient-create'), data)
        self.assertEqual(response.status_code, 302)
        created = Patient.objects.get(medical_record_number='MRN-777')
        self.assertTrue(created.is_active)
        self.assertEqual(created.created_by, self.user)

    def test_search_filters_results(self):
        make_patient(medical_record_number='MRN-002', first_name='Bobur', last_name='Karimov')
        response = self.client.get(reverse('patient-list'), {'q': 'Bobur'})
        self.assertContains(response, 'Bobur')
        self.assertNotContains(response, 'MRN-001')

    def test_history_create_returns_404_for_missing_patient(self):
        response = self.client.get(reverse('history-create', kwargs={'patient_pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('patient-list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)


class PatientAdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='secret123')
        self.client.force_login(self.admin)
        self.patient = make_patient()

    def test_patient_change_page_opens(self):
        # Regressiya: admission_date readonly bo'lmagani uchun FieldError berardi
        url = reverse('admin:patients_patient_change', args=[self.patient.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
