from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import MonitoringSession, VitalSigns, NeurologicalAssessment
from apps.patients.models import Patient


class MonitoringSessionListView(LoginRequiredMixin, ListView):
    """Monitoring sessiyalari ro'yxati"""
    model = MonitoringSession
    template_name = 'monitoring/session_list.html'
    context_object_name = 'sessions'
    paginate_by = 20


class MonitoringSessionDetailView(LoginRequiredMixin, DetailView):
    """Monitoring sessiyasi tafsilotlari"""
    model = MonitoringSession
    template_name = 'monitoring/session_detail.html'
    context_object_name = 'session'


class VitalSignsCreateView(LoginRequiredMixin, CreateView):
    """Vital signs qo'shish"""
    model = VitalSigns
    template_name = 'monitoring/vital_signs_form.html'
    fields = [
        'heart_rate', 'respiratory_rate', 'temperature',
        'blood_pressure_systolic', 'blood_pressure_diastolic',
        'oxygen_saturation'
    ]

    def form_valid(self, form):
        session = get_object_or_404(MonitoringSession, pk=self.kwargs['session_pk'])
        form.instance.session = session
        form.instance.recorded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('monitoring-session-detail', kwargs={'pk': self.kwargs['session_pk']})


class NeurologicalAssessmentCreateView(LoginRequiredMixin, CreateView):
    """Nevrologik baholash qo'shish"""
    model = NeurologicalAssessment
    template_name = 'monitoring/neurological_assessment_form.html'
    fields = [
        'consciousness_level', 'muscle_tone', 'reflexes',
        'seizure_activity', 'seizure_description',
        'fontanelle_status', 'pupil_response', 'assessment_notes'
    ]

    def form_valid(self, form):
        session = get_object_or_404(MonitoringSession, pk=self.kwargs['session_pk'])
        form.instance.session = session
        form.instance.assessed_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('monitoring-session-detail', kwargs={'pk': self.kwargs['session_pk']})
