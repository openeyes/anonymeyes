from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from captcha.fields import ReCaptchaField
from apps.anonymeyes.models import Patient, Management, Outcome

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
    def send_email(self):
        message = get_template('anonymeyes/message.txt')
        d = Context(self.cleaned_data)
        send_mail('Message from CGRN contact form', message.render(d), 'www@cgrn.j13.me',
                  ['jamie.neil@openeyes.org.uk'])

class CaptchaContactForm(ContactForm):
    captcha = ReCaptchaField()

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('sex', 'dob', 'postcode', 'ethnic_group', 'consanguinity')
        widgets = {
                   'postcode': forms.TextInput(attrs={'size':'10'}),
                   'dob': forms.DateInput(attrs={'class':'datepicker past'})
        }

class PatientBaselineForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('visual_acuity_date', 'diagnosis_right', 'diagnosis_left',
                  'visual_acuity_method', 'visual_acuity_right', 'visual_acuity_left', 'visual_acuity_both',
                  'iop_right', 'iop_left', 'tonometry', 'eua',
                  'lens_status_right', 'lens_extraction_date_right',
                  'lens_status_left', 'lens_extraction_date_left'
                  )
        widgets = {
                   'lens_extraction_date_right': forms.DateInput(attrs={'class':'datepicker past'}),
                   'lens_extraction_date_left': forms.DateInput(attrs={'class':'datepicker past'}),
                   'visual_acuity_date': forms.DateInput(attrs={'class':'datepicker past'}),
                   'visual_acuity_right': forms.TextInput(attrs={'class': 'small', 'size':'10'}),
                   'visual_acuity_left': forms.TextInput(attrs={'class': 'small', 'size':'10'}),
                   'visual_acuity_both': forms.TextInput(attrs={'class': 'small', 'size':'10'}),
                   'iop_right': forms.TextInput(attrs={'class': 'small', 'size':'10'}),
                   'iop_left': forms.TextInput(attrs={'class': 'small', 'size':'10'})
        }
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
        return lens_extraction_date_right

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
        return surgery

    def clean_complication(self):
        complication = self.cleaned_data.get('complication')
        type = self.cleaned_data.get('type')
        if type and type.name == 'Complication' and not complication:
            raise forms.ValidationError("Complication detail required")
        return complication

    def clean_adjuvant(self):
        adjuvant = self.cleaned_data.get('adjuvant')
        surgery = self.cleaned_data.get('surgery')
        if surgery and surgery.adjuvant and not adjuvant:
            raise forms.ValidationError("Adjuvant detail required")
        return adjuvant

class PatientOutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        widgets = {
                   'date': forms.DateInput(attrs={'class':'datepicker past'}),
                   'visual_acuity_right': forms.TextInput(attrs={'class': 'small', 'size':'10'}),
                   'visual_acuity_left': forms.TextInput(attrs={'class': 'small', 'size':'10'}),
                   'visual_acuity_both': forms.TextInput(attrs={'class': 'small', 'size':'10'}),
        }
        exclude = { 'patient', 'created_by', 'updated_by', }

PatientManagementFormSet = forms.models.inlineformset_factory(Patient, Management, form = PatientManagementForm, extra=1, can_delete=False)

PatientOutcomeFormSet = forms.models.inlineformset_factory(Patient, Outcome, form = PatientOutcomeForm, extra=1, can_delete=False)

PatientUpdateManagementFormSet = forms.models.inlineformset_factory(Patient, Management, form = PatientManagementForm, extra=1)

PatientUpdateOutcomeFormSet = forms.models.inlineformset_factory(Patient, Outcome, form = PatientOutcomeForm, extra=1)
