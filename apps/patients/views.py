from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Patient


class DashboardView(LoginRequiredMixin, ListView):
    """Asosiy dashboard"""
    model = Patient
    template_name = 'patients/dashboard.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        return Patient.objects.filter(is_active=True)


class PatientListView(LoginRequiredMixin, ListView):
    """Bemorlar ro'yxati"""
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20


class PatientDetailView(LoginRequiredMixin, DetailView):
    """Bemor tafsilotlari"""
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'


class PatientCreateView(LoginRequiredMixin, CreateView):
    """Yangi bemor qo'shish"""
    model = Patient
    template_name = 'patients/patient_form.html'
    fields = [
        'medical_record_number', 'first_name', 'last_name', 'gender', 'birth_date',
        'gestational_age', 'birth_weight', 'birth_length', 'head_circumference',
        'apgar_score_1min', 'apgar_score_5min',
        'mother_name', 'mother_age', 'mother_phone',
        'diagnosis', 'complications', 'treatment_plan'
    ]
    success_url = reverse_lazy('patient-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    """Bemor ma'lumotlarini yangilash"""
    model = Patient
    template_name = 'patients/patient_form.html'
    fields = [
        'first_name', 'last_name', 'gender', 'birth_date',
        'gestational_age', 'birth_weight', 'birth_length', 'head_circumference',
        'apgar_score_1min', 'apgar_score_5min',
        'mother_name', 'mother_age', 'mother_phone',
        'diagnosis', 'complications', 'treatment_plan',
        'is_active', 'discharge_date'
    ]
    success_url = reverse_lazy('patient-list')
