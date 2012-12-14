from django import forms
from django.http import HttpResponseRedirect
from anonymeyes.models import Patient, Management, Outcome

class PatientFormStep1(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('sex', 'dob', 'postcode', 'ethnic_group', 'consanguinity')
        widgets = {
                   'postcode': forms.TextInput(attrs={'size':'10'}),
                   'dob': forms.DateInput(attrs={'class':'datepicker past'}),
        }

class PatientFormStep2(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('eye', 'diagnosis', 'lens_status_right', 'lens_extraction_date_right', 'lens_status_left', 'lens_extraction_date_left',
                 'visual_acuity_date', 'visual_acuity_method', 'visual_acuity_right', 'visual_acuity_left', 'visual_acuity_both')
        widgets = {
                   'lens_extraction_date_right': forms.DateInput(attrs={'class':'datepicker past'}),
                   'lens_extraction_date_left': forms.DateInput(attrs={'class':'datepicker past'}),
                   'visual_acuity_date': forms.DateInput(attrs={'class':'datepicker past'}),
                   'visual_acuity_right': forms.TextInput(attrs={'size':'10'}),
                   'visual_acuity_left': forms.TextInput(attrs={'size':'10'}),
                   'visual_acuity_both': forms.TextInput(attrs={'size':'10'}),
        }

PatientFormStep3 = forms.models.inlineformset_factory(Patient, Management, extra=1, can_delete=False)

PatientFormStep4 = forms.models.inlineformset_factory(Patient, Outcome, extra=1, can_delete=False)
