from django import forms

from .models import MonitoringSession, NeurologicalAssessment, VitalSigns


class MonitoringSessionForm(forms.ModelForm):
    """Monitoring sessiyasini boshlash formasi"""

    class Meta:
        model = MonitoringSession
        fields = ['patient', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = self.fields['patient'].queryset.filter(
            is_active=True
        ).order_by('last_name', 'first_name')

    def clean_patient(self):
        patient = self.cleaned_data.get('patient')
        if patient and MonitoringSession.objects.filter(patient=patient, is_active=True).exists():
            raise forms.ValidationError('Bu bemor uchun allaqachon faol monitoring sessiyasi mavjud')
        return patient


class VitalSignsForm(forms.ModelForm):
    """Hayotiy ko'rsatkichlarni qayd qilish formasi"""

    class Meta:
        model = VitalSigns
        fields = [
            'heart_rate', 'respiratory_rate', 'temperature',
            'blood_pressure_systolic', 'blood_pressure_diastolic',
            'oxygen_saturation',
        ]
        widgets = {
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '300'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '150'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'blood_pressure_systolic': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'blood_pressure_diastolic': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'oxygen_saturation': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}
            ),
        }

    def clean_heart_rate(self):
        value = self.cleaned_data.get('heart_rate')
        if value is not None and not 0 < value <= 300:
            raise forms.ValidationError("Yurak urishi 1 va 300 bpm orasida bo'lishi kerak")
        return value

    def clean_respiratory_rate(self):
        value = self.cleaned_data.get('respiratory_rate')
        if value is not None and not 0 < value <= 150:
            raise forms.ValidationError("Nafas olish 1 va 150 rpm orasida bo'lishi kerak")
        return value

    def clean_temperature(self):
        value = self.cleaned_data.get('temperature')
        if value is not None and not 25 <= value <= 45:
            raise forms.ValidationError("Harorat 25 va 45 °C orasida bo'lishi kerak")
        return value

    def clean_oxygen_saturation(self):
        value = self.cleaned_data.get('oxygen_saturation')
        if value is not None and not 0 <= value <= 100:
            raise forms.ValidationError("Kislorod to'yinganligi 0 va 100 % orasida bo'lishi kerak")
        return value

    def clean(self):
        cleaned = super().clean()
        systolic = cleaned.get('blood_pressure_systolic')
        diastolic = cleaned.get('blood_pressure_diastolic')
        if systolic is not None and diastolic is not None and diastolic >= systolic:
            self.add_error(
                'blood_pressure_diastolic',
                "Diastolik bosim sistolik bosimdan kichik bo'lishi kerak",
            )
        return cleaned


class NeurologicalAssessmentForm(forms.ModelForm):
    """Nevrologik baholash formasi"""

    class Meta:
        model = NeurologicalAssessment
        fields = [
            'consciousness_level', 'muscle_tone', 'reflexes',
            'seizure_activity', 'seizure_description',
            'fontanelle_status', 'pupil_response', 'assessment_notes',
        ]
        widgets = {
            'consciousness_level': forms.TextInput(attrs={'class': 'form-control'}),
            'muscle_tone': forms.TextInput(attrs={'class': 'form-control'}),
            'reflexes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'seizure_activity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'seizure_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fontanelle_status': forms.TextInput(attrs={'class': 'form-control'}),
            'pupil_response': forms.TextInput(attrs={'class': 'form-control'}),
            'assessment_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('seizure_activity') and not cleaned.get('seizure_description'):
            self.add_error(
                'seizure_description',
                "Tutqanoq faolligi belgilangan bo'lsa, uning tavsifini kiriting",
            )
        return cleaned
