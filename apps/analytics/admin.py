from django.contrib import admin
from .models import Report, Statistics


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'report_type',
        'patient',
        'created_by',
        'created_at',
        'is_generated'
    ]
    list_filter = ['report_type', 'is_generated', 'created_at']
    search_fields = ['title', 'description', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['created_at']


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'total_patients',
        'active_patients',
        'total_tests',
        'abnormal_results'
    ]
    list_filter = ['date']
    readonly_fields = ['date']
