from django import forms
from .models import Patient, MedicalHistory


class PatientForm(forms.ModelForm):
    """Bemor formasi"""

    class Meta:
        model = Patient
        fields = [
            'medical_record_number', 'first_name', 'last_name', 'gender', 'birth_date',
            'gestational_age', 'birth_weight', 'birth_length', 'head_circumference',
            'apgar_score_1min', 'apgar_score_5min',
            'mother_name', 'mother_age', 'mother_phone',
            'diagnosis', 'complications', 'treatment_plan'
        ]
        widgets = {
            'medical_record_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'gestational_age': forms.NumberInput(attrs={'class': 'form-control', 'min': '20', 'max': '44'}),
            'birth_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'birth_length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'head_circumference': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'apgar_score_1min': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'apgar_score_5min': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_age': forms.NumberInput(attrs={'class': 'form-control', 'min': '15', 'max': '60'}),
            'mother_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'complications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_gestational_age(self):
        """Gestatsion yoshni tekshirish"""
        age = self.cleaned_data.get('gestational_age')
        if age and (age < 20 or age > 44):
            raise forms.ValidationError('Gestatsion yoshi 20 va 44 hafta orasida bo\'lishi kerak')
        return age

    def clean_apgar_score_1min(self):
        """Apgar 1 min ni tekshirish"""
        score = self.cleaned_data.get('apgar_score_1min')
        if score is not None and (score < 0 or score > 10):
            raise forms.ValidationError('Apgar ko\'rsatkichi 0 va 10 orasida bo\'lishi kerak')
        return score

    def clean_apgar_score_5min(self):
        """Apgar 5 min ni tekshirish"""
        score = self.cleaned_data.get('apgar_score_5min')
        if score is not None and (score < 0 or score > 10):
            raise forms.ValidationError('Apgar ko\'rsatkichi 0 va 10 orasida bo\'lishi kerak')
        return score


class MedicalHistoryForm(forms.ModelForm):
    """Tibbiy tarix formasi"""

    class Meta:
        model = MedicalHistory
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
