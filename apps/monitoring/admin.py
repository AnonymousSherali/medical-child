from django.contrib import admin
from .models import MonitoringSession, VitalSigns, NeurologicalAssessment


class VitalSignsInline(admin.TabularInline):
    model = VitalSigns
    extra = 0
    readonly_fields = ['timestamp']


class NeurologicalAssessmentInline(admin.StackedInline):
    model = NeurologicalAssessment
    extra = 0
    readonly_fields = ['assessment_date']


@admin.register(MonitoringSession)
class MonitoringSessionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'start_date', 'end_date', 'is_active', 'created_by']
    list_filter = ['is_active', 'start_date']
    search_fields = ['patient__first_name', 'patient__last_name']
    readonly_fields = ['start_date', 'created_by']
    inlines = [VitalSignsInline, NeurologicalAssessmentInline]


@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = [
        'session',
        'timestamp',
        'heart_rate',
        'respiratory_rate',
        'temperature',
        'oxygen_saturation'
    ]
    list_filter = ['timestamp']
    search_fields = ['session__patient__first_name', 'session__patient__last_name']
    readonly_fields = ['timestamp']


@admin.register(NeurologicalAssessment)
class NeurologicalAssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'session',
        'assessment_date',
        'consciousness_level',
        'seizure_activity',
        'assessed_by'
    ]
    list_filter = ['assessment_date', 'seizure_activity']
    search_fields = ['session__patient__first_name', 'session__patient__last_name']
    readonly_fields = ['assessment_date']
