from django import forms

from .models import BloodTestResult, LabTest, NeuroProteinResult

DATETIME_INPUT_FORMATS = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']


class LabTestForm(forms.ModelForm):
    """Laboratoriya tahlili formasi"""

    class Meta:
        model = LabTest
        fields = ['patient', 'test_type', 'test_date', 'sample_collected_date', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'test_type': forms.Select(attrs={'class': 'form-select'}),
            'test_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
            'sample_collected_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ('test_date', 'sample_collected_date'):
            self.fields[field].input_formats = DATETIME_INPUT_FORMATS
        self.fields['patient'].queryset = self.fields['patient'].queryset.order_by(
            'last_name', 'first_name'
        )

    def clean(self):
        cleaned = super().clean()
        test_date = cleaned.get('test_date')
        collected = cleaned.get('sample_collected_date')
        if test_date and collected and collected > test_date:
            self.add_error(
                'sample_collected_date',
                "Namuna olingan sana tahlil sanasidan keyin bo'lishi mumkin emas",
            )
        return cleaned


class NeuroProteinResultForm(forms.ModelForm):
    """Neyro-oqsil natijasi formasi"""

    class Meta:
        model = NeuroProteinResult
        fields = [
            'protein_type', 'value', 'unit',
            'reference_range_min', 'reference_range_max',
            'interpretation',
        ]
        widgets = {
            'protein_type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ng/ml'}),
            'reference_range_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'reference_range_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'interpretation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value is not None and value < 0:
            raise forms.ValidationError("Qiymat manfiy bo'lishi mumkin emas")
        return value

    def clean(self):
        cleaned = super().clean()
        low = cleaned.get('reference_range_min')
        high = cleaned.get('reference_range_max')
        if low is not None and high is not None and low > high:
            self.add_error(
                'reference_range_max',
                "Me'yoriy diapazon maksimumi minimumdan kichik bo'lishi mumkin emas",
            )
        return cleaned


class BloodTestResultForm(forms.ModelForm):
    """Qon tahlili natijasi formasi"""

    class Meta:
        model = BloodTestResult
        fields = [
            'hemoglobin', 'rbc', 'wbc', 'platelets',
            'glucose', 'creatinine', 'bilirubin', 'notes',
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

    def clean(self):
        cleaned = super().clean()
        measured = [
            cleaned.get(name)
            for name in (
                'hemoglobin', 'rbc', 'wbc', 'platelets',
                'glucose', 'creatinine', 'bilirubin',
            )
        ]
        if all(value is None for value in measured):
            raise forms.ValidationError("Kamida bitta ko'rsatkichni kiriting")
        return cleaned
