from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms

from apps.anonymeyes.models import *

admin.site.register(IOPAgent)
admin.site.register(EthnicGroupGroup)
admin.site.register(Country)
admin.site.register(DiagnosisGroup)
admin.site.register(LensStatus)
admin.site.register(VisualAcuityMethod)
admin.site.register(ManagementType)
admin.site.register(Complication)
admin.site.register(Adjuvant)
admin.site.register(Tonometry)

class EthnicGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'sort')
    list_filter = ('group',)

admin.site.register(EthnicGroup, EthnicGroupAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'last_login', 'is_active', 'is_staff')
    inlines = [ UserProfileInline, ]
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

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
                         'fields': ('created_by', 'updated_by', 'created_at', 'updated_at',
                                    'sex', 'dob_day', 'dob_month', 'dob_year',
                                    'country', 'postcode', 'health_care',
                                    'ethnic_group', 'ethnic_group_comment',
                                    'consanguinity', 'history', 'history_comment',
                                    'comments',
                                     )
                         }),
                 ('Diagnosis', {
                         'fields': ('visual_acuity_date', 'diagnosis_right', 'diagnosis_right_comment',
                                    'diagnosis_left', 'diagnosis_left_comment')
                         }),
                 ('Lens Status', {
                         'fields': (
                                    ('lens_status_right', 'lens_extraction_date_right'),
                                    ('lens_status_left', 'lens_extraction_date_left')
                                    )
                         }),
                 ('Visual Acuity', {
                         'fields': ('visual_acuity_method', 'visual_acuity_method_comment',
                                     'visual_acuity_right', 'visual_acuity_correction_right',
                                     'visual_acuity_left', 'visual_acuity_correction_left',
                                     'visual_acuity_both', 'visual_acuity_correction_both',
                                     'visual_acuity_scale', 'visual_acuity_fixation_preference')
                         }),
                 ('IOP', {
                         'fields': ('iop_right', 'iop_left', 'tonometry',
                                     'iop_agents_right', 'iop_agents_left', 'eua')
                         }),
    )
    inlines = [
        ManagementInline,
        OutcomeInline,
    ]
    list_display = ('uuid', 'sex', 'dob_year', 'postcode', 'outcome_status', 'created_by_name', 'visual_acuity_date', 'created_at', 'updated_at')

    def created_by_name(self, obj):
        return '%s %s (%s)' % (obj.created_by.first_name, obj.created_by.last_name, obj.created_by.email)
    created_by_name.short_description = 'Created by'

    def outcome_status(self, obj):
        if obj.outcome_overdue:
            text = 'Overdue'
            background = 'red'
            color = 'white'
        elif not obj.next_reminder:
            text = 'Complete'
            background = 'grey'
            color = 'white'
        elif obj.outcome_due:
            text = 'Due'
            background = 'orange'
            color = 'white'
        else:
            text = 'Not due'
            background = 'green'
            color = 'white'
        return '<div style="background-color:%s; padding: 3px; color: %s">%s</div>' % (background, color, text)
    outcome_status.allow_tags = True

    list_filter = ('sex', 'dob_year', 'created_at', 'updated_at')
    search_fields = ('postcode', 'diagnosis_right__name', 'diagnosis_left__name')
    
admin.site.register(Patient, PatientAdmin)

class SurgeryAdmin(admin.ModelAdmin):
    list_display = ('name', 'adjuvant', 'sort')
    list_filter = ('adjuvant',)

admin.site.register(Surgery, SurgeryAdmin)
    
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'sort')
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
