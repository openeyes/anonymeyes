try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.forms.models import construct_instance
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView, CreateView, FormView, DeleteView, RedirectView
from django.views.generic.detail import BaseDetailView
from django.utils import simplejson as json
from django.utils.decorators import method_decorator
from django.contrib.sites.models import get_current_site
from apps.anonymeyes.admin import PatientAdminForm
from apps.anonymeyes.forms import *
from apps.anonymeyes.models import Patient, Management, VisualAcuityReading, VisualAcuityScale

class ProfileDetailView(DetailView):
    template_name = 'anonymeyes/profile_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.get_profile()

class ProfileUpdateView(UpdateView):
    template_name = 'anonymeyes/profile_form.html'
    success_url = '/anonymeyes/profile/'
    form_class = ProfileForm
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.get_profile()

class DiagnosesView(BaseDetailView):
    
    model = DiagnosisGroup
    
    def render_to_response(self, context):
        diagnoses = self.object.diagnosis_set.all()
        data = serializers.serialize('json', diagnoses)
        return HttpResponse(data, content_type='application/json')

class IndexView(TemplateView):
    template_name = 'anonymeyes/index.html'

class AboutView(TemplateView):
    template_name = 'anonymeyes/about.html'

class HelpView(TemplateView):
    template_name = 'anonymeyes/help.html'

class ContactView(FormView):
    template_name = 'anonymeyes/contact.html'
    success_url = '/anonymeyes/thanks/'

    def get_form_class(self):
        if self.request.user.is_authenticated():
            return ContactForm
        else:
            return CaptchaContactForm
    
    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)

class ThanksView(TemplateView):
    template_name = 'anonymeyes/thanks.html'

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

    def get_form(self, form_class):
        form = super(PatientCreateView, self).get_form(form_class)
        form.request = self.request
        return form

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
            management_formset.save_m2m()
            outcome_formset.instance = self.object
            for outcome_instance in outcome_formset.save(commit=False):
                outcome_instance.created_by = self.request.user
                outcome_instance.updated_by = self.request.user
                outcome_instance.save()
            outcome_formset.save_m2m()
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form, formsets_invalid=True))

    def get_context_data(self, **kwargs):
        context = super(PatientCreateView, self).get_context_data(**kwargs)
        if 'formsets' not in context:
            context['formsets'] = OrderedDict()
        if self.request.POST:
            context['formsets']['Management'] = PatientManagementFormSet(self.request.POST, prefix='managements')
            context['formsets']['Outcome'] = PatientOutcomeFormSet(self.request.POST, prefix='outcomes')
        else:
            context['formsets']['Management'] = PatientManagementFormSet(prefix='managements')
            context['formsets']['Outcome'] = PatientOutcomeFormSet(prefix='outcomes')
        return context

class PatientUpdateView(UpdateView):
    form_class = PatientForm
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
     
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(PatientUpdateView, self).get_form(form_class)
        form.request = self.request
        return form

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        context = self.get_context_data()
        management_formset = context['formsets']['Management']
        outcome_formset = context['formsets']['Outcome']
        if management_formset.is_valid() and outcome_formset.is_valid():
            management_formset.instance = self.object
            for management_instance in management_formset.save(commit=False):
                if not management_instance.created_by:
                    management_instance.created_by = self.request.user
                management_instance.updated_by = self.request.user
                management_instance.save()
            management_formset.save_m2m()
            outcome_formset.instance = self.object
            for outcome_instance in outcome_formset.save(commit=False):
                if not outcome_instance.created_by:
                    outcome_instance.created_by = self.request.user
                outcome_instance.updated_by = self.request.user
                outcome_instance.save()
            outcome_formset.save_m2m()
            return super(PatientUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formsets_invalid=True))

    
    def get_context_data(self, **kwargs):
        context = super(PatientUpdateView, self).get_context_data(**kwargs)
        if 'formsets' not in context:
            context['formsets'] = OrderedDict()
        if self.request.POST:
            context['formsets']['Management'] = PatientUpdateManagementFormSet(self.request.POST, instance=self.object, prefix='managements')
            context['formsets']['Outcome'] = PatientUpdateOutcomeFormSet(self.request.POST, instance=self.object, prefix='outcomes')
        else:
            context['formsets']['Management'] = PatientUpdateManagementFormSet(instance=self.object, prefix='managements')
            context['formsets']['Outcome'] = PatientUpdateOutcomeFormSet(instance=self.object, prefix='outcomes')
        return context

class VisualAcuityReadingsView(TemplateView):
    template_name = 'anonymeyes/visual_acuity_readings.html'
    
    def get_context_data(self, **kwargs):
        context = super(VisualAcuityReadingsView, self).get_context_data(**kwargs)
        # current_reading_id=(self.request.GET.get('reading_pk')) and int(self.request.GET.get('reading_pk')) or None
        context['readings'] = VisualAcuityScale.objects.get(pk=int(self.kwargs.get('scale_pk'))).readings.all()
        return context

class VisualAcuityScalesView(TemplateView):
    template_name = 'anonymeyes/visual_acuity_scales.html'
    
    def get_context_data(self, **kwargs):
        context = super(VisualAcuityScalesView, self).get_context_data(**kwargs)
        context['scales'] = VisualAcuityMethod.objects.get(pk=int(self.kwargs.get('method_pk'))).scales.all()
        return context

class PatientListView(ListView):
     context_object_name = 'patients'
     
     def get_queryset(self):
          return Patient.objects.filter(created_by=self.request.user)
     
     @method_decorator(login_required)
     def dispatch(self, request, *args, **kwargs):
         return super(PatientListView, self).dispatch(request, *args, **kwargs)

class PatientDetailView(DetailView):
    context_object_name = 'patient'
     
    def get_queryset(self):
          return Patient.objects.filter(created_by=self.request.user)
     
    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        context['patient_url'] = 'http://' + get_current_site(self.request).domain + '/anonymeyes/uuid/' + self.get_object().uuid.lower()
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientDetailView, self).dispatch(request, *args, **kwargs)

class PatientDeleteView(DeleteView):
    context_object_name = 'patient'
    success_url = '/anonymeyes/list/'
     
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
     
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientDeleteView, self).dispatch(request, *args, **kwargs)

class PatientUUIDView(RedirectView):
    def get_redirect_url(self, **kwargs):
        try:
            patient = Patient.objects.get(uuid=kwargs['uuid'])
            return '/anonymeyes/detail/' + str(patient.pk)
        except:
            raise Http404

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientUUIDView, self).dispatch(request, *args, **kwargs)

