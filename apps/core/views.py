from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HelpView(LoginRequiredMixin, TemplateView):
    """Foydalanuvchi qo'llanmasi va tibbiy atamalar lug'ati."""

    template_name = 'core/help.html'
