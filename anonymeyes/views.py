from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from anonymeyes.admin import PatientAdminForm
from anonymeyes.forms import PatientFormStep1, PatientFormStep2, PatientFormStep3
from anonymeyes.models import Patient, Management


def index(request):
    return render(request, 'index.html')

class PatientWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        #do_something_with_the_form_data(form_list)
        '''
        patient = Patient()
        for form in form_list:
            for field, value in form.cleaned_data.iteritems():
                setattr(patient, field, value)
        patient.save()
        return HttpResponseRedirect('/anonymeyes/thanks/')
        '''
        return render(request, 'debug.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

@login_required
def create(request):
    instance_dict = {'2': Management.objects.none()}
    wizard = PatientWizard.as_view([PatientFormStep1, PatientFormStep2, PatientFormStep3], instance_dict=instance_dict)
    return wizard(request)

@login_required
def thanks(request):
    return render(request, 'thanks.html')

