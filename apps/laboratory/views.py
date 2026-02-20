from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import LabTest, NeuroProteinResult, BloodTestResult
from .forms import LabTestForm, NeuroProteinResultForm, BloodTestResultForm


class LabTestListView(LoginRequiredMixin, ListView):
    model = LabTest
    template_name = 'laboratory/labtest_list.html'
    context_object_name = 'tests'
    paginate_by = 20


class LabTestDetailView(LoginRequiredMixin, DetailView):
    model = LabTest
    template_name = 'laboratory/labtest_detail.html'
    context_object_name = 'test'


class LabTestCreateView(LoginRequiredMixin, CreateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'laboratory/labtest_form.html'
    success_url = reverse_lazy('labtest-list')

    def form_valid(self, form):
        form.instance.ordered_by = self.request.user
        return super().form_valid(form)


class NeuroProteinResultCreateView(LoginRequiredMixin, CreateView):
    model = NeuroProteinResult
    form_class = NeuroProteinResultForm
    template_name = 'laboratory/neuroprotein_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab_test'] = LabTest.objects.get(pk=self.kwargs['test_pk'])
        return context

    def form_valid(self, form):
        form.instance.lab_test = LabTest.objects.get(pk=self.kwargs['test_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('labtest-detail', kwargs={'pk': self.kwargs['test_pk']})


class BloodTestResultCreateView(LoginRequiredMixin, CreateView):
    model = BloodTestResult
    form_class = BloodTestResultForm
    template_name = 'laboratory/blood_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab_test'] = LabTest.objects.get(pk=self.kwargs['test_pk'])
        return context

    def form_valid(self, form):
        form.instance.lab_test = LabTest.objects.get(pk=self.kwargs['test_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('labtest-detail', kwargs={'pk': self.kwargs['test_pk']})


class NeuroProteinResultListView(LoginRequiredMixin, ListView):
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
