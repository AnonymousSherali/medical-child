from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('patients/', views.PatientListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('patients/create/', views.PatientCreateView.as_view(), name='patient-create'),
    path('patients/<int:pk>/update/', views.PatientUpdateView.as_view(), name='patient-update'),
]
