from django import forms

from .models import MedicalHistory, Patient

DATETIME_INPUT_FORMATS = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']


class PatientForm(forms.ModelForm):
    """Yangi bemor qo'shish formasi.

    Status maydonlari (is_active, discharge_date) ataylab yo'q: ular template'da
    faqat tahrirlashda ko'rsatilardi, natijada yangi bemor POST'da is_active
    kelmagani uchun False bo'lib saqlanar va dashboardda ko'rinmasdi.
    """

    class Meta:
        model = Patient
        fields = [
            'medical_record_number', 'first_name', 'last_name', 'gender', 'birth_date',
            'gestational_age', 'birth_weight', 'birth_length', 'head_circumference',
            'apgar_score_1min', 'apgar_score_5min',
            'mother_name', 'mother_age', 'mother_phone',
            'diagnosis', 'complications', 'treatment_plan',
        ]
        widgets = {
            'medical_record_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'gestational_age': forms.NumberInput(attrs={'class': 'form-control', 'min': '20', 'max': '44'}),
            'birth_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'birth_length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'head_circumference': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'apgar_score_1min': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'apgar_score_5min': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_age': forms.NumberInput(attrs={'class': 'form-control', 'min': '15', 'max': '60'}),
            'mother_phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}
            ),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'complications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # datetime-local input mavjud qiymatni faqat shu formatda tanaydi
        self.fields['birth_date'].input_formats = DATETIME_INPUT_FORMATS

    def clean_gestational_age(self):
        age = self.cleaned_data.get('gestational_age')
        if age is not None and not 20 <= age <= 44:
            raise forms.ValidationError("Gestatsion yoshi 20 va 44 hafta orasida bo'lishi kerak")
        return age

    def clean_birth_weight(self):
        weight = self.cleaned_data.get('birth_weight')
        if weight is not None and not 0 < weight <= 10:
            raise forms.ValidationError("Tug'ilish og'irligi 0 va 10 kg orasida bo'lishi kerak")
        return weight

    def clean_birth_date(self):
        from django.utils import timezone

        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now():
            raise forms.ValidationError("Tug'ilgan sana kelajakda bo'lishi mumkin emas")
        return birth_date

    def _clean_apgar(self, field_name):
        score = self.cleaned_data.get(field_name)
        if score is not None and not 0 <= score <= 10:
            raise forms.ValidationError("Apgar ko'rsatkichi 0 va 10 orasida bo'lishi kerak")
        return score

    def clean_apgar_score_1min(self):
        return self._clean_apgar('apgar_score_1min')

    def clean_apgar_score_5min(self):
        return self._clean_apgar('apgar_score_5min')


class PatientUpdateForm(PatientForm):
    """Bemorni tahrirlash formasi — chiqarish holatini ham boshqaradi."""

    class Meta(PatientForm.Meta):
        fields = PatientForm.Meta.fields + ['is_active', 'discharge_date']
        widgets = {
            **PatientForm.Meta.widgets,
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'discharge_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discharge_date'].input_formats = DATETIME_INPUT_FORMATS

    def clean(self):
        cleaned = super().clean()
        birth_date = cleaned.get('birth_date')
        discharge_date = cleaned.get('discharge_date')
        is_active = cleaned.get('is_active')

        if discharge_date and birth_date and discharge_date < birth_date:
            self.add_error(
                'discharge_date', "Chiqarilgan sana tug'ilgan sanadan oldin bo'lishi mumkin emas"
            )

        if discharge_date and is_active:
            self.add_error('is_active', "Chiqarilgan sana kiritilgan bemor faol bo'lib qololmaydi")

        if not is_active and not discharge_date:
            self.add_error('discharge_date', "Faol bo'lmagan bemor uchun chiqarilgan sanani kiriting")

        return cleaned


class MedicalHistoryForm(forms.ModelForm):
    """Tibbiy tarix formasi"""

    class Meta:
        model = MedicalHistory
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
