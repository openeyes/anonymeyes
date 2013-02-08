from django.contrib import admin
from django import forms

from apps.anonymeyes.models import *

admin.site.register(EthnicGroup)
admin.site.register(DiagnosisGroup)
admin.site.register(LensStatus)
admin.site.register(VisualAcuityMethod)
admin.site.register(ManagementType)
admin.site.register(Complication)
admin.site.register(Adjuvant)
admin.site.register(Tonometry)

class ManagementAdminForm(forms.ModelForm):
    class Meta:
        model = Management
        widgets = {
                   'comments': forms.TextInput
        }

class ManagementInline(admin.TabularInline):
    extra = 0
    model = Management
    form = ManagementAdminForm
    readonly_fields = ('created_at', 'updated_at',)

class OutcomeAdminForm(forms.ModelForm):
    class Meta:
        model = Outcome

class OutcomeInline(admin.TabularInline):
    extra = 0
    model = Outcome
    form = OutcomeAdminForm
    readonly_fields = ('created_at', 'updated_at',)

class PatientAdminForm(forms.ModelForm):
    class Meta:
        model = Patient
        widgets = {
                   'postcode': forms.TextInput(attrs={'size':'10'}),
                   'iop_right': forms.TextInput(attrs={'size':'10'}),
                   'iop_left': forms.TextInput(attrs={'size':'10'})
        }

class PatientAdmin(admin.ModelAdmin):
    form = PatientAdminForm
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
                 (None, {
                         'fields': ('created_by', 'updated_by', 'created_at', 'updated_at', 'sex', 'dob_day', 'dob_month', 'dob_year', 'postcode', 'ethnic_group', 'consanguinity')
                         }),
                 ('Baseline Assessment', {
                         'fields': ('visual_acuity_date', 'diagnosis_right', 'diagnosis_left',
                                    ('visual_acuity_method', 'visual_acuity_right', 'visual_acuity_left', 'visual_acuity_both'),
                                    ('iop_right', 'iop_left', 'tonometry', 'eua', 'anaesthesia'),
                                    ('lens_status_right', 'lens_extraction_date_right'),
                                    ('lens_status_left', 'lens_extraction_date_left')
                                    )
                         }),
    )
    inlines = [
        ManagementInline,
        OutcomeInline,
    ]
    list_display = ('uuid','sex', 'dob_year', 'postcode','created_at', 'updated_at')
    list_filter = ('sex','dob_year','created_at','updated_at')
    search_fields = ('postcode','diagnosis_right__name','diagnosis_left__name')
    
admin.site.register(Patient, PatientAdmin)

class SurgeryAdmin(admin.ModelAdmin):
    list_display = ('name','adjuvant','sort')
    list_filter = ('adjuvant',)

admin.site.register(Surgery, SurgeryAdmin)
    
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('name','group','sort')
    list_filter = ('group',)

admin.site.register(Diagnosis, DiagnosisAdmin)

class VisualAcuityReadingInline(admin.TabularInline):
    extra = 0
    model = VisualAcuityReading

class VisualAcuityScaleAdmin(admin.ModelAdmin):
    inlines = [
        VisualAcuityReadingInline,
    ]

admin.site.register(VisualAcuityScale, VisualAcuityScaleAdmin)
