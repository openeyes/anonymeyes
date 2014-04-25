from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core import validators 
from uuid import uuid4
from datetime import date
from dateutil import relativedelta

class DOBPrecision(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    css_class = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    dob_precision = models.ForeignKey(DOBPrecision, related_name='+', default=1, verbose_name='DOB Maximum Precision')
    dob_min_precision = models.ForeignKey(DOBPrecision, related_name='+', default=1, verbose_name='DOB Minimum Precision')

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class EthnicGroupGroup(models.Model):
    class Meta:
        verbose_name = 'Ethnic group / Race'
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class EthnicGroup(models.Model):
    class Meta:
        ordering = ['group','sort','name']

    name = models.CharField(max_length=64)
    group = models.ForeignKey(EthnicGroupGroup)
    sort = models.IntegerField(default=10)
    requires_comment = models.BooleanField(default=False)
    
    def description(self):
        if(self.group.ethnic_group_set.count() > 1):
            return self.group.name + ': ' + self.name
        else:
            return self.name
    
    def __unicode__(self):
        return self.name

class Eye(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=10)
    single = models.BooleanField()
    sort = models.IntegerField(default=10)
    
    
    def __unicode__(self):
        return self.name

class DiagnosisGroup(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=255)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class Diagnosis(models.Model):
    class Meta:
        verbose_name_plural = 'diagnoses'
        ordering = ['group__sort','sort','name']

    name = models.CharField(max_length=255)
    group = models.ForeignKey(DiagnosisGroup)
    sort = models.IntegerField(default=10)
    requires_comment = models.BooleanField(default=False)
    
    def description(self):
        if(self.group.diagnosis_set.count() > 1):
            return self.group.name + ': ' + self.name
        else:
            return self.name
    
    def __unicode__(self):
        return self.name

class HealthCare(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=255)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class Anaesthesia(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=255)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class LensStatusGroup(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=255)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class LensStatus(models.Model):
    class Meta:
        ordering = ['group__sort','sort','name']
        verbose_name_plural = 'lens statuses'
        
    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    group = models.ForeignKey(LensStatusGroup)
    
    def __unicode__(self):
        return self.name

class VisualAcuityScale(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class VisualAcuityMethod(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    scales = models.ManyToManyField(VisualAcuityScale)
    
    def __unicode__(self):
        return self.name

class VisualAcuityReading(models.Model):
    class Meta:
        ordering = ['scale__name','sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    scale = models.ForeignKey(VisualAcuityScale, related_name='readings')
    not_recorded = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class VisualAcuityCorrection(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    beo = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Tonometry(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class IOPAgent(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    no_agents = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class PostcodeValidator(models.Model):
    pattern = models.CharField(max_length=64)
    error = models.CharField(max_length=255)

    def __unicode__(self):
        return self.pattern

class Country(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    iso = models.CharField(max_length=2)
    postcode_validator = models.ForeignKey(PostcodeValidator)

    def __unicode__(self):
        return self.name

class Patient(models.Model):
    uuid = models.CharField(unique=True, max_length=64, editable=False, blank=True, default=uuid4)
    created_by = models.ForeignKey(User, related_name='patient_created_set', blank=True, null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='patient_updated_set', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    next_reminder = models.DateField(auto_now_add=True, blank=True, null=True)
    outcome_overdue = models.BooleanField(default=False)
    MALE = 0
    FEMALE = 1
    SEX_CHOICES = (
                   (MALE, 'Male'),
                   (FEMALE, 'Female'),
    )
    sex = models.IntegerField(choices=SEX_CHOICES)
    dob_day = models.IntegerField(blank=True, null=True, validators=[
                                                                     validators.MaxValueValidator(31),
                                                                     validators.MinValueValidator(1)
                                                                     ])
    MONTH_CHOICES = (
                     (1, '01'),
                     (2, '02'),
                     (3, '03'),
                     (4, '04'),
                     (5, '05'),
                     (6, '06'),
                     (7, '07'),
                     (8, '08'),
                     (9, '09'),
                     (10, '10'),
                     (11, '11'),
                     (12, '12'),
                     )
    dob_month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
    dob_year = models.IntegerField(validators=[
                                               validators.MaxValueValidator(date.today().year),
                                               validators.MinValueValidator(date.today().year - 30)
                                               ])
    @property
    def dob(self):
        dob = str(self.dob_year)
        if self.dob_month:
            dob = dob + '-' + str(self.dob_month).zfill(2)
        if self.dob_day:
            dob = dob + '-' + str(self.dob_day).zfill(2)
        return dob

    @property
    def outcome_due(self):
        window_step = 6
        window_last = 18
        today = date.today()
        for window in range(window_step,window_last,window_step):
            if self.visual_acuity_date + relativedelta.relativedelta(months=window-1) <= today and self.visual_acuity_date + relativedelta.relativedelta(months=window+1) >= today:
                outcomes = self.outcome_set.filter(date__gte = self.visual_acuity_date + relativedelta.relativedelta(months=window-1), date__lte = self.visual_acuity_date + relativedelta.relativedelta(months=window+1))
                if not outcomes:
                    return True
        return False

    country = models.ForeignKey(Country, verbose_name='Country of Residence')
    postcode = models.CharField(
                                verbose_name='Post/Zip Code',
                                max_length=6,
                                )
    health_care = models.ForeignKey(HealthCare, verbose_name='Health Care Coverage')
    ethnic_group = models.ForeignKey(EthnicGroup, verbose_name='Ethnic Group / Race')
    ethnic_group_comment = models.CharField(max_length=255, blank=True)
    UNKNOWN = 2
    NO = 0
    YES = 1
    TRISTATE_CHOICES = (
                            (UNKNOWN, 'Unknown'),
                            (NO, 'No'),
                            (YES, 'Yes'),
    )
    consanguinity = models.IntegerField(choices=TRISTATE_CHOICES)
    history = models.IntegerField(choices=TRISTATE_CHOICES, verbose_name='Family History of Childhood Onset Glaucoma')
    history_comment = models.TextField(blank=True)
    diagnosis_right = models.ForeignKey(Diagnosis, related_name='+', verbose_name='Right Diagnosis')
    diagnosis_left = models.ForeignKey(Diagnosis, related_name='+', verbose_name='Left Diagnosis')
    diagnosis_right_comment = models.TextField(verbose_name='Right Diagnosis comment', blank=True)
    diagnosis_left_comment = models.TextField(verbose_name='Left Diagnosis comment', blank=True)
    lens_status_right = models.ForeignKey(LensStatus, related_name='+', verbose_name='Right Lens Status')
    lens_status_left = models.ForeignKey(LensStatus, related_name='+', verbose_name='Left Lens Status')
    lens_extraction_date_right = models.DateField(verbose_name='Right Extraction Date', blank=True, null=True)
    lens_extraction_date_left = models.DateField(verbose_name='Left Extraction Date', blank=True, null=True)
    visual_acuity_date = models.DateField(verbose_name='Date')
    visual_acuity_method = models.ForeignKey(VisualAcuityMethod,verbose_name='Method')
    visual_acuity_method_comment = models.TextField(verbose_name='Method Comment', blank=True)
    visual_acuity_scale = models.ForeignKey(VisualAcuityScale, related_name='patient_visualacuity_scale',verbose_name='Scale')
    visual_acuity_right = models.ForeignKey(VisualAcuityReading, related_name='patient_rva', verbose_name='RVA')
    visual_acuity_left = models.ForeignKey(VisualAcuityReading, related_name='patient_lva', verbose_name='LVA')
    visual_acuity_both = models.ForeignKey(VisualAcuityReading, related_name='patient_beo', verbose_name='Both Eyes Open')
    visual_acuity_correction_right = models.ForeignKey(VisualAcuityCorrection, related_name='patient_rva_correction'
                                                       , verbose_name='Right correction', blank=True, null=True
                                                       , limit_choices_to = {'beo': False})
    visual_acuity_correction_left = models.ForeignKey(VisualAcuityCorrection, related_name='patient_lva_correction'
                                                      , verbose_name='Left correction', blank=True, null=True
                                                      , limit_choices_to = {'beo': False})
    visual_acuity_correction_both = models.ForeignKey(VisualAcuityCorrection, related_name='patient_beo_correction'
                                                      , verbose_name='Both correction', blank=True, null=True)
    NONE = 1
    RIGHT = 2
    LEFT = 3
    FIXATION_CHOICES = (
                            (RIGHT, 'Right'),
                            (LEFT, 'Left'),
                            (NONE, 'None'),
    )
    visual_acuity_fixation_preference = models.IntegerField(choices=FIXATION_CHOICES, verbose_name='Fixation Preference', blank=True, null=True)
    iop_right = models.IntegerField(verbose_name='Right IOP', validators=[
                                                                     validators.MaxValueValidator(99),
                                                                     validators.MinValueValidator(1)
                                                                     ])
    iop_left = models.IntegerField(verbose_name='Left IOP', validators=[
                                                                     validators.MaxValueValidator(99),
                                                                     validators.MinValueValidator(1)
                                                                     ])
    iop_agents_right = models.ManyToManyField(IOPAgent, related_name='patient_iop_agents_right', verbose_name='Right IOP Agents')
    iop_agents_left = models.ManyToManyField(IOPAgent, related_name='patient_iop_agents_left', verbose_name='Left IOP Agents')
    tonometry = models.ForeignKey(Tonometry)
    eua = models.ForeignKey(Anaesthesia, verbose_name='EUA')
    comments = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-updated_at']

    def __unicode__(self):
        return str(self.uuid)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
    
    def save(self):
        self.postcode = self.postcode.upper()
        super(Patient,self).save()

class Complication(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    requires_comment = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Surgery(models.Model):
    name = models.CharField(max_length=64)
    adjuvant = models.BooleanField()
    stage = models.BooleanField()
    sort = models.IntegerField(default=10)
    requires_comment = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['sort','name']
        verbose_name_plural = 'Surgeries'
    
    def __unicode__(self):
        return self.name

class Adjuvant(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class SurgeryStage(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class ManagementType(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class Management(models.Model):
    created_by = models.ForeignKey(User, related_name='management_created_set', blank=True, null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='management_updated_set', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    date = models.DateField()
    eye = models.ForeignKey(Eye, blank=True, null=True)
    type = models.ForeignKey(ManagementType)
    surgery = models.ForeignKey(Surgery, blank=True, null=True)
    complication = models.ForeignKey(Complication, blank=True, null=True)
    adjuvant = models.ForeignKey(Adjuvant, blank=True, null=True)
    surgery_stage = models.ForeignKey(SurgeryStage, blank=True, null=True)
    agents = models.ManyToManyField(IOPAgent, verbose_name='IOP Agents', blank=True, limit_choices_to = {'no_agents': False})
    comments = models.TextField(blank=True)
    patient = models.ForeignKey(Patient)
    @property
    def surgery_meta(self):
        meta = []
        if self.adjuvant:
            meta.append(str(self.adjuvant))
        if self.surgery_stage:
            meta.append(str(self.surgery_stage))
        return ', '.join(meta)

    def __unicode__(self):
        return str(self.date)
    
class Outcome(models.Model):
    created_by = models.ForeignKey(User, related_name='outcome_created_set', blank=True, null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='outcome_updated_set', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    date = models.DateField()
    IOP_CONTROLLED = 1
    IOP_UNCONTROLLED = 2
    IOP_CONTROL_NA = 3
    IOP_CONTROL_CHOICES = (
                            (IOP_CONTROLLED, 'Controlled'),
                            (IOP_UNCONTROLLED, 'Uncontrolled'),
                            (IOP_CONTROL_NA, 'Not applicable'),
    )
    iop_control_right = models.IntegerField(choices=IOP_CONTROL_CHOICES, verbose_name='Right IOP Control')
    iop_control_left = models.IntegerField(choices=IOP_CONTROL_CHOICES, verbose_name='Left IOP Control')
    iop_right = models.IntegerField(verbose_name='Right IOP', validators=[
                                                                     validators.MaxValueValidator(99),
                                                                     validators.MinValueValidator(1)
                                                                     ])
    iop_left = models.IntegerField(verbose_name='Left IOP', validators=[
                                                                     validators.MaxValueValidator(99),
                                                                     validators.MinValueValidator(1)
                                                                     ])
    iop_agents_right = models.ManyToManyField(IOPAgent, related_name='outcome_iop_agents_right', verbose_name='IOP Agents Right')
    iop_agents_left = models.ManyToManyField(IOPAgent, related_name='outcome_iop_agents_left', verbose_name='IOP Agents Left')
    tonometry = models.ForeignKey(Tonometry)
    eua = models.ForeignKey(Anaesthesia, verbose_name='EUA')
    visual_acuity_method = models.ForeignKey(VisualAcuityMethod)
    visual_acuity_method_comment = models.TextField(verbose_name='Method Comment', blank=True)
    visual_acuity_scale = models.ForeignKey(VisualAcuityScale, related_name='outcome_visualacuity_scale', verbose_name='Scale')
    visual_acuity_right = models.ForeignKey(VisualAcuityReading, related_name='outcome_rva', verbose_name='RVA')
    visual_acuity_left = models.ForeignKey(VisualAcuityReading, related_name='outcome_lva', verbose_name='LVA')
    visual_acuity_both = models.ForeignKey(VisualAcuityReading, related_name='outcome_beo', verbose_name='Both Eyes Open')
    visual_acuity_correction_right = models.ForeignKey(VisualAcuityCorrection, related_name='outcome_rva_correction'
                                                       , verbose_name='Right correction', blank=True, null=True
                                                       , limit_choices_to = {'beo': False})
    visual_acuity_correction_left = models.ForeignKey(VisualAcuityCorrection, related_name='outcome_lva_correction'
                                                      , verbose_name='Left correction', blank=True, null=True
                                                      , limit_choices_to = {'beo': False})
    visual_acuity_correction_both = models.ForeignKey(VisualAcuityCorrection, related_name='outcome_beo_correction'
                                                      , verbose_name='Both correction', blank=True, null=True)
    NONE = 1
    RIGHT = 2
    LEFT = 3
    FIXATION_CHOICES = (
                            (RIGHT, 'Right'),
                            (LEFT, 'Left'),
                            (NONE, 'None'),
    )
    visual_acuity_fixation_preference = models.IntegerField(choices=FIXATION_CHOICES, verbose_name='Fixation Preference', blank=True, null=True)
    patient = models.ForeignKey(Patient)

    def __unicode__(self):
        return str(self.date)
