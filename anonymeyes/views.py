from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from django.forms.models import construct_instance
from anonymeyes.admin import PatientAdminForm
from anonymeyes.forms import PatientFormStep1, PatientFormStep2, PatientFormStep3, PatientFormStep4
from anonymeyes.models import Patient, Management

def index(request):
    return render(request, 'index.html')

class PatientWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        
        # Save patient
        patient = Patient()
        for form in form_list:
            patient = construct_instance(form, patient)
        patient.save()

        # Save management records
        for management_record in form_list[2].save(commit=False):
            management_record.patient = patient
            management_record.save()

        # Save outcome records
        for outcome_record in form_list[3].save(commit=False):
            outcome_record.patient = patient
            outcome_record.save()

        return HttpResponseRedirect('/anonymeyes/thanks/')

@login_required
def create(request):
    patient = Patient()
    initial_dict = {
                    '0': {
                          'sex': 0,
                          'dob': '03/12/2012',
                          'postcode': 'ss9',
                          'ethnic_group': 1,
                          'consanguinity': 0,
                          },
                    '1': {
                          'eye': 1,
                          'diagnosis': 1,
                          'lens_status_right': 1,
                          'lens_status_left': 1,
                          'lens_extraction_date_right': '03/12/2012',
                          'lens_extraction_date_left': '03/12/2012',
                          'visual_acuity_date': '03/12/2012',
                          'visual_acuity_method': 1,
                          'visual_acuity_right': 1,
                          'visual_acuity_left': 2,
                          'visual_acuity_both': 3,
                          },
                    }
    wizard = PatientWizard.as_view([PatientFormStep1, PatientFormStep2, PatientFormStep3, PatientFormStep4], initial_dict=initial_dict)
    return wizard(request)

@login_required
def thanks(request):
    return render(request, 'thanks.html')

