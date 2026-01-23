from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.LabTestListView.as_view(), name='labtest-list'),
    path('tests/<int:pk>/', views.LabTestDetailView.as_view(), name='labtest-detail'),
    path('tests/create/', views.LabTestCreateView.as_view(), name='labtest-create'),
    path('neuroprotein/', views.NeuroProteinResultListView.as_view(), name='neuroprotein-list'),
]
