# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from uuid import UUID


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Patient.diagnosis'
        db.delete_column('anonymeyes_patient', 'diagnosis_id')

        # Adding field 'Patient.diagnosis_left'
        db.add_column('anonymeyes_patient', 'diagnosis_left',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='+', to=orm['anonymeyes.Diagnosis']),
                      keep_default=False)

        # Adding field 'Patient.diagnosis_right'
        db.add_column('anonymeyes_patient', 'diagnosis_right',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='+', to=orm['anonymeyes.Diagnosis']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Patient.diagnosis'
        db.add_column('anonymeyes_patient', 'diagnosis',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['anonymeyes.Diagnosis']),
                      keep_default=False)

        # Deleting field 'Patient.diagnosis_left'
        db.delete_column('anonymeyes_patient', 'diagnosis_left_id')

        # Deleting field 'Patient.diagnosis_right'
        db.delete_column('anonymeyes_patient', 'diagnosis_right_id')


    models = {
        'anonymeyes.adjuvant': {
            'Meta': {'object_name': 'Adjuvant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'anonymeyes.complication': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'Complication'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'anonymeyes.diagnosis': {
            'Meta': {'ordering': "['group__sort', 'sort', 'name']", 'object_name': 'Diagnosis'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.DiagnosisGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'anonymeyes.diagnosisgroup': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'DiagnosisGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'anonymeyes.ethnicgroup': {
            'Meta': {'object_name': 'EthnicGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'anonymeyes.eye': {
            'Meta': {'object_name': 'Eye'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'anonymeyes.iopcontrol': {
            'Meta': {'object_name': 'IOPControl'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
            'eye': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Eye']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Patient']"}),
            'surgery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Surgery']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.ManagementType']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'management_updated_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"})
        },
        'anonymeyes.managementtype': {
            'Meta': {'object_name': 'ManagementType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'anonymeyes.outcome': {
            'Meta': {'object_name': 'Outcome'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'outcome_created_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'eye': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Eye']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iop_control': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.IOPControl']"}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Patient']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'outcome_updated_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'visual_acuity_both': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'visual_acuity_left': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'visual_acuity_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.VisualAcuityMethod']"}),
            'visual_acuity_right': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'anonymeyes.patient': {
            'Meta': {'ordering': "['-updated_at']", 'object_name': 'Patient'},
            'consanguinity': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'patient_created_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'diagnosis_left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['anonymeyes.Diagnosis']"}),
            'diagnosis_right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['anonymeyes.Diagnosis']"}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'ethnic_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.EthnicGroup']"}),
            'eye': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Eye']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lens_extraction_date_left': ('django.db.models.fields.DateField', [], {}),
            'lens_extraction_date_right': ('django.db.models.fields.DateField', [], {}),
            'lens_status_left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['anonymeyes.LensStatus']"}),
            'lens_status_right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['anonymeyes.LensStatus']"}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'sex': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'patient_updated_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "UUID('b74172ef-1fcf-43c7-bdb4-4933dfd136b9')", 'unique': 'True', 'max_length': '64', 'blank': 'True'}),
            'visual_acuity_both': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'visual_acuity_date': ('django.db.models.fields.DateField', [], {}),
            'visual_acuity_left': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'visual_acuity_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.VisualAcuityMethod']"}),
            'visual_acuity_right': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'anonymeyes.surgery': {
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'Surgery'},
            'adjuvant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'anonymeyes.visualacuitymethod': {
            'Meta': {'object_name': 'VisualAcuityMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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