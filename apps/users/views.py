from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserCreationForm, ProfileForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class RegisterView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Yangi xodim hisobini yaratish — faqat administratorlar uchun.

    Avval bu sahifa ochiq edi: istalgan odam o'zini "Administrator" roli bilan
    ro'yxatdan o'tkazib, barcha bemorlar ma'lumotlarini ko'ra olardi.
    """

    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('register')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"{self.object.get_full_name() or self.object.username} hisobi yaratildi",
        )
        return response


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Foydalanuvchi o'z profilini ko'radi va tahrirlaydi."""

    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')
    success_message = "Profil ma'lumotlari saqlandi"

    def get_object(self, queryset=None):
        return self.request.user


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = "Parol muvaffaqiyatli o'zgartirildi"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
        return form
