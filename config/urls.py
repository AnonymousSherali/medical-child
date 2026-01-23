"""
URL configuration for NeuroMonitor project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.patients.urls')),
    path('monitoring/', include('apps.monitoring.urls')),
    path('laboratory/', include('apps.laboratory.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('accounts/', include('apps.users.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "NeuroMonitor Admin"
admin.site.site_title = "NeuroMonitor"
admin.site.index_title = "Tizim boshqaruvi"
