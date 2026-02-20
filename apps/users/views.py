from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
