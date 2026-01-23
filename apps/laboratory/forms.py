from django import forms
from .models import LabTest, NeuroProteinResult, BloodTestResult


class LabTestForm(forms.ModelForm):
    """Laboratoriya tahlili formasi"""

    class Meta:
        model = LabTest
        fields = ['patient', 'test_type', 'test_date', 'sample_collected_date', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'test_type': forms.Select(attrs={'class': 'form-select'}),
            'test_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'sample_collected_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class NeuroProteinResultForm(forms.ModelForm):
    """Neyro-oqsil natijasi formasi"""

    class Meta:
        model = NeuroProteinResult
        fields = [
            'protein_type', 'value', 'unit',
            'reference_range_min', 'reference_range_max',
            'interpretation'
        ]
        widgets = {
            'protein_type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ng/ml'}),
            'reference_range_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'reference_range_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'interpretation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BloodTestResultForm(forms.ModelForm):
    """Qon tahlili natijasi formasi"""

    class Meta:
        model = BloodTestResult
        fields = [
            'hemoglobin', 'rbc', 'wbc', 'platelets',
            'glucose', 'creatinine', 'bilirubin', 'notes'
        ]
        widgets = {
            'hemoglobin': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'rbc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'wbc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'platelets': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'glucose': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'creatinine': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bilirubin': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
