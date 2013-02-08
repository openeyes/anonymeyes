from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from captcha.fields import ReCaptchaField
from apps.anonymeyes.models import Patient, Management, Outcome, VisualAcuityReading, VisualAcuityMethod
from form_utils.forms import BetterModelForm
import datetime

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
    def send_email(self):
        message = get_template('anonymeyes/message.txt')
        d = Context(self.cleaned_data)
        send_mail('Message from CGRN contact form', message.render(d), settings.CONTACT_SENDER,
                  settings.CONTACT_RECIPIENTS)

class CaptchaContactForm(ContactForm):
    captcha = ReCaptchaField()

class PatientForm(BetterModelForm):
    class Meta:
        model = Patient
        fieldsets = [
                     ('patient', {
                                  'fields': [ 'sex', 'dob_day', 'dob_month', 'dob_year', 'postcode', 'health_care', 'ethnic_group', 'consanguinity', ],
                                  }),
                     ('baseline', {
                                   'fields': [ 'visual_acuity_date', 'diagnosis_right', 'diagnosis_left', ],
                                   }),
                     ('visual_acuity', {
                                   'fields': [ 'visual_acuity_method',
                                               'visual_acuity_right', 'visual_acuity_correction_right',
                                               'visual_acuity_left', 'visual_acuity_correction_left',
                                               'visual_acuity_both', 'visual_acuity_correction_both', ],
                                   }),
                     ('iop', {
                                   'fields': [ 'iop_right', 'iop_left', 'tonometry', 'eua', 'anaesthesia'],
                                   }),
                     ('lens', {
                                   'fields': [ 'lens_status_right', 'lens_extraction_date_right',
                                              'lens_status_left', 'lens_extraction_date_left', ],
                                   }),
                     ]
        widgets = {
                   'postcode': forms.TextInput(attrs={'size':'10'}),
                   'dob_day': forms.TextInput(attrs={'size':'10'}),
                   'dob_year': forms.TextInput(attrs={'size':'10'}),
                   'lens_extraction_date_right': forms.DateInput(attrs={'class':'datepicker past'}),
                   'lens_extraction_date_left': forms.DateInput(attrs={'class':'datepicker past'}),
                   'visual_acuity_date': forms.DateInput(attrs={'class':'datepicker past'}),
                   'visual_acuity_method': forms.Select(attrs={'class':'visualacuitymethod'}),
                   'visual_acuity_right': forms.Select(attrs={'class':'visualacuity'}),
                   'visual_acuity_left': forms.Select(attrs={'class':'visualacuity'}),
                   'visual_acuity_both': forms.Select(attrs={'class':'visualacuity'}),
                   'iop_right': forms.TextInput(attrs={'class': 'small', 'size':'10'}),
                   'iop_left': forms.TextInput(attrs={'class': 'small', 'size':'10'}),
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PatientForm, self).__init__(*args, **kwargs)
        
        # Filter VisualAcuityReading choices depending upon selected method
        method_id=self.is_bound and self.data['visual_acuity_method'] \
            or 'visual_acuity_method' in self.initial and self.initial['visual_acuity_method']
        if method_id:
            scale_id=VisualAcuityMethod.objects.get(pk=method_id).scale_id
            filtered=VisualAcuityReading.objects.filter(scale_id=scale_id)
        else:
            filtered=VisualAcuityReading.objects.none()
        self.fields['visual_acuity_left'].queryset=filtered
        self.fields['visual_acuity_right'].queryset=filtered
        self.fields['visual_acuity_both'].queryset=filtered
        
    def clean_lens_extraction_date_right(self):
        lens_extraction_date_right = self.cleaned_data.get('lens_extraction_date_right')
        lens_status_right = self.cleaned_data.get('lens_status_right')
        if lens_status_right and lens_status_right.name != 'Aphakia' and lens_status_right.name != 'Pseudophakia':
            return None
        return lens_extraction_date_right
    
    def clean_lens_extraction_date_left(self):
        lens_extraction_date_left = self.cleaned_data.get('lens_extraction_date_left')
        lens_status_left = self.cleaned_data.get('lens_status_left')
        if lens_status_left and lens_status_left.name != 'Aphakia' and lens_status_left.name != 'Pseudophakia':
            return None
        return lens_extraction_date_left

    def clean_anaesthesia(self):
        anaesthesia = self.cleaned_data.get('anaesthesia')
        eua = self.cleaned_data.get('eua')
        if eua != Patient.YES:
            return None
        return anaesthesia

    def clean_dob_month(self):
        dob_month = self.cleaned_data.get('dob_month')
        dob_day = self.cleaned_data.get('dob_day')
        precision = self.request.user.get_profile().dob_precision
        if ((precision and precision.name != 'Year') or dob_day) and dob_month == None:
            raise forms.ValidationError("DOB month required")
        return dob_month

    def clean_dob_day(self):
        dob_day = self.cleaned_data.get('dob_day')
        precision = self.request.user.get_profile().dob_precision
        if precision and precision.name == 'Day' and dob_day == None:
            raise forms.ValidationError("DOB day required")
        return dob_day

    def clean(self):
        cleaned_data = super(PatientForm, self).clean()
        dob_day = int(cleaned_data.get("dob_day") or 1)
        dob_month = int(cleaned_data.get("dob_month") or 1)
        dob_year = int(cleaned_data.get("dob_year") or 0)
        try:
            dob = datetime.datetime(dob_year, dob_month, dob_day)
        except ValueError:
            raise forms.ValidationError("DOB is not valid")
        return cleaned_data
    
class PatientManagementForm(forms.ModelForm):
    class Meta:
        model = Management
        widgets = {
                   'date': forms.DateInput(attrs={'class':'datepicker past'}),
                   'comments': forms.Textarea(attrs={'rows':1}),
        }
        exclude = { 'patient', 'created_by', 'updated_by', }
        
    def clean_surgery(self):
        surgery = self.cleaned_data.get('surgery')
        type = self.cleaned_data.get('type')
        if type and type.name == 'Surgery' and not surgery:
            raise forms.ValidationError("Surgery detail required")
        elif type and type.name != 'Surgery':
            return None
        return surgery

    def clean_complication(self):
        complication = self.cleaned_data.get('complication')
        type = self.cleaned_data.get('type')
        if type and type.name == 'Complication' and not complication:
            raise forms.ValidationError("Complication detail required")
        elif type and type.name != 'Complication':
            return None
        return complication

    def clean_adjuvant(self):
        adjuvant = self.cleaned_data.get('adjuvant')
        surgery = self.cleaned_data.get('surgery')
        if surgery and surgery.adjuvant and not adjuvant:
            raise forms.ValidationError("Adjuvant detail required")
        elif surgery and not surgery.adjuvant:
            return None
        return adjuvant

    def clean_surgery_stage(self):
        surgery_stage = self.cleaned_data.get('surgery_stage')
        surgery = self.cleaned_data.get('surgery')
        if surgery and surgery.stage and not surgery_stage:
            raise forms.ValidationError("Surgery stage detail required")
        elif surgery and not surgery.stage:
            return None
        return surgery_stage

class PatientOutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        widgets = {
                   'date': forms.DateInput(attrs={'class':'datepicker past'}),
                   'visual_acuity_method': forms.Select(attrs={'class':'visualacuitymethod'}),
                   'visual_acuity_right': forms.Select(attrs={'class':'visualacuity'}),
                   'visual_acuity_left': forms.Select(attrs={'class':'visualacuity'}),
                   'visual_acuity_both': forms.Select(attrs={'class':'visualacuity'}),
        }
        exclude = { 'patient', 'created_by', 'updated_by', }

    def __init__(self, *args, **kwargs):
        super(PatientOutcomeForm, self).__init__(*args, **kwargs)
        
        # Filter VisualAcuityReading choices depending upon selected method
        method_id=self.is_bound and self.data['visual_acuity_method'] \
            or 'visual_acuity_method' in self.initial and self.initial['visual_acuity_method']
        if method_id:
            scale_id=VisualAcuityMethod.objects.get(pk=method_id).scale_id
            filtered=VisualAcuityReading.objects.filter(scale_id=scale_id)
        else:
            filtered=VisualAcuityReading.objects.none()
        self.fields['visual_acuity_left'].queryset=filtered
        self.fields['visual_acuity_right'].queryset=filtered
        self.fields['visual_acuity_both'].queryset=filtered

    def clean_iop_agents(self):
        iop_agents = self.cleaned_data.get('iop_agents')
        iop_control = self.cleaned_data.get('iop_control')
        if iop_control and not iop_agents:
            raise forms.ValidationError("IOP control agents required")
        elif not iop_control:
            return None
        return iop_agents

PatientManagementFormSet = forms.models.inlineformset_factory(Patient, Management, form = PatientManagementForm, extra=1, can_delete=False)

PatientOutcomeFormSet = forms.models.inlineformset_factory(Patient, Outcome, form = PatientOutcomeForm, extra=1, can_delete=False)

PatientUpdateManagementFormSet = forms.models.inlineformset_factory(Patient, Management, form = PatientManagementForm, extra=1)

PatientUpdateOutcomeFormSet = forms.models.inlineformset_factory(Patient, Outcome, form = PatientOutcomeForm, extra=1)
