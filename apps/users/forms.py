from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """CustomUser uchun registratsiya formasi"""

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'phone', 'department')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
