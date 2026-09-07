from django.urls import path

from . import views

urlpatterns = [
    path('tests/', views.LabTestListView.as_view(), name='labtest-list'),
    path('tests/create/', views.LabTestCreateView.as_view(), name='labtest-create'),
    path('tests/<int:pk>/', views.LabTestDetailView.as_view(), name='labtest-detail'),
    path('tests/<int:pk>/complete/', views.LabTestCompleteView.as_view(), name='labtest-complete'),
    path(
        'tests/<int:test_pk>/neuroprotein/add/',
        views.NeuroProteinResultCreateView.as_view(),
        name='neuroprotein-create',
    ),
    path(
        'tests/<int:test_pk>/blood/add/',
        views.BloodTestResultCreateView.as_view(),
        name='blood-create',
    ),
    path('neuroprotein/', views.NeuroProteinResultListView.as_view(), name='neuroprotein-list'),
]
