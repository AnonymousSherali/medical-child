from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from .forms import BloodTestResultForm, LabTestForm, NeuroProteinResultForm
from .models import BloodTestResult, LabTest, NeuroProteinResult


class LabTestListView(LoginRequiredMixin, ListView):
    """Laboratoriya tahlillari ro'yxati — tur va holat bo'yicha filtr bilan."""

    model = LabTest
    template_name = 'laboratory/labtest_list.html'
    context_object_name = 'tests'
    paginate_by = 20

    def get_queryset(self):
        queryset = LabTest.objects.select_related('patient', 'ordered_by')
        test_type = self.request.GET.get('test_type')
        if test_type:
            queryset = queryset.filter(test_type=test_type)
        status = self.request.GET.get('status')
        if status == 'completed':
            queryset = queryset.filter(is_completed=True)
        elif status == 'pending':
            queryset = queryset.filter(is_completed=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_types'] = LabTest.TEST_TYPE_CHOICES
        context['selected_type'] = self.request.GET.get('test_type', '')
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class LabTestDetailView(LoginRequiredMixin, DetailView):
    """Laboratoriya tahlili tafsilotlari"""

    model = LabTest
    template_name = 'laboratory/labtest_detail.html'
    context_object_name = 'test'

    def get_queryset(self):
        return LabTest.objects.select_related(
            'patient', 'ordered_by', 'performed_by'
        ).prefetch_related('neuro_protein_results', 'blood_test_results')


class LabTestCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Yangi tahlil buyurtmasi"""

    model = LabTest
    form_class = LabTestForm
    template_name = 'laboratory/labtest_form.html'
    success_message = 'Tahlil buyurtmasi yaratildi'

    def get_initial(self):
        initial = super().get_initial()
        patient_pk = self.request.GET.get('patient')
        if patient_pk:
            initial['patient'] = patient_pk
        return initial

    def form_valid(self, form):
        form.instance.ordered_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('labtest-detail', kwargs={'pk': self.object.pk})


class LabTestResultCreateMixin(LoginRequiredMixin, SuccessMessageMixin):
    """Natija formalari uchun umumiy tahlilni yuklash mantiqi."""

    def dispatch(self, request, *args, **kwargs):
        # .get() 500 qaytarardi, endi 404
        self.lab_test = get_object_or_404(LabTest, pk=kwargs['test_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab_test'] = self.lab_test
        return context

    def form_valid(self, form):
        form.instance.lab_test = self.lab_test
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('labtest-detail', kwargs={'pk': self.lab_test.pk})


class NeuroProteinResultCreateView(LabTestResultCreateMixin, CreateView):
    """Neyro-oqsil natijasini kiritish"""

    model = NeuroProteinResult
    form_class = NeuroProteinResultForm
    template_name = 'laboratory/neuroprotein_form.html'
    success_message = 'Neyro-oqsil natijasi saqlandi'


class BloodTestResultCreateView(LabTestResultCreateMixin, CreateView):
    """Qon tahlili natijasini kiritish"""

    model = BloodTestResult
    form_class = BloodTestResultForm
    template_name = 'laboratory/blood_form.html'
    success_message = 'Qon tahlili natijasi saqlandi'


class LabTestCompleteView(LoginRequiredMixin, View):
    """Tahlilni tugallangan deb belgilash."""

    def post(self, request, pk):
        test = get_object_or_404(LabTest, pk=pk)
        test.is_completed = True
        test.performed_by = request.user
        test.save(update_fields=['is_completed', 'performed_by', 'updated_at'])
        messages.success(request, 'Tahlil tugallangan deb belgilandi')
        return redirect('labtest-detail', pk=pk)


class NeuroProteinResultListView(LoginRequiredMixin, ListView):
    """Neyro-oqsil natijalari ro'yxati"""

    model = NeuroProteinResult
    template_name = 'laboratory/neuroprotein_list.html'
    context_object_name = 'results'
    paginate_by = 20

    def get_queryset(self):
        queryset = NeuroProteinResult.objects.select_related('lab_test', 'lab_test__patient')
        protein_type = self.request.GET.get('protein_type')
        if protein_type:
            queryset = queryset.filter(protein_type=protein_type)
        if self.request.GET.get('abnormal') == '1':
            queryset = queryset.filter(is_abnormal=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protein_types'] = NeuroProteinResult.PROTEIN_TYPE_CHOICES
        context['selected_protein'] = self.request.GET.get('protein_type', '')
        context['abnormal_only'] = self.request.GET.get('abnormal') == '1'
        return context
