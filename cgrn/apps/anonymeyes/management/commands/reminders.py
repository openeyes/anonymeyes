from django.core.management.base import BaseCommand, CommandError
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
        for outcome in [relativedelta.relativedelta(),
                        relativedelta.relativedelta(months=-6),
                        relativedelta.relativedelta(months=-12),
                        relativedelta.relativedelta(months=-18)]:
            reminders.append(
                {'delta': outcome + relativedelta.relativedelta(months=-5, weeks=2),
                 'message': 'reminder1'})
            reminders.append({'delta': outcome + relativedelta.relativedelta(months=-5),
                              'message': 'reminder2'})
            reminders.append({'delta': outcome + relativedelta.relativedelta(months=-6),
                              'message': 'reminder3'})
            reminders.append(
                {'delta': outcome + relativedelta.relativedelta(months=-7, weeks=2),
                 'message': 'reminder4'})
            reminders.append({'delta': outcome + relativedelta.relativedelta(months=-7),
                              'message': 'reminder5'})

        patients = Patient.objects.filter(Q(next_reminder__lte=today) | Q(next_reminder__isnull=True))
        for patient in patients:

            self.stdout.write(
                'Processing patient UUID %s, next reminder is %s\n' % (patient.uuid, patient.next_reminder))

            # Send reminder
            for reminder in reversed(reminders):
                if patient.created_at.date() - reminder['delta'] <= today:
                    self.stdout.write('- Sending reminder: %s, created %s, matching %s (%s <= %s)\n' % (
                        reminder['message'], patient.created_at.date(), reminder['delta'],
                        patient.created_at.date() - reminder['delta'], today))
                    body = get_template('anonymeyes/reminders/' + reminder['message'] + '.txt')
                    d = Context({})
                    send_mail('Reminder to update IPSOCG dataset', body.render(d), settings.CONTACT_SENDER, settings.CONTACT_RECIPIENTS)
                    break

            # Update next reminder
            for reminder in reminders:
                if today + reminder['delta'] < patient.created_at.date():
                    self.stdout.write('- Updating patient: (%s < %s), setting next reminder to %s (%s)\n' % (
                        today + reminder['delta'], patient.created_at.date(),
                        patient.created_at.date() - reminder['delta'],
                        reminder['message']))
                    patient.next_reminder = patient.created_at.date() - reminder['delta']
                    #patient.save()
                    break
