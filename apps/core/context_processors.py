from datetime import timedelta

from django.utils import timezone

# URL nomi -> yon menyudagi bo'lim. Ro'yxatda yo'q nomlar view moduli bo'yicha aniqlanadi.
_SECTION_BY_URL_NAME = {
    'dashboard': 'dashboard',
    'neuroprotein-list': 'neuroprotein',
    'neuroprotein-create': 'laboratory',
    'report-list': 'reports',
    'report-detail': 'reports',
    'statistics': 'reports',
    'help': 'help',
    'profile': 'profile',
    'password-change': 'profile',
    'register': 'staff',
}


def navigation(request):
    """Yon menyuda faol bo'limni belgilash va ogohlantirish nishonlari uchun ma'lumot."""
    section = ''
    match = getattr(request, 'resolver_match', None)
    if match is not None:
        section = _SECTION_BY_URL_NAME.get(match.url_name or '')
        if not section:
            # 'apps.patients.views' -> 'patients'
            parts = (getattr(match.func, '__module__', '') or '').split('.')
            section = parts[1] if len(parts) > 2 and parts[0] == 'apps' else ''

    context = {'nav_section': section}

    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated:
        # Import shu yerda: context processor ilova yuklanishidan oldin import qilinadi
        from apps.laboratory.models import NeuroProteinResult
        from apps.monitoring.models import MonitoringSession

        week_ago = timezone.now() - timedelta(days=7)
        context['nav_recent_abnormal'] = NeuroProteinResult.objects.filter(
            is_abnormal=True, created_at__gte=week_ago
        ).count()
        context['nav_active_sessions'] = MonitoringSession.objects.filter(is_active=True).count()
    return context
