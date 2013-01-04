# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EthnicGroup'
        db.create_table('anonymeyes_ethnicgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('anonymeyes', ['EthnicGroup'])

        # Adding model 'Eye'
        db.create_table('anonymeyes_eye', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('anonymeyes', ['Eye'])

        # Adding model 'Diagnosis'
        db.create_table('anonymeyes_diagnosis', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('anonymeyes', ['Diagnosis'])

        # Adding model 'LensStatus'
        db.create_table('anonymeyes_lensstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('anonymeyes', ['LensStatus'])

        # Adding model 'VisualAcuityMethod'
        db.create_table('anonymeyes_visualacuitymethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('anonymeyes', ['VisualAcuityMethod'])

        # Adding model 'Patient'
        db.create_table('anonymeyes_patient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default=UUID('2af64c81-d96c-4c92-956a-db8cba8eff85'), unique=True, max_length=64, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='patient_created_set', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='patient_updated_set', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sex', self.gf('django.db.models.fields.IntegerField')()),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('ethnic_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.EthnicGroup'])),
            ('consanguinity', self.gf('django.db.models.fields.IntegerField')()),
            ('eye', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.Eye'])),
            ('diagnosis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.Diagnosis'])),
            ('lens_status_right', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['anonymeyes.LensStatus'])),
            ('lens_status_left', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['anonymeyes.LensStatus'])),
            ('lens_extraction_date_right', self.gf('django.db.models.fields.DateField')()),
            ('lens_extraction_date_left', self.gf('django.db.models.fields.DateField')()),
            ('visual_acuity_date', self.gf('django.db.models.fields.DateField')()),
            ('visual_acuity_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.VisualAcuityMethod'])),
            ('visual_acuity_right', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('visual_acuity_left', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('visual_acuity_both', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('anonymeyes', ['Patient'])

        # Adding model 'ManagementType'
        db.create_table('anonymeyes_managementtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('anonymeyes', ['ManagementType'])

        # Adding model 'Management'
        db.create_table('anonymeyes_management', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='management_created_set', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='management_updated_set', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('eye', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.Eye'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.ManagementType'])),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.Patient'])),
        ))
        db.send_create_signal('anonymeyes', ['Management'])

        # Adding model 'IOPControl'
        db.create_table('anonymeyes_iopcontrol', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('anonymeyes', ['IOPControl'])

        # Adding model 'Outcome'
        db.create_table('anonymeyes_outcome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='outcome_created_set', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='outcome_updated_set', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('eye', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.Eye'])),
            ('iop_control', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.IOPControl'])),
            ('visual_acuity_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.VisualAcuityMethod'])),
            ('visual_acuity_right', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('visual_acuity_left', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('visual_acuity_both', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anonymeyes.Patient'])),
        ))
        db.send_create_signal('anonymeyes', ['Outcome'])


    def backwards(self, orm):
        # Deleting model 'EthnicGroup'
        db.delete_table('anonymeyes_ethnicgroup')

        # Deleting model 'Eye'
        db.delete_table('anonymeyes_eye')

        # Deleting model 'Diagnosis'
        db.delete_table('anonymeyes_diagnosis')

        # Deleting model 'LensStatus'
        db.delete_table('anonymeyes_lensstatus')

        # Deleting model 'VisualAcuityMethod'
        db.delete_table('anonymeyes_visualacuitymethod')

        # Deleting model 'Patient'
        db.delete_table('anonymeyes_patient')

        # Deleting model 'ManagementType'
        db.delete_table('anonymeyes_managementtype')

        # Deleting model 'Management'
        db.delete_table('anonymeyes_management')

        # Deleting model 'IOPControl'
        db.delete_table('anonymeyes_iopcontrol')

        # Deleting model 'Outcome'
        db.delete_table('anonymeyes_outcome')


    models = {
        'anonymeyes.diagnosis': {
            'Meta': {'object_name': 'Diagnosis'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'management_created_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'eye': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Eye']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Patient']"}),
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
            'Meta': {'object_name': 'Patient'},
            'consanguinity': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'patient_created_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'diagnosis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.Diagnosis']"}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "UUID('55a4082b-54c5-48db-bd09-54253b917988')", 'unique': 'True', 'max_length': '64', 'blank': 'True'}),
            'visual_acuity_both': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'visual_acuity_date': ('django.db.models.fields.DateField', [], {}),
            'visual_acuity_left': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'visual_acuity_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anonymeyes.VisualAcuityMethod']"}),
            'visual_acuity_right': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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