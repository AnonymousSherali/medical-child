from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.patients.tests import make_patient

from .forms import LabTestForm
from .models import LabTest, NeuroProteinResult

User = get_user_model()


class NeuroProteinResultTests(TestCase):
    def setUp(self):
        self.patient = make_patient()
        self.lab_test = LabTest.objects.create(
            patient=self.patient,
            test_type='nse',
            test_date=timezone.now(),
            sample_collected_date=timezone.now() - timedelta(hours=1),
        )

    def _result(self, **kwargs):
        defaults = dict(
            lab_test=self.lab_test, protein_type='nse', value=Decimal('10'), unit='ng/ml'
        )
        defaults.update(kwargs)
        return NeuroProteinResult.objects.create(**defaults)

    def test_marks_value_above_range_as_abnormal(self):
        result = self._result(
            value=Decimal('50'),
            reference_range_min=Decimal('5'),
            reference_range_max=Decimal('20'),
        )
        self.assertTrue(result.is_abnormal)

    def test_marks_value_inside_range_as_normal(self):
        result = self._result(
            value=Decimal('10'),
            reference_range_min=Decimal('5'),
            reference_range_max=Decimal('20'),
        )
        self.assertFalse(result.is_abnormal)

    def test_zero_reference_minimum_is_respected(self):
        # Regressiya: min=0 "falsy" bo'lgani uchun avval e'tiborsiz qolardi
        result = self._result(
            value=Decimal('30'),
            reference_range_min=Decimal('0'),
            reference_range_max=Decimal('20'),
        )
        self.assertTrue(result.is_abnormal)

    def test_only_upper_bound_given(self):
        result = self._result(value=Decimal('25'), reference_range_max=Decimal('20'))
        self.assertTrue(result.is_abnormal)

    def test_has_abnormal_results_property(self):
        self.assertFalse(self.lab_test.has_abnormal_results)
        self._result(value=Decimal('99'), reference_range_max=Decimal('20'))
        self.assertTrue(self.lab_test.has_abnormal_results)


class LabTestViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lab', password='secret123')
        self.client.force_login(self.user)
        self.patient = make_patient()
        self.lab_test = LabTest.objects.create(
            patient=self.patient,
            test_type='nse',
            test_date=timezone.now(),
            sample_collected_date=timezone.now() - timedelta(hours=1),
        )

    def test_pages_render(self):
        for url in (
            reverse('labtest-list'),
            reverse('labtest-create'),
            reverse('labtest-detail', kwargs={'pk': self.lab_test.pk}),
            reverse('neuroprotein-list'),
            reverse('neuroprotein-create', kwargs={'test_pk': self.lab_test.pk}),
            reverse('blood-create', kwargs={'test_pk': self.lab_test.pk}),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_result_create_returns_404_for_missing_test(self):
        url = reverse('neuroprotein-create', kwargs={'test_pk': 9999})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_mark_test_completed(self):
        url = reverse('labtest-complete', kwargs={'pk': self.lab_test.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.lab_test.refresh_from_db()
        self.assertTrue(self.lab_test.is_completed)
        self.assertEqual(self.lab_test.performed_by, self.user)

    def test_sample_date_after_test_date_is_rejected(self):
        now = timezone.now()
        form = LabTestForm(data={
            'patient': self.patient.pk,
            'test_type': 'nse',
            'test_date': now.strftime('%Y-%m-%dT%H:%M'),
            'sample_collected_date': (now + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M'),
            'notes': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('sample_collected_date', form.errors)

    def test_csv_export(self):
        response = self.client.get(reverse('export-patients'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])
        self.assertIn(self.patient.medical_record_number, response.content.decode('utf-8'))

    def test_neuroprotein_csv_export(self):
        NeuroProteinResult.objects.create(
            lab_test=self.lab_test, protein_type='nse', value=Decimal('12'), unit='ng/ml'
        )
        response = self.client.get(reverse('export-neuroprotein'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.patient.full_name, response.content.decode('utf-8'))
