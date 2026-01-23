from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg
from .models import Report, Statistics
from apps.patients.models import Patient
from apps.laboratory.models import LabTest, NeuroProteinResult


class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    """Analitika dashboard"""
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Umumiy statistika
        context['total_patients'] = Patient.objects.count()
        context['active_patients'] = Patient.objects.filter(is_active=True).count()
        context['total_tests'] = LabTest.objects.count()
        context['completed_tests'] = LabTest.objects.filter(is_completed=True).count()

        # Neyro-oqsillar bo'yicha statistika
        context['abnormal_results'] = NeuroProteinResult.objects.filter(is_abnormal=True).count()

        # Oxirgi hisobotlar
        context['recent_reports'] = Report.objects.all()[:5]

        return context


class ReportListView(LoginRequiredMixin, ListView):
    """Hisobotlar ro'yxati"""
    model = Report
    template_name = 'analytics/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20


class ReportDetailView(LoginRequiredMixin, DetailView):
    """Hisobot tafsilotlari"""
    model = Report
    template_name = 'analytics/report_detail.html'
    context_object_name = 'report'


class StatisticsView(LoginRequiredMixin, ListView):
    """Statistika ko'rinishi"""
    model = Statistics
    template_name = 'analytics/statistics.html'
    context_object_name = 'statistics'
    paginate_by = 30
