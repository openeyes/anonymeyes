from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.forms.models import construct_instance
from anonymeyes.admin import PatientAdminForm
from anonymeyes.forms import PatientForm, PatientBaselineForm, PatientManagementFormSet, PatientOutcomeFormSet
from anonymeyes.models import Patient, Management

def index(request):
    return render(request, 'index.html')

class PatientWizard(NamedUrlSessionWizardView):
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

        return render(self.request, 'thanks.html', { "patient": patient })

@login_required
def create(request, **kwargs):
    ''' Test data
    initial_dict = {
                    'patient': {
                          'sex': 0,
                          'dob': '03/12/2012',
                          'postcode': 'ss9',
                          'ethnic_group': 1,
                          'consanguinity': 0,
                          },
                    'baseline': {
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
                    '''
    forms = (
             ('patient', PatientForm),
             ('baseline', PatientBaselineForm),
             ('management', PatientManagementFormSet),
             ('outcome', PatientOutcomeFormSet),
             )
    wizard = PatientWizard.as_view(forms, url_name='create_step',
                                   #initial_dict=initial_dict
                                   )
    return wizard(request, **kwargs)

