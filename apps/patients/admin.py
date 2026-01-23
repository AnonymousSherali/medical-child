from django.contrib import admin
from .models import Patient, MedicalHistory


class MedicalHistoryInline(admin.TabularInline):
    model = MedicalHistory
    extra = 0
    readonly_fields = ['date']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        'medical_record_number',
        'first_name',
        'last_name',
        'gender',
        'birth_date',
        'gestational_age',
        'is_active'
    ]
    list_filter = ['gender', 'is_active', 'admission_date']
    search_fields = ['medical_record_number', 'first_name', 'last_name', 'mother_name']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    inlines = [MedicalHistoryInline]

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('medical_record_number', 'first_name', 'last_name', 'gender', 'birth_date')
        }),
        ('Tug\'ilish parametrlari', {
            'fields': (
                'gestational_age',
                'birth_weight',
                'birth_length',
                'head_circumference',
                'apgar_score_1min',
                'apgar_score_5min'
            )
        }),
        ('Ona ma\'lumotlari', {
            'fields': ('mother_name', 'mother_age', 'mother_phone')
        }),
        ('Tibbiy ma\'lumotlar', {
            'fields': ('diagnosis', 'complications', 'treatment_plan')
        }),
        ('Status', {
            'fields': ('is_active', 'admission_date', 'discharge_date')
        }),
        ('Meta', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'doctor']
    list_filter = ['date']
    search_fields = ['patient__first_name', 'patient__last_name', 'description']
    readonly_fields = ['date']
