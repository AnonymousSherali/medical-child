from django.contrib import admin
from .models import LabTest, NeuroProteinResult, BloodTestResult


class NeuroProteinResultInline(admin.TabularInline):
    model = NeuroProteinResult
    extra = 1
    readonly_fields = ['is_abnormal', 'created_at']


class BloodTestResultInline(admin.StackedInline):
    model = BloodTestResult
    extra = 0


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = [
        'patient',
        'test_type',
        'test_date',
        'is_completed',
        'ordered_by'
    ]
    list_filter = ['test_type', 'is_completed', 'test_date']
    search_fields = ['patient__first_name', 'patient__last_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [NeuroProteinResultInline, BloodTestResultInline]

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('patient', 'test_type', 'test_date', 'sample_collected_date')
        }),
        ('Status', {
            'fields': ('is_completed', 'notes')
        }),
        ('Meta', {
            'fields': ('ordered_by', 'performed_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NeuroProteinResult)
class NeuroProteinResultAdmin(admin.ModelAdmin):
    list_display = [
        'lab_test',
        'protein_type',
        'value',
        'unit',
        'is_abnormal',
        'created_at'
    ]
    list_filter = ['protein_type', 'is_abnormal', 'created_at']
    search_fields = ['lab_test__patient__first_name', 'lab_test__patient__last_name']
    readonly_fields = ['is_abnormal', 'created_at']


@admin.register(BloodTestResult)
class BloodTestResultAdmin(admin.ModelAdmin):
    list_display = [
        'lab_test',
        'hemoglobin',
        'wbc',
        'platelets',
        'glucose'
    ]
    search_fields = ['lab_test__patient__first_name', 'lab_test__patient__last_name']
