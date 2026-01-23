from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import LabTest, NeuroProteinResult


class LabTestListView(LoginRequiredMixin, ListView):
    """Laboratoriya tahillari ro'yxati"""
    model = LabTest
    template_name = 'laboratory/labtest_list.html'
    context_object_name = 'tests'
    paginate_by = 20


class LabTestDetailView(LoginRequiredMixin, DetailView):
    """Laboratoriya tahlili tafsilotlari"""
    model = LabTest
    template_name = 'laboratory/labtest_detail.html'
    context_object_name = 'test'


class LabTestCreateView(LoginRequiredMixin, CreateView):
    """Yangi tahlil qo'shish"""
    model = LabTest
    template_name = 'laboratory/labtest_form.html'
    fields = ['patient', 'test_type', 'test_date', 'sample_collected_date', 'notes']
    success_url = reverse_lazy('labtest-list')

    def form_valid(self, form):
        form.instance.ordered_by = self.request.user
        return super().form_valid(form)


class NeuroProteinResultListView(LoginRequiredMixin, ListView):
    """Neyro-oqsil natijalari ro'yxati"""
    model = NeuroProteinResult
    template_name = 'laboratory/neuroprotein_list.html'
    context_object_name = 'results'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        protein_type = self.request.GET.get('protein_type')
        if protein_type:
            queryset = queryset.filter(protein_type=protein_type)
        return queryset
