from django.db import models
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
    lens_status_right = models.ForeignKey(LensStatus, related_name='+', verbose_name='Right Lens Status')
    lens_status_left = models.ForeignKey(LensStatus, related_name='+', verbose_name='Left Lens Status')
    lens_extraction_date_right = models.DateField(verbose_name='Extraction Date')
    lens_extraction_date_left = models.DateField(verbose_name='Extraction Date')
    visual_acuity_date = models.DateField()
    visual_acuity_method = models.ForeignKey(VisualAcuityMethod,verbose_name='Method')
    visual_acuity_right = models.CharField(max_length=10, verbose_name='RVA')
    visual_acuity_left = models.CharField(max_length=10, verbose_name='LVA')
    visual_acuity_both = models.CharField(max_length=10, verbose_name='BVA')
    
    def __unicode__(self):
        return str(self.uuid)

class ManagementType(models.Model):
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name

class Management(models.Model):
    date = models.DateField()
    eye = models.ForeignKey(Eye)
    type = models.ForeignKey(ManagementType)
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
    date = models.DateField()
    eye = models.ForeignKey(Eye)
    iop_control = models.ForeignKey(IOPControl)
    visual_acuity_method = models.ForeignKey(VisualAcuityMethod)
    visual_acuity_right = models.CharField(max_length=10, verbose_name='RVA')
    visual_acuity_left = models.CharField(max_length=10, verbose_name='LVA')
    visual_acuity_both = models.CharField(max_length=10, verbose_name='BVA')
    patient = models.ForeignKey(Patient)

    def __unicode__(self):
        return str(self.date)
