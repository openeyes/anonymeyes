# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from uuid import UUID


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Patient.eua'
        db.alter_column('anonymeyes_patient', 'eua', self.gf('django.db.models.fields.BooleanField')())

    def backwards(self, orm):

        # Changing field 'Patient.eua'
        db.alter_column('anonymeyes_patient', 'eua', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'anonymeyes.adjuvant': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'Adjuvant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.anaesthesia': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'Anaesthesia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.complication': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'Complication'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.diagnosis': {
            'Meta': {'ordering': "['group__sort', 'sort', 'name']", 'object_name': 'Diagnosis'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.DiagnosisGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.diagnosisgroup': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'DiagnosisGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.dobprecision': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'DOBPrecision'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.ethnicgroup': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'EthnicGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.eye': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'Eye'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'single': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.healthcare': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'HealthCare'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.lensstatus': {
            'Meta': {'object_name': 'LensStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'anonymeyes.management': {
            'Meta': {'object_name': 'Management'},
            'adjuvant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Adjuvant']", 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'complication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Complication']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'management_created_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'eye': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Eye']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Patient']"}),
            'surgery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Surgery']", 'null': 'True', 'blank': 'True'}),
            'surgery_stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.SurgeryStage']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.ManagementType']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'management_updated_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"})
        },
        'anonymeyes.managementtype': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'ManagementType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.outcome': {
            'Meta': {'object_name': 'Outcome'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'outcome_created_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'eye': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Eye']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iop_agents': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'iop_control': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Patient']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'outcome_updated_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'visual_acuity_both': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outcome_beo'", 'to': "orm['anonymeyes.VisualAcuityReading']"}),
            'visual_acuity_correction_both': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outcome_beo_correction'", 'to': "orm['anonymeyes.VisualAcuityCorrection']"}),
            'visual_acuity_correction_left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outcome_lva_correction'", 'to': "orm['anonymeyes.VisualAcuityCorrection']"}),
            'visual_acuity_correction_right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outcome_rva_correction'", 'to': "orm['anonymeyes.VisualAcuityCorrection']"}),
            'visual_acuity_left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outcome_lva'", 'to': "orm['anonymeyes.VisualAcuityReading']"}),
            'visual_acuity_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.VisualAcuityMethod']"}),
            'visual_acuity_right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outcome_rva'", 'to': "orm['anonymeyes.VisualAcuityReading']"})
        },
        'anonymeyes.patient': {
            'Meta': {'ordering': "['-updated_at']", 'object_name': 'Patient'},
            'anaesthesia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Anaesthesia']", 'null': 'True', 'blank': 'True'}),
            'consanguinity': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'patient_created_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'diagnosis_left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['anonymeyes.Diagnosis']"}),
            'diagnosis_right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['anonymeyes.Diagnosis']"}),
            'dob_day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dob_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dob_year': ('django.db.models.fields.IntegerField', [], {}),
            'ethnic_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.EthnicGroup']"}),
            'eua': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'health_care': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.HealthCare']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iop_left': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'iop_right': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lens_extraction_date_left': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lens_extraction_date_right': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lens_status_left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['anonymeyes.LensStatus']"}),
            'lens_status_right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['anonymeyes.LensStatus']"}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'sex': ('django.db.models.fields.IntegerField', [], {}),
            'tonometry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Tonometry']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'patient_updated_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "UUID('a4de1a3f-6c16-4ca5-a65c-17a8caa5278c')", 'unique': 'True', 'max_length': '64', 'blank': 'True'}),
            'visual_acuity_both': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'patient_beo'", 'to': "orm['anonymeyes.VisualAcuityReading']"}),
            'visual_acuity_correction_both': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'patient_beo_correction'", 'to': "orm['anonymeyes.VisualAcuityCorrection']"}),
            'visual_acuity_correction_left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'patient_lva_correction'", 'to': "orm['anonymeyes.VisualAcuityCorrection']"}),
            'visual_acuity_correction_right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'patient_rva_correction'", 'to': "orm['anonymeyes.VisualAcuityCorrection']"}),
            'visual_acuity_date': ('django.db.models.fields.DateField', [], {}),
            'visual_acuity_left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'patient_lva'", 'to': "orm['anonymeyes.VisualAcuityReading']"}),
            'visual_acuity_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.VisualAcuityMethod']"}),
            'visual_acuity_right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'patient_rva'", 'to': "orm['anonymeyes.VisualAcuityReading']"})
        },
        'anonymeyes.surgery': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'Surgery'},
            'adjuvant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'stage': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'anonymeyes.surgerystage': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'SurgeryStage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.tonometry': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'Tonometry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'dob_precision': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['anonymeyes.DOBPrecision']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'anonymeyes.visualacuitycorrection': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'VisualAcuityCorrection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.visualacuitymethod': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'VisualAcuityMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.VisualAcuityScale']"}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'anonymeyes.visualacuityreading': {
            'Meta': {'ordering': "['scale__name', 'sort', 'name']", 'object_name': 'VisualAcuityReading'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'readings'", 'to': "orm['anonymeyes.VisualAcuityScale']"}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'anonymeyes.visualacuityscale': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'VisualAcuityScale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['anonymeyes']