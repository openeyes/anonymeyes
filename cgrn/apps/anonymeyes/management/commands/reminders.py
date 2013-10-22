from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from apps.anonymeyes.models import Patient, Management, Outcome
from django.db.models import Q
from django.template import Context
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings
from pprint import pprint
import datetime, dateutil.relativedelta as relativedelta


class Command(BaseCommand):
    help = 'Sends notifications for updating outcomes'

    def handle(self, *args, **options):
        today = datetime.date.today()
        reminders = []
        for outcome in [6, 12, 18]:
            outcome_delta = relativedelta.relativedelta(months=-outcome)
            reminders.append({
                'delta': outcome_delta + relativedelta.relativedelta(months=1, weeks=2),
                'month': outcome,
                'message': 'reminder1'
            })
            reminders.append({
                'delta': outcome_delta + relativedelta.relativedelta(months=1),
                'month': outcome,
                'message': 'reminder2'
            })
            reminders.append({
                'delta': outcome_delta + relativedelta.relativedelta(),
                'month': outcome,
                'message': 'reminder3'
            })
            reminders.append({
                'delta': outcome_delta + relativedelta.relativedelta(months=-1, weeks=2),
                'month': outcome,
                'message': 'reminder4'
            })
            reminders.append({
                'delta': outcome_delta + relativedelta.relativedelta(months=-1),
                'month': outcome,
                'message': 'reminder5'
            })

        patients = Patient.objects.filter(Q(next_reminder__lte=today))
        for patient in patients:

            self.stdout.write(
                'Processing patient UUID %s, next reminder is %s\n' % (patient.uuid, patient.next_reminder))

            # Send reminder
            for reminder in reversed(reminders):
                if patient.created_at.date() - reminder['delta'] <= today:
                    self.stdout.write('- Sending reminder: template=%s, created_at=%s, reminder_date=%s (%s), recipient=%s\n' % (
                        reminder['message'],
                        patient.created_at.date(),
                        patient.created_at.date() - reminder['delta'],
                        reminder['delta'],
                        patient.created_by.email
                    ))
                    body = get_template('anonymeyes/reminders/' + reminder['message'] + '.txt')
                    d = Context({
                        'month': reminder['month'],
                        'patient': patient,
                        'patient_url': 'http://' + Site.objects.get_current().domain + '/anonymeyes/uuid/' + patient.uuid.lower(),
                        'start_date': 'FIXME',
                        'end_date': 'FIXME',
                    })
                    #send_mail('IPSOCG Outcomes Data: '+reminder['month']+' months', body.render(d), settings.CONTACT_SENDER, patient.created_by.email)
                    break

            # Update next reminder
            patient.next_reminder = None
            for reminder in reminders:
                if today + reminder['delta'] < patient.created_at.date():
                    self.stdout.write('- Updating patient: (%s < %s), setting next reminder to %s (%s)\n' % (
                        today + reminder['delta'], patient.created_at.date(),
                        patient.created_at.date() - reminder['delta'],
                        reminder['message']))
                    patient.next_reminder = patient.created_at.date() - reminder['delta']
                    break
            if not patient.next_reminder:
                self.stdout.write('- Updating patient: no reminder date matches, so setting next reminder to null\n')
            patient.save()
