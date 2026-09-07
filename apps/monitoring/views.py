from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from .forms import MonitoringSessionForm, NeurologicalAssessmentForm, VitalSignsForm
from .models import MonitoringSession, NeurologicalAssessment, VitalSigns


class MonitoringSessionListView(LoginRequiredMixin, ListView):
    """Monitoring sessiyalari ro'yxati"""

    model = MonitoringSession
    template_name = 'monitoring/session_list.html'
    context_object_name = 'sessions'
    paginate_by = 20

    def get_queryset(self):
        queryset = MonitoringSession.objects.select_related('patient', 'created_by')
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'closed':
            queryset = queryset.filter(is_active=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class MonitoringSessionDetailView(LoginRequiredMixin, DetailView):
    """Monitoring sessiyasi tafsilotlari"""

    model = MonitoringSession
    template_name = 'monitoring/session_detail.html'
    context_object_name = 'session'

    def get_queryset(self):
        return MonitoringSession.objects.select_related('patient', 'created_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vital_signs'] = self.object.vital_signs.select_related('recorded_by')[:50]
        context['assessments'] = self.object.neurological_assessments.select_related('assessed_by')[:20]
        context['latest_vitals'] = self.object.vital_signs.first()
        return context


class MonitoringSessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Yangi monitoring sessiyasini boshlash"""

    model = MonitoringSession
    form_class = MonitoringSessionForm
    template_name = 'monitoring/session_form.html'
    success_message = 'Monitoring sessiyasi boshlandi'

    def get_initial(self):
        initial = super().get_initial()
        patient_pk = self.request.GET.get('patient')
        if patient_pk:
            initial['patient'] = patient_pk
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('monitoring-session-detail', kwargs={'pk': self.object.pk})


class MonitoringSessionCloseView(LoginRequiredMixin, View):
    """Monitoring sessiyasini yakunlash"""

    def post(self, request, pk):
        session = get_object_or_404(MonitoringSession, pk=pk)
        if session.is_active:
            session.is_active = False
            session.end_date = timezone.now()
            session.save(update_fields=['is_active', 'end_date'])
            messages.success(request, 'Monitoring sessiyasi yakunlandi')
        else:
            messages.info(request, 'Bu sessiya allaqachon yakunlangan')
        return redirect('monitoring-session-detail', pk=pk)


class SessionChildCreateMixin(LoginRequiredMixin, SuccessMessageMixin):
    """Sessiyaga bog'liq yozuvlar uchun umumiy mantiq."""

    def dispatch(self, request, *args, **kwargs):
        self.session = get_object_or_404(MonitoringSession, pk=kwargs['session_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['session'] = self.session
        return context

    def form_valid(self, form):
        form.instance.session = self.session
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('monitoring-session-detail', kwargs={'pk': self.session.pk})


class VitalSignsCreateView(SessionChildCreateMixin, CreateView):
    """Hayotiy ko'rsatkichlarni qayd qilish"""

    model = VitalSigns
    form_class = VitalSignsForm
    template_name = 'monitoring/vital_signs_form.html'
    success_message = "Hayotiy ko'rsatkichlar qayd qilindi"

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        return super().form_valid(form)


class NeurologicalAssessmentCreateView(SessionChildCreateMixin, CreateView):
    """Nevrologik baholash qo'shish"""

    model = NeurologicalAssessment
    form_class = NeurologicalAssessmentForm
    template_name = 'monitoring/neurological_assessment_form.html'
    success_message = 'Nevrologik baholash saqlandi'

    def form_valid(self, form):
        form.instance.assessed_by = self.request.user
        return super().form_valid(form)
