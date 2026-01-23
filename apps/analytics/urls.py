from django.urls import path
from . import views

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    path('reports/', views.ReportListView.as_view(), name='report-list'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
]
