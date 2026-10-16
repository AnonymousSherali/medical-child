from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.laboratory.models import LabTest, NeuroProteinResult
from apps.monitoring.models import MonitoringSession, VitalSigns
from apps.patients.tests import make_patient

User = get_user_model()


class NavigationTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_user('doc', password='x'))

    def test_active_section(self):
        cases = {
            reverse('dashboard'): 'dashboard',
            reverse('patient-list'): 'patients',
            reverse('labtest-list'): 'laboratory',
            reverse('neuroprotein-list'): 'neuroprotein',
            reverse('monitoring-session-list'): 'monitoring',
            reverse('analytics-dashboard'): 'analytics',
            reverse('report-list'): 'reports',
            reverse('help'): 'help',
        }
        for url, section in cases.items():
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).context['nav_section'], section)

    def test_sidebar_badges(self):
        patient = make_patient()
        MonitoringSession.objects.create(patient=patient)
        test = LabTest.objects.create(patient=patient, test_type='nse',
                                      test_date=timezone.now(), sample_collected_date=timezone.now())
        NeuroProteinResult.objects.create(lab_test=test, protein_type='nse', value=Decimal('50'),
                                          unit='ng/ml', reference_range_max=Decimal('20'))
        context = self.client.get(reverse('dashboard')).context
        self.assertEqual(context['nav_active_sessions'], 1)
        self.assertEqual(context['nav_recent_abnormal'], 1)

    def test_help_page(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NSE')

    @override_settings(DEBUG=False)
    def test_custom_404(self):
        response = self.client.get('/mavjud-emas/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Sahifa topilmadi', status_code=404)


class ChartDataTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_user('doc', password='x'))
        self.patient = make_patient(gestational_age=30)
        make_patient(medical_record_number='MRN-T', gestational_age=39)

    def test_dashboard_gestation_buckets(self):
        context = self.client.get(reverse('dashboard')).context
        self.assertEqual(context['gestation_chart']['values'], [0, 1, 0, 1])

    def test_patient_protein_chart_is_chronological(self):
        now = timezone.now()
        later = LabTest.objects.create(patient=self.patient, test_type='nse',
                                       test_date=now, sample_collected_date=now)
        earlier = LabTest.objects.create(patient=self.patient, test_type='s100b',
                                         test_date=now - timedelta(days=2),
                                         sample_collected_date=now - timedelta(days=2))
        NeuroProteinResult.objects.create(lab_test=later, protein_type='nse', value=Decimal('12'), unit='ng/ml')
        NeuroProteinResult.objects.create(lab_test=earlier, protein_type='s100b', value=Decimal('0.5'), unit='µg/L')

        chart = self.client.get(reverse('patient-detail', args=[self.patient.pk])).context['protein_chart']
        self.assertEqual({s['label'] for s in chart}, {'NSE', 'S100B'})
        stamps = sorted(p['t'] for s in chart for p in s['points'])
        self.assertEqual(stamps[0], earlier.test_date.isoformat())

    def test_session_vitals_chart(self):
        session = MonitoringSession.objects.create(patient=self.patient)
        VitalSigns.objects.create(session=session, heart_rate=140, respiratory_rate=45,
                                  temperature=Decimal('36.6'))
        chart = self.client.get(reverse('monitoring-session-detail', args=[session.pk])).context['vitals_chart']
        self.assertEqual(chart['heart_rate'], [140])
        self.assertEqual(chart['oxygen_saturation'], [None])

    def test_analytics_protein_chart(self):
        test = LabTest.objects.create(patient=self.patient, test_type='nse',
                                      test_date=timezone.now(), sample_collected_date=timezone.now())
        NeuroProteinResult.objects.create(lab_test=test, protein_type='nse', value=Decimal('50'),
                                          unit='ng/ml', reference_range_max=Decimal('20'))
        NeuroProteinResult.objects.create(lab_test=test, protein_type='nse', value=Decimal('10'),
                                          unit='ng/ml', reference_range_max=Decimal('20'))
        chart = self.client.get(reverse('analytics-dashboard')).context['protein_chart']
        self.assertEqual(chart, {'labels': ['NSE'], 'normal': [1], 'abnormal': [1]})


class DeviationTests(TestCase):
    def setUp(self):
        patient = make_patient()
        self.test = LabTest.objects.create(patient=patient, test_type='nse',
                                           test_date=timezone.now(), sample_collected_date=timezone.now())

    def _result(self, value, low=None, high=None):
        return NeuroProteinResult.objects.create(
            lab_test=self.test, protein_type='nse', value=Decimal(value), unit='ng/ml',
            reference_range_min=low, reference_range_max=high,
        )

    def test_directions(self):
        self.assertEqual(self._result('30', Decimal('5'), Decimal('20')).deviation, 'high')
        self.assertEqual(self._result('2', Decimal('5'), Decimal('20')).deviation, 'low')
        self.assertIsNone(self._result('10', Decimal('5'), Decimal('20')).deviation)
        self.assertIsNone(self._result('10').deviation)

    def test_has_abnormal_results_uses_prefetch(self):
        self._result('30', high=Decimal('20'))
        test = LabTest.objects.prefetch_related('neuro_protein_results').get(pk=self.test.pk)
        with self.assertNumQueries(0):
            self.assertTrue(test.has_abnormal_results)


class LabSearchTests(TestCase):
    def test_search_by_patient_name(self):
        self.client.force_login(User.objects.create_user('lab', password='x'))
        ali = make_patient(first_name='Ali')
        bobur = make_patient(medical_record_number='MRN-B', first_name='Bobur')
        for p in (ali, bobur):
            LabTest.objects.create(patient=p, test_type='nse',
                                   test_date=timezone.now(), sample_collected_date=timezone.now())
        tests = self.client.get(reverse('labtest-list'), {'q': 'Bobur'}).context['tests']
        self.assertEqual([t.patient for t in tests], [bobur])
