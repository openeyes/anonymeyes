from django.contrib import admin
from django import forms

from apps.anonymeyes.models import *

admin.site.register(EthnicGroup)
admin.site.register(Eye)
admin.site.register(Diagnosis)
admin.site.register(LensStatus)
admin.site.register(VisualAcuityMethod)
admin.site.register(IOPControl)
admin.site.register(ManagementType)
admin.site.register(Surgery)
admin.site.register(Complication)
admin.site.register(Adjuvant)

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
        widgets = {
                   'visual_acuity_right': forms.TextInput(attrs={'size':'10'}),
                   'visual_acuity_left': forms.TextInput(attrs={'size':'10'}),
                   'visual_acuity_both': forms.TextInput(attrs={'size':'10'}),
        }

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
                   'visual_acuity_right': forms.TextInput(attrs={'size':'10'}),
                   'visual_acuity_left': forms.TextInput(attrs={'size':'10'}),
                   'visual_acuity_both': forms.TextInput(attrs={'size':'10'}),
        }

class PatientAdmin(admin.ModelAdmin):
    form = PatientAdminForm
    readonly_fields = ('created_at', 'updated_at',)
    fieldsets = (
                 (None, {
                         'fields': ('created_by', 'updated_by', 'created_at', 'updated_at', 'sex', 'dob', 'postcode', 'ethnic_group', 'consanguinity')
                         }),
                 ('Baseline Assessment', {
                         'fields': ('eye', 'diagnosis', ('lens_status_right', 'lens_extraction_date_right'), ('lens_status_left', 'lens_extraction_date_left'),
                                    ('visual_acuity_date', 'visual_acuity_method'), ('visual_acuity_right', 'visual_acuity_left', 'visual_acuity_both'))
                         }),
    )
    inlines = [
        ManagementInline,
        OutcomeInline,
    ]

admin.site.register(Patient, PatientAdmin)
