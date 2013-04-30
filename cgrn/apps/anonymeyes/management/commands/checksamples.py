from django.core.management.base import BaseCommand, CommandError
from apps.anonymeyes.models import Patient, Management, Outcome

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Checks sample datasets'

    def handle(self, *args, **options):
        samples = [2004, 2009, 2010];
        for sample in samples:
            patients = Patient.objects.filter(dob_year=sample).exclude(created_by__username='mariap')
            canonical_patient = Patient.objects.get(dob_year=sample, created_by__username='mariap')
            self.stdout.write('\nProcessing %s\n-----\n' % canonical_patient.dob)
            for patient in patients:
                mismatches = []
                
                # Patient
                exclude = [ 'uuid', 'dob_month', 'dob_year', 'dob_day', 'created_by_id',
                           'updated_by_id', 'updated_at', 'created_at', 'id', 'postcode',
                           'country_id', '_state', 'visual_acuity_date', 'visual_acuity_method_id',
                           'visual_acuity_method_comment', 'visual_acuity_scale_id',
                           'visual_acuity_right_id', 'visual_acuity_left_id', 'visual_acuity_both_id',
                           'visual_acuity_correction_right_id', 'visual_acuity_correction_left_id',
                           'visual_acuity_correction_both_id', 'visual_acuity_fixation_preference' ]
                mismatches += self._compare(canonical_patient, patient, exclude, 'patient')
                
                # Managements
                managements = list(Management.objects.filter(patient=patient).order_by('date'))
                canonical_managements = list(Management.objects.filter(patient=canonical_patient).order_by('date'))
                exclude = [ 'created_by_id', 'updated_by_id', 'updated_at',
                           'created_at', 'id', '_state', 'patient_id' ]
                management_record_count = len(managements)
                if len(canonical_managements) < management_record_count:
                    management_record_count = len(canonical_managements)
                for index in range(1,management_record_count):
                    mismatches += self._compare(canonical_managements[index], managements[index], exclude, 'management.'+str(index))
                if len(canonical_managements) > len(managements):
                    mismatches += ['management.missing.'+str(len(canonical_managements)-len(managements))]
                elif len(managements) > len(canonical_managements):
                    mismatches += ['management.extra.'+str(len(managements)-len(canonical_managements))]
                    
                # Outcomes
                outcomes = list(Outcome.objects.filter(patient=patient).order_by('date'))
                canonical_outcomes = list(Outcome.objects.filter(patient=canonical_patient).order_by('date'))
                exclude = [ 'created_by_id', 'updated_by_id', 'updated_at',
                           'created_at', 'id', '_state', 'patient_id','visual_acuity_date',
                           'visual_acuity_method_id', 'visual_acuity_method_comment',
                           'visual_acuity_scale_id', 'visual_acuity_right_id', 'visual_acuity_left_id',
                           'visual_acuity_both_id', 'visual_acuity_correction_right_id',
                           'visual_acuity_correction_left_id', 'visual_acuity_correction_both_id',
                           'visual_acuity_fixation_preference' ]
                outcome_record_count = len(outcomes)
                if len(canonical_outcomes) < outcome_record_count:
                    outcome_record_count = len(canonical_outcomes)
                for index in range(1,outcome_record_count):
                    mismatches += self._compare(canonical_outcomes[index], outcomes[index], exclude, 'outcome.'+str(index))
                if len(canonical_outcomes) > len(outcomes):
                    mismatches += ['outcome.missing.'+str(len(canonical_outcomes)-len(outcomes))]
                elif len(outcomes) > len(canonical_outcomes):
                    mismatches += ['outcome.extra.'+str(len(outcomes)-len(canonical_outcomes))]
                    
                self.stdout.write('Username %s has %s mismatches %s\n' % (patient.created_by.username, len(mismatches), mismatches))
                
                
    def _compare(self, obj1, obj2, excluded_keys, prefix):
        d1, d2 = obj1.__dict__, obj2.__dict__
        fields = []
        for k, v in d1.items():
            if k in excluded_keys:
                continue
            try:
                if v != d2[k]:
                    fields.append(prefix+'.'+k)
            except KeyError:
                fields.append(prefix+'.'+k)
        return fields

