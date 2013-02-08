from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import validators 
from uuid import uuid4
import re

class EthnicGroup(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class Eye(models.Model):
    class Meta:
        ordering = ['id']

    name = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.name

class DiagnosisGroup(models.Model):
    class Meta:
        verbose_name_plural = 'diagnose groups'
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
    
    def __unicode__(self):
        if(self.group.diagnosis_set.count() > 1):
            return self.group.name + ': ' + self.name
        else:
            return self.name

class LensStatus(models.Model):
    class Meta:
        verbose_name_plural = 'lens statuses'
    name = models.CharField(max_length=64)
    
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
    scale = models.ForeignKey(VisualAcuityScale)
    
    def __unicode__(self):
        return self.name

class VisualAcuityReading(models.Model):
    class Meta:
        ordering = ['scale__name','sort','name']

    name = models.CharField(max_length=64)
    value = models.IntegerField()
    sort = models.IntegerField(default=10)
    scale = models.ForeignKey(VisualAcuityScale, related_name='readings')
    
    def __unicode__(self):
        return self.name

class Tonometry(models.Model):
    class Meta:
        ordering = ['sort','name']

    name = models.CharField(max_length=64)
    sort = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.name

class Patient(models.Model):
    uuid = models.CharField(unique=True, max_length=64, editable=False, blank=True, default=uuid4)
    created_by = models.ForeignKey(User, related_name='patient_created_set', blank=True, null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='patient_updated_set', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    MALE = 0
    FEMALE = 1
    SEX_CHOICES = (
                   (MALE, 'Male'),
                   (FEMALE, 'Female'),
    )
    sex = models.IntegerField(choices=SEX_CHOICES)
    dob = models.DateField() 
    postcode = models.CharField(
                                verbose_name='Postcode Prefix',
                                max_length=4,
                                validators=[ validators.RegexValidator(regex=re.compile('^[A-Za-z]{1,2}[0-9]{1,2}[A-Za-z]?$'), message='First part of postcode only (e.g. AB12)') ],
                                )
    ethnic_group = models.ForeignKey(EthnicGroup)
    NO = 0
    YES = 1
    UNKNOWN = 2
    TRISTATE_CHOICES = (
                            (UNKNOWN, 'Unknown'),
                            (YES, 'Yes'),
                            (NO, 'No'),
    )
    consanguinity = models.IntegerField(choices=TRISTATE_CHOICES)
    diagnosis_right = models.ForeignKey(Diagnosis, related_name='+', verbose_name='Right diagnosis')
    diagnosis_left = models.ForeignKey(Diagnosis, related_name='+', verbose_name='Left diagnosis')
    lens_status_right = models.ForeignKey(LensStatus, related_name='+', verbose_name='Right lens status')
    lens_status_left = models.ForeignKey(LensStatus, related_name='+', verbose_name='Left lens status')
    lens_extraction_date_right = models.DateField(verbose_name='Right Extraction date', blank=True, null=True)
    lens_extraction_date_left = models.DateField(verbose_name='Left Extraction date', blank=True, null=True)
    visual_acuity_date = models.DateField(verbose_name='Date')
    visual_acuity_method = models.ForeignKey(VisualAcuityMethod,verbose_name='Method')
    visual_acuity_right = models.ForeignKey(VisualAcuityReading, related_name='patient_rva', verbose_name='RVA')
    visual_acuity_left = models.ForeignKey(VisualAcuityReading, related_name='patient_lva', verbose_name='LVA')
    visual_acuity_both = models.ForeignKey(VisualAcuityReading, related_name='patient_beo', verbose_name='BEO')
    iop_right = models.IntegerField(verbose_name='Right IOP', blank=True, null=True)
    iop_left = models.IntegerField(verbose_name='Left IOP', blank=True, null=True)
    tonometry = models.ForeignKey(Tonometry)
    eua = models.IntegerField(verbose_name='EUA', choices=TRISTATE_CHOICES)
    
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

    def __unicode__(self):
        return self.name

class Surgery(models.Model):
    name = models.CharField(max_length=64)
    adjuvant = models.BooleanField()
    sort = models.IntegerField(default=10)
    
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
    comments = models.TextField(blank=True)
    patient = models.ForeignKey(Patient)

    def __unicode__(self):
        return str(self.date)
    
class IOPControl(models.Model):
    class Meta:
        verbose_name = 'IOP control'
        verbose_name_plural = 'IOP controls'
        
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name

class Outcome(models.Model):
    created_by = models.ForeignKey(User, related_name='outcome_created_set', blank=True, null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='outcome_updated_set', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    date = models.DateField()
    eye = models.ForeignKey(Eye)
    iop_control = models.ForeignKey(IOPControl, verbose_name='IOP Control')
    visual_acuity_method = models.ForeignKey(VisualAcuityMethod)
    visual_acuity_right = models.ForeignKey(VisualAcuityReading, related_name='outcome_rva', verbose_name='RVA')
    visual_acuity_left = models.ForeignKey(VisualAcuityReading, related_name='outcome_lva', verbose_name='LVA')
    visual_acuity_both = models.ForeignKey(VisualAcuityReading, related_name='outcome_beo', verbose_name='BEO')
    patient = models.ForeignKey(Patient)

    def __unicode__(self):
        return str(self.date)
