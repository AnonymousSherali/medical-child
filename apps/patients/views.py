from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.laboratory.models import LabTest, NeuroProteinResult
from apps.monitoring.models import MonitoringSession

from .forms import MedicalHistoryForm, PatientForm, PatientUpdateForm
from .models import MedicalHistory, Patient


class DashboardView(LoginRequiredMixin, ListView):
    """Asosiy dashboard — faol bemorlar va kunlik statistika."""

    model = Patient
    template_name = 'patients/dashboard.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        return Patient.objects.filter(is_active=True).select_related('created_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        # Bu qiymatlar template'da qattiq 0 bo'lib turgan edi
        context['active_patient_count'] = Patient.objects.filter(is_active=True).count()
        context['tests_today'] = LabTest.objects.filter(test_date__date=today).count()
        context['abnormal_count'] = NeuroProteinResult.objects.filter(is_abnormal=True).count()
        context['active_sessions'] = MonitoringSession.objects.filter(is_active=True).count()
        return context


class PatientListView(LoginRequiredMixin, ListView):
    """Bemorlar ro'yxati — qidiruv va status filtri bilan."""

    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        queryset = Patient.objects.select_related('created_by')
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(medical_record_number__icontains=query)
                | Q(mother_name__icontains=query)
            )
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'discharged':
            queryset = queryset.filter(is_active=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['status'] = self.request.GET.get('status', '')
        return context


class PatientDetailView(LoginRequiredMixin, DetailView):
    """Bemor tafsilotlari — tarix, tahlillar va monitoring bilan."""

    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object

        # Bu bo'limlar sahifada umuman ko'rsatilmasdi
        context['histories'] = patient.medical_histories.select_related('doctor')[:10]
        context['lab_tests'] = patient.lab_tests.prefetch_related(
            'neuro_protein_results', 'blood_test_results'
        )[:10]
        context['sessions'] = patient.monitoring_sessions.all()[:10]
        context['active_session'] = patient.monitoring_sessions.filter(is_active=True).first()
        return context


class PatientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Yangi bemor qo'shish"""

    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_message = "Bemor muvaffaqiyatli qo'shildi"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patient-detail', kwargs={'pk': self.object.pk})


class PatientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Bemor ma'lumotlarini yangilash"""

    model = Patient
    form_class = PatientUpdateForm
    template_name = 'patients/patient_form.html'
    success_message = "Bemor ma'lumotlari yangilandi"

    def get_success_url(self):
        return reverse('patient-detail', kwargs={'pk': self.object.pk})


class MedicalHistoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Bemor tibbiy tarixiga yozuv qo'shish"""

    model = MedicalHistory
    form_class = MedicalHistoryForm
    template_name = 'patients/history_form.html'
    success_message = "Tibbiy tarixga yozuv qo'shildi"

    def dispatch(self, request, *args, **kwargs):
        # .get() 500 qaytarardi, endi 404
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        return context

    def form_valid(self, form):
        form.instance.patient = self.patient
        form.instance.doctor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patient-detail', kwargs={'pk': self.patient.pk})
