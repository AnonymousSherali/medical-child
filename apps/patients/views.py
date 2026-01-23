from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Patient
from .forms import PatientForm


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
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    """Bemor ma'lumotlarini yangilash"""
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient-list')
