import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from apps.laboratory.models import LabTest, NeuroProteinResult
from apps.monitoring.models import MonitoringSession
from apps.patients.models import Patient

from .models import Report, Statistics


class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    """Analitika dashboard — umumiy ko'rsatkichlar va taqsimotlar."""

    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        patients = Patient.objects.all()
        context['total_patients'] = patients.count()
        context['active_patients'] = patients.filter(is_active=True).count()
        context['preterm_patients'] = patients.filter(gestational_age__lt=37).count()
        context['avg_gestational_age'] = patients.aggregate(v=Avg('gestational_age'))['v']
        context['avg_birth_weight'] = patients.aggregate(v=Avg('birth_weight'))['v']

        context['total_tests'] = LabTest.objects.count()
        context['completed_tests'] = LabTest.objects.filter(is_completed=True).count()
        context['pending_tests'] = LabTest.objects.filter(is_completed=False).count()

        results = NeuroProteinResult.objects.all()
        context['total_results'] = results.count()
        context['abnormal_results'] = results.filter(is_abnormal=True).count()

        # Oqsil turi bo'yicha taqsimot
        protein_labels = dict(NeuroProteinResult.PROTEIN_TYPE_CHOICES)
        protein_stats = []
        for row in results.values('protein_type').annotate(total=Count('id')).order_by('protein_type'):
            protein_type = row['protein_type']
            protein_stats.append({
                'label': protein_labels.get(protein_type, protein_type),
                'total': row['total'],
                'abnormal': results.filter(protein_type=protein_type, is_abnormal=True).count(),
                'average': results.filter(protein_type=protein_type).aggregate(v=Avg('value'))['v'],
            })
        context['protein_stats'] = protein_stats

        context['active_sessions'] = MonitoringSession.objects.filter(is_active=True).count()
        context['total_sessions'] = MonitoringSession.objects.count()

        context['recent_reports'] = Report.objects.select_related('patient', 'created_by')[:5]
        context['recent_tests'] = LabTest.objects.select_related('patient')[:5]
        return context


class ReportListView(LoginRequiredMixin, ListView):
    """Hisobotlar ro'yxati"""

    model = Report
    template_name = 'analytics/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20

    def get_queryset(self):
        return Report.objects.select_related('patient', 'created_by')


class ReportDetailView(LoginRequiredMixin, DetailView):
    """Hisobot tafsilotlari"""

    model = Report
    template_name = 'analytics/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return Report.objects.select_related('patient', 'created_by')


class StatisticsView(LoginRequiredMixin, ListView):
    """Kunlik statistika yozuvlari"""

    model = Statistics
    template_name = 'analytics/statistics.html'
    context_object_name = 'statistics'
    paginate_by = 30


class PatientExportView(LoginRequiredMixin, View):
    """Bemorlar ro'yxatini CSV formatda yuklab olish (Excel'da ochiladi)."""

    def get(self, request):
        filename = f"bemorlar-{timezone.localdate():%Y-%m-%d}.csv"
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        # Excel UTF-8 ni to'g'ri o'qishi uchun BOM
        response.write('﻿')

        writer = csv.writer(response)
        writer.writerow([
            'Karta raqami', 'Ism', 'Familiya', 'Jinsi', "Tug'ilgan sana",
            'Gestatsion yoshi (hafta)', "Og'irligi (kg)", "Bo'yi (sm)",
            'Apgar 1 daq', 'Apgar 5 daq', 'Ona FIO', 'Holat',
        ])
        for patient in Patient.objects.all().iterator():
            writer.writerow([
                patient.medical_record_number,
                patient.first_name,
                patient.last_name,
                patient.get_gender_display(),
                timezone.localtime(patient.birth_date).strftime('%Y-%m-%d %H:%M'),
                patient.gestational_age,
                patient.birth_weight,
                patient.birth_length,
                patient.apgar_score_1min,
                patient.apgar_score_5min,
                patient.mother_name,
                'Faol' if patient.is_active else 'Chiqarilgan',
            ])
        return response


class NeuroProteinExportView(LoginRequiredMixin, View):
    """Neyro-oqsil natijalarini CSV formatda yuklab olish."""

    def get(self, request):
        filename = f"neyro-oqsillar-{timezone.localdate():%Y-%m-%d}.csv"
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write('﻿')

        writer = csv.writer(response)
        writer.writerow([
            'Bemor', 'Karta raqami', 'Oqsil turi', 'Qiymat', "O'lchov birligi",
            "Me'yor min", "Me'yor max", 'Holat', 'Tahlil sanasi',
        ])
        queryset = NeuroProteinResult.objects.select_related('lab_test__patient')
        for result in queryset.iterator():
            patient = result.lab_test.patient
            writer.writerow([
                patient.full_name,
                patient.medical_record_number,
                result.get_protein_type_display(),
                result.value,
                result.unit,
                result.reference_range_min if result.reference_range_min is not None else '',
                result.reference_range_max if result.reference_range_max is not None else '',
                "Me'yordan chetlashgan" if result.is_abnormal else "Me'yorda",
                timezone.localtime(result.lab_test.test_date).strftime('%Y-%m-%d %H:%M'),
            ])
        return response
