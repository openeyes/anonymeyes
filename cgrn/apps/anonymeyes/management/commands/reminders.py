from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from apps.anonymeyes.models import Patient, Management, Outcome
from django.db.models import Q
from django.template import Context
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings
import datetime, dateutil.relativedelta as relativedelta, pprint


class Command(BaseCommand):
    help = 'Sends notifications for updating outcomes'

    def handle(self, *args, **options):
        today = datetime.date.today()
        reminders = [
            {
                'delta': relativedelta.relativedelta(months=-1, weeks=-2),
                'message': 'reminder1'
            },
            {
                'delta': relativedelta.relativedelta(months=-1),
                'message': 'reminder2'
            },
            {
                'delta': relativedelta.relativedelta(),
                'message': 'reminder3'
            },
            {
                'delta': relativedelta.relativedelta(months=1, weeks=-2),
                'message': 'reminder4'
            },
            {
                'delta': relativedelta.relativedelta(months=1),
                'message': 'reminder5'
            }
        ]
        window_step = 6
        window_last = 18

        patients = Patient.objects.filter(Q(next_reminder__lte=today)).order_by('visual_acuity_date')
        for patient in patients:

            self.stdout.write('Processing patient UUID %s, date %s, next reminder is %s\n' % (patient.uuid, patient.visual_acuity_date, patient.next_reminder))

            reminder_sent = False
            for window in range(window_step,window_last,window_step):
                # See if we are inside the reminder window
                if patient.visual_acuity_date + relativedelta.relativedelta(months=window-1, weeks=-2) <= today and patient.visual_acuity_date + relativedelta.relativedelta(months=window+1) >= today:
                    self.stdout.write('- Inside %s month window\n' % (window))
                    # See if we have an outcome for the current_window
                    outcomes = patient.outcome_set.filter(date__gte = patient.visual_acuity_date + relativedelta.relativedelta(months=window-1), date__lte = patient.visual_acuity_date + relativedelta.relativedelta(months=window+1))
                    if not outcomes:
                        # No outcome(s) for this window, so we need to send a reminder

                        ''' Send reminder '''

                        for reminder in reversed(reminders):
                            if patient.visual_acuity_date + relativedelta.relativedelta(months=window) + reminder['delta'] <= today:
                                self.stdout.write('- Sending reminder: template=%s, recipient=%s\n' % (
                                    reminder['message'],
                                    patient.created_by.email
                                ))
                                body = get_template('anonymeyes/reminders/' + reminder['message'] + '.txt')
                                d = Context({
                                    'month': window,
                                    'patient': patient,
                                    'patient_url': 'http://' + Site.objects.get_current().domain + '/anonymeyes/uuid/' + patient.uuid.lower(),
                                    'start_date': patient.visual_acuity_date + relativedelta.relativedelta(months=window-1),
                                    'end_date': patient.visual_acuity_date + relativedelta.relativedelta(months=window+1),
                                })
                                send_mail('IPSOCG Outcomes Data: '+str(window)+' months', body.render(d), settings.CONTACT_SENDER, [patient.created_by.email])
                                pprint.pprint(body.render(d))
                                reminder_sent = True
                                break

                        if not reminder_sent:
                            # Something went wrong. We should have sent a reminder but nothing was sent
                            raise Exception('Reminder should have been sent, but couldn\'t find a match')

                    else:
                        # Outcome(s) already exist for this window, so no need to send reminder
                        self.stdout.write('- Outcome exists for current window, so no need to send reminder\n')

                    break

            ''' Set next reminder '''

            # Default next reminder is None, which means that there are no more reminders
            patient.next_reminder = None
            patient.outcome_overdue = False

            window = window_step
            while not patient.next_reminder and window <= window_last:

                # Step through the reminder points in the window until we find one that hasn't yet been sent
                for reminder in reminders:
                    next_reminder = patient.visual_acuity_date + relativedelta.relativedelta(months=window) + reminder['delta']
                    if next_reminder > today:
                        # Set next reminder
                        self.stdout.write('- Setting next reminder to %s (%s/%s)\n' % (next_reminder, window, reminder['message']))
                        patient.next_reminder = next_reminder
                        break

                if not patient.next_reminder and not patient.outcome_overdue:
                    # Check that we have a valid outcome for this window before moving on
                    outcomes = patient.outcome_set.filter(date__gte = patient.visual_acuity_date + relativedelta.relativedelta(months=window-1), date__lte = patient.visual_acuity_date + relativedelta.relativedelta(months=window+1))
                    if not outcomes:
                        patient.outcome_overdue = True
                        self.stdout.write('- Window expired without outcome being entered. Marking as overdue\n')

                window += window_step

            if not patient.next_reminder:
                self.stdout.write('- Clearing next reminder (no more reminders due)\n')

            patient.save()


