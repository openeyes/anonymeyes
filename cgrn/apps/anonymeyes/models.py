from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from uuid import uuid4

class EthnicGroup(models.Model):
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name

class Eye(models.Model):
    name = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.name

class Diagnosis(models.Model):
    class Meta:
        verbose_name_plural = 'diagnoses'
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

class LensStatus(models.Model):
    class Meta:
        verbose_name_plural = 'lens statuses'
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name

class VisualAcuityMethod(models.Model):
    name = models.CharField(max_length=64)
    
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
    postcode = models.CharField(max_length=4)
    ethnic_group = models.ForeignKey(EthnicGroup)
    NO = 0
    YES = 1
    UNKNOWN = 2
    CONSANGUINITY_CHOICES = (
                            (UNKNOWN, 'Unknown'),
                            (YES, 'Yes'),
                            (NO, 'No'),
    )
    consanguinity = models.IntegerField(choices=CONSANGUINITY_CHOICES)
    eye = models.ForeignKey(Eye)
    diagnosis = models.ForeignKey(Diagnosis)
    lens_status_right = models.ForeignKey(LensStatus, related_name='+', verbose_name='Right lens status')
    lens_status_left = models.ForeignKey(LensStatus, related_name='+', verbose_name='Left lens status')
    lens_extraction_date_right = models.DateField(verbose_name='Extraction date')
    lens_extraction_date_left = models.DateField(verbose_name='Extraction date')
    visual_acuity_date = models.DateField()
    visual_acuity_method = models.ForeignKey(VisualAcuityMethod,verbose_name='Visual Acuity Method')
    visual_acuity_right = models.CharField(max_length=10, verbose_name='RVA')
    visual_acuity_left = models.CharField(max_length=10, verbose_name='LVA')
    visual_acuity_both = models.CharField(max_length=10, verbose_name='BVA')
    
    def __unicode__(self):
        return str(self.uuid)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

class Complication(models.Model):
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name

class Surgery(models.Model):
    name = models.CharField(max_length=64)
    adjuvant = models.BooleanField()
    
    def __unicode__(self):
        return self.name

class Adjuvant(models.Model):
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name

class ManagementType(models.Model):
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name

class Management(models.Model):
    created_by = models.ForeignKey(User, related_name='management_created_set', blank=True, null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='management_updated_set', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    date = models.DateField()
    eye = models.ForeignKey(Eye)
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
    visual_acuity_right = models.CharField(max_length=10, verbose_name='RVA')
    visual_acuity_left = models.CharField(max_length=10, verbose_name='LVA')
    visual_acuity_both = models.CharField(max_length=10, verbose_name='BVA')
    patient = models.ForeignKey(Patient)

    def __unicode__(self):
        return str(self.date)
