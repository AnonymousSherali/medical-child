from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.MonitoringSessionListView.as_view(), name='monitoring-session-list'),
    path('sessions/<int:pk>/', views.MonitoringSessionDetailView.as_view(), name='monitoring-session-detail'),
    path('sessions/<int:session_pk>/vital-signs/create/', views.VitalSignsCreateView.as_view(), name='vital-signs-create'),
    path('sessions/<int:session_pk>/neurological/create/', views.NeurologicalAssessmentCreateView.as_view(), name='neurological-assessment-create'),
]
