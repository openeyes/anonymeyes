import collections
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.http import HttpResponseRedirect
from django.forms.models import construct_instance
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from anonymeyes.admin import PatientAdminForm
from anonymeyes.forms import PatientForm, PatientManagementFormSet, PatientOutcomeFormSet, PatientUpdateManagementFormSet, PatientUpdateOutcomeFormSet
from anonymeyes.models import Patient, Management

class IndexView(TemplateView):
    template_name='anonymeyes/index.html'

class PatientWizard(NamedUrlSessionWizardView):
    def done(self, form_list, **kwargs):
        
        # Save patient
        patient = Patient()
        for form in form_list:
            patient = construct_instance(form, patient)
        patient.created_by = self.request.user
        patient.updated_by = self.request.user
        patient.save()

        # Save management records
        for management_record in form_list[1].save(commit=False):
            management_record.patient = patient
            management_record.created_by = self.request.user
            management_record.updated_by = self.request.user
            management_record.save()

        # Save outcome records
        for outcome_record in form_list[2].save(commit=False):
            outcome_record.patient = patient
            outcome_record.created_by = self.request.user
            outcome_record.updated_by = self.request.user
            outcome_record.save()

        return render(self.request, 'thanks.html', { "patient": patient })

@login_required
def wizard(request, **kwargs):
    forms = (
             ('patient', PatientForm),
             ('management', PatientManagementFormSet),
             ('outcome', PatientOutcomeFormSet),
             )
    wizard = PatientWizard.as_view(forms, url_name='wizard_step')
    return wizard(request, **kwargs)

class PatientCreateView(CreateView):
    form_class = PatientForm
    model = Patient

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        context = self.get_context_data()
        management_formset = context['formsets']['Management']
        outcome_formset = context['formsets']['Outcome']
        if management_formset.is_valid() and outcome_formset.is_valid():
            response = super(PatientCreateView, self).form_valid(form)
            management_formset.instance = self.object
            for management_instance in management_formset.save(commit=False):
                management_instance.created_by = self.request.user
                management_instance.updated_by = self.request.user
                management_instance.save()
            outcome_formset.instance = self.object
            for outcome_instance in outcome_formset.save(commit=False):
                outcome_instance.created_by = self.request.user
                outcome_instance.updated_by = self.request.user
                outcome_instance.save()
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(PatientCreateView, self).get_context_data(**kwargs)
        if 'formsets' not in context:
            context['formsets'] = collections.OrderedDict()
        if self.request.POST:
            context['formsets']['Management'] = PatientManagementFormSet(self.request.POST)
            context['formsets']['Outcome'] = PatientOutcomeFormSet(self.request.POST)
        else:
            context['formsets']['Management'] = PatientManagementFormSet()
            context['formsets']['Outcome'] = PatientOutcomeFormSet()
        return context

class PatientUpdateView(UpdateView):
    form_class = PatientForm
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
     
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        context = self.get_context_data()
        management_formset = context['formsets']['Management']
        outcome_formset = context['formsets']['Outcome']
        if management_formset.is_valid() and outcome_formset.is_valid():
            management_formset.instance = self.object
            for management_instance in management_formset.save(commit=False):
                management_instance.updated_by = self.request.user
                management_instance.save()
            outcome_formset.instance = self.object
            for outcome_instance in outcome_formset.save(commit=False):
                outcome_instance.updated_by = self.request.user
                outcome_instance.save()
            return super(PatientUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    
    def get_context_data(self, **kwargs):
        context = super(PatientUpdateView, self).get_context_data(**kwargs)
        if 'formsets' not in context:
            context['formsets'] = collections.OrderedDict()
        if self.request.POST:
            context['formsets']['Management'] = PatientUpdateManagementFormSet(self.request.POST, instance=self.object)
            context['formsets']['Outcome'] = PatientUpdateOutcomeFormSet(self.request.POST, instance=self.object)
        else:
            context['formsets']['Management'] = PatientUpdateManagementFormSet(instance=self.object)
            context['formsets']['Outcome'] = PatientUpdateOutcomeFormSet(instance=self.object)
        return context

class PatientListView(ListView):
     context_object_name='patients'
     
     def get_queryset(self):
          return Patient.objects.filter(created_by=self.request.user)
     
     @method_decorator(login_required)
     def dispatch(self, request, *args, **kwargs):
         return super(PatientListView, self).dispatch(request, *args, **kwargs)

class PatientDetailView(DetailView):
     context_object_name='patient'
     
     def get_queryset(self):
          return Patient.objects.filter(created_by=self.request.user)
     
     @method_decorator(login_required)
     def dispatch(self, request, *args, **kwargs):
         return super(PatientDetailView, self).dispatch(request, *args, **kwargs)

