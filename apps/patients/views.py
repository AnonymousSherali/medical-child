from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Patient, MedicalHistory
from .forms import PatientForm, MedicalHistoryForm


class DashboardView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/dashboard.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        return Patient.objects.filter(is_active=True)


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient-list')


class MedicalHistoryCreateView(LoginRequiredMixin, CreateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm
    template_name = 'patients/history_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(pk=self.kwargs['patient_pk'])
        return context

    def form_valid(self, form):
        form.instance.patient = Patient.objects.get(pk=self.kwargs['patient_pk'])
        form.instance.doctor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patient-detail', kwargs={'pk': self.kwargs['patient_pk']})
