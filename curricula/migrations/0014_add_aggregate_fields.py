# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field reporting_categories on 'Unit'
        db.create_table('curricula_unit_reporting_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('unit', models.ForeignKey(orm['curricula.unit'], null=False)),
            ('reportingcategory', models.ForeignKey(orm['reporting.reportingcategory'], null=False))
        ))
        db.create_unique('curricula_unit_reporting_categories', ['unit_id', 'reportingcategory_id'])

        # Adding field 'Lesson.duration'
        db.add_column('curricula_lesson', 'duration',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Lesson.accessibility_notes'
        db.add_column('curricula_lesson', 'accessibility_notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field subjects on 'Lesson'
        db.create_table('curricula_lesson_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('subject', models.ForeignKey(orm['edumetadata.subject'], null=False))
        ))
        db.create_unique('curricula_lesson_subjects', ['lesson_id', 'subject_id'])

        # Adding M2M table for field grades on 'Lesson'
        db.create_table('curricula_lesson_grades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('grade', models.ForeignKey(orm['edumetadata.grade'], null=False))
        ))
        db.create_unique('curricula_lesson_grades', ['lesson_id', 'grade_id'])

        # Adding M2M table for field physical_space_types on 'Lesson'
        db.create_table('curricula_lesson_physical_space_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('physicalspacetype', models.ForeignKey(orm['curricula.physicalspacetype'], null=False))
        ))
        db.create_unique('curricula_lesson_physical_space_types', ['lesson_id', 'physicalspacetype_id'])

        # Adding M2M table for field plugin_types on 'Lesson'
        db.create_table('curricula_lesson_plugin_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('plugintype', models.ForeignKey(orm['curricula.plugintype'], null=False))
        ))
        db.create_unique('curricula_lesson_plugin_types', ['lesson_id', 'plugintype_id'])

        # Adding M2M table for field tech_setup_types on 'Lesson'
        db.create_table('curricula_lesson_tech_setup_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('techsetuptype', models.ForeignKey(orm['curricula.techsetuptype'], null=False))
        ))
        db.create_unique('curricula_lesson_tech_setup_types', ['lesson_id', 'techsetuptype_id'])


    def backwards(self, orm):
        # Removing M2M table for field reporting_categories on 'Unit'
        db.delete_table('curricula_unit_reporting_categories')

        # Deleting field 'Lesson.duration'
        db.delete_column('curricula_lesson', 'duration')

        # Deleting field 'Lesson.accessibility_notes'
        db.delete_column('curricula_lesson', 'accessibility_notes')

        # Removing M2M table for field subjects on 'Lesson'
        db.delete_table('curricula_lesson_subjects')

        # Removing M2M table for field grades on 'Lesson'
        db.delete_table('curricula_lesson_grades')

        # Removing M2M table for field physical_space_types on 'Lesson'
        db.delete_table('curricula_lesson_physical_space_types')

        # Removing M2M table for field plugin_types on 'Lesson'
        db.delete_table('curricula_lesson_plugin_types')

        # Removing M2M table for field tech_setup_types on 'Lesson'
        db.delete_table('curricula_lesson_tech_setup_types')


    models = {
        'concepts.concept': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Concept'},
            'bbox_e': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'bbox_n': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'bbox_s': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'bbox_w': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_tagged': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'substitute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['concepts.Concept']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'woeid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'concepts.conceptitem': {
            'Meta': {'ordering': "('id',)", 'object_name': 'ConceptItem'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concepts_conceptitem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concepts_conceptitem_items'", 'to': "orm['concepts.Concept']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core_media.embeddedphoto': {
            'Meta': {'object_name': 'EmbeddedPhoto'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.NGPhoto']"})
        },
        'core_media.ngphoto': {
            'Meta': {'object_name': 'NGPhoto'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'allowable_image_use': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True'}),
            'approved': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'asset_versions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'batch_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cleared_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'content_create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'copy_edit_caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'copyright_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'copyright_notice': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'copyright_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'creator_job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'credit_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['credits.CreditGroup']", 'null': 'True', 'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'e_mail': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'effect_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email_permission_letter': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'embargo_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'eras': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.HistoricalEra']", 'null': 'True', 'blank': 'True'}),
            'exif_data': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_pub_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'geocore_account_nbr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'geocore_purchased_for': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'geologic_time': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumetadata.GeologicTime']", 'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Grade']", 'null': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'invoice_nbr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'kill_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_mod_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'last_pub_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_user': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'license_expires': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'licensor_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['licensing.GrantedLicense']", 'null': 'True', 'blank': 'True'}),
            'model_release': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'ng_style_credit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'orientation': ('django.db.models.fields.CharField', [], {'default': "'Horizontal'", 'max_length': '50'}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'photoid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'primary_content_type': ('edumetadata.fields.PrimaryContentTypeField', [], {'blank': 'True', 'related_name': "'primary_ngphoto_set'", 'null': 'True', 'to': "orm['edumetadata.AlternateType']"}),
            'project_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publish_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_end_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_start_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'retract_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rfp_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rights_clear': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'secondary_content_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.AlternateType']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'special_restrictions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'spi_record_nbr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Subject']", 'null': 'True', 'blank': 'True'}),
            'transmission_reference': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'uploaded_file_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vendor_id_nbr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'credits.creditgroup': {
            'Meta': {'object_name': 'CreditGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'other': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'works_cited': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'curricula.activity': {
            'Meta': {'ordering': "['title']", 'object_name': 'Activity'},
            'accessibility_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ads_excluded': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'assessment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'background_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['credits.CreditGroup']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'directions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'eras': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.HistoricalEra']", 'null': 'True', 'blank': 'True'}),
            'extending_the_learning': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geologic_time': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumetadata.GeologicTime']", 'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Grade']", 'null': 'True', 'blank': 'True'}),
            'grouping_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.GroupingType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'internet_access_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_modular': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'learner_groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.LearnerGroup']", 'null': 'True', 'blank': 'True'}),
            'lessons': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Lesson']", 'through': "orm['curricula.LessonActivity']", 'symmetrical': 'False'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.Material']", 'null': 'True', 'blank': 'True'}),
            'notes_on_readability_score': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'other_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pedagogical_purpose_type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'physical_space_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.PhysicalSpaceType']", 'null': 'True', 'blank': 'True'}),
            'plugin_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.PluginType']", 'null': 'True', 'blank': 'True'}),
            'prior_activities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.Activity']", 'null': 'True', 'blank': 'True'}),
            'prior_knowledge': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_end_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_start_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'reporting_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['reporting.ReportingCategory']", 'null': 'True', 'blank': 'True'}),
            'resource_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['resource_carousel.ExternalResource']", 'through': "orm['curricula.ResourceItem']", 'symmetrical': 'False'}),
            'secondary_content_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.AlternateType']", 'null': 'True', 'blank': 'True'}),
            'setup': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.Skill']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'standards': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.Standard']", 'null': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Subject']", 'null': 'True', 'blank': 'True'}),
            'subtitle_guiding_question': ('django.db.models.fields.TextField', [], {}),
            'teaching_approaches': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.TeachingApproach']", 'null': 'True', 'blank': 'True'}),
            'teaching_method_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.TeachingMethodType']", 'null': 'True', 'blank': 'True'}),
            'tech_setup_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.TechSetupType']", 'null': 'True', 'blank': 'True'}),
            'tips': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.Tip']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'vocabulary': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reference.GlossaryTerm']", 'through': "orm['curricula.Vocabulary']", 'symmetrical': 'False'})
        },
        'curricula.activityrelation': {
            'Meta': {'object_name': 'ActivityRelation'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relations'", 'to': "orm['curricula.Activity']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'relation_type': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'null': 'True', 'blank': 'True'})
        },
        'curricula.categoryidea': {
            'Meta': {'object_name': 'CategoryIdea'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.IdeaCategory']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Idea']", 'null': 'True'})
        },
        'curricula.groupingtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'GroupingType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'curricula.idea': {
            'Meta': {'object_name': 'Idea'},
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ideas'", 'symmetrical': 'False', 'through': "orm['curricula.CategoryIdea']", 'to': "orm['curricula.IdeaCategory']"}),
            'content_body': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'key_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.NGPhoto']", 'null': 'True', 'blank': 'True'}),
            'last_updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'})
        },
        'curricula.ideacategory': {
            'Meta': {'object_name': 'IdeaCategory'},
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'content_body': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['credits.CreditGroup']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'eras': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.HistoricalEra']", 'null': 'True', 'blank': 'True'}),
            'geologic_time': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumetadata.GeologicTime']", 'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Grade']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'key_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.NGPhoto']"}),
            'last_updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'license_name': ('django.db.models.fields.related.ForeignKey', [], {'default': '23', 'to': "orm['licensing.GrantedLicense']", 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_end_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_start_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'reporting_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['reporting.ReportingCategory']", 'null': 'True', 'blank': 'True'}),
            'secondary_content_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.AlternateType']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Subject']", 'null': 'True', 'blank': 'True'}),
            'subtitle_guiding_question': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'curricula.ideacategoryrelation': {
            'Meta': {'object_name': 'IdeaCategoryRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relations'", 'to': "orm['curricula.IdeaCategory']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'relation_type': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'null': 'True', 'blank': 'True'})
        },
        'curricula.learnergroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'LearnerGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        },
        'curricula.learningobjective': {
            'Meta': {'ordering': "['text']", 'object_name': 'LearningObjective'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'curricula.lesson': {
            'Meta': {'ordering': "['title']", 'object_name': 'Lesson'},
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Activity']", 'through': "orm['curricula.LessonActivity']", 'symmetrical': 'False'}),
            'ads_excluded': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'assessment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'background_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['credits.CreditGroup']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'eras': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.HistoricalEra']", 'null': 'True', 'blank': 'True'}),
            'geologic_time': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumetadata.GeologicTime']", 'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Grade']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'is_modular': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.Material']", 'null': 'True', 'blank': 'True'}),
            'other_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'physical_space_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.PhysicalSpaceType']", 'null': 'True', 'blank': 'True'}),
            'plugin_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.PluginType']", 'null': 'True', 'blank': 'True'}),
            'prior_knowledge': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'prior_lessons': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.Lesson']", 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_end_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_start_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'reporting_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['reporting.ReportingCategory']", 'null': 'True', 'blank': 'True'}),
            'secondary_content_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.AlternateType']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Subject']", 'null': 'True', 'blank': 'True'}),
            'subtitle_guiding_question': ('django.db.models.fields.TextField', [], {}),
            'tech_setup_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['curricula.TechSetupType']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Unit']", 'through': "orm['curricula.UnitLesson']", 'symmetrical': 'False'})
        },
        'curricula.lessonactivity': {
            'Meta': {'ordering': "('order',)", 'object_name': 'LessonActivity'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Lesson']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'transition_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'curricula.lessonrelation': {
            'Meta': {'object_name': 'LessonRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relations'", 'to': "orm['curricula.Lesson']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'relation_type': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'null': 'True', 'blank': 'True'})
        },
        'curricula.material': {
            'Meta': {'ordering': "['name']", 'object_name': 'Material'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'curricula.objectiverelation': {
            'Meta': {'object_name': 'ObjectiveRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'objective': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.LearningObjective']"})
        },
        'curricula.physicalspacetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'PhysicalSpaceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'curricula.plugintype': {
            'Meta': {'ordering': "['name']", 'object_name': 'PluginType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'curricula.questionanswer': {
            'Meta': {'object_name': 'QuestionAnswer'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Activity']"}),
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'curricula.resourceitem': {
            'Meta': {'object_name': 'ResourceItem'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['curricula.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instructional_resource'", 'to': "orm['resource_carousel.ExternalResource']"})
        },
        'curricula.skill': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Skill'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['curricula.Skill']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'curricula.standard': {
            'Meta': {'ordering': "['standard_type', 'name']", 'object_name': 'Standard'},
            'definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumetadata.Grade']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'standard_type': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'thinkfinity_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'when_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'curricula.teachingapproach': {
            'Meta': {'ordering': "['name']", 'object_name': 'TeachingApproach'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'curricula.teachingmethodtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'TeachingMethodType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'curricula.techsetuptype': {
            'Meta': {'ordering': "['title']", 'object_name': 'TechSetupType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'curricula.tip': {
            'Meta': {'ordering': "['category', 'body']", 'object_name': 'Tip'},
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.TipCategory']", 'null': 'True', 'blank': 'True'}),
            'content_creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'tip_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'curricula.tipcategory': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'TipCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['curricula.TipCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'curricula.unit': {
            'Meta': {'ordering': "['title']", 'object_name': 'Unit'},
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['credits.CreditGroup']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'eras': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.HistoricalEra']", 'null': 'True', 'blank': 'True'}),
            'geologic_time': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumetadata.GeologicTime']", 'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Grade']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'key_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.NGPhoto']"}),
            'lessons': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Lesson']", 'through': "orm['curricula.UnitLesson']", 'symmetrical': 'False'}),
            'overview': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_end_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_start_date': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'reporting_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['reporting.ReportingCategory']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Subject']", 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'curricula.unitlesson': {
            'Meta': {'ordering': "('order',)", 'object_name': 'UnitLesson'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Lesson']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'transition_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Unit']"})
        },
        'curricula.unitrelation': {
            'Meta': {'object_name': 'UnitRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'relation_type': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relations'", 'to': "orm['curricula.Unit']"})
        },
        'curricula.vocabulary': {
            'Meta': {'ordering': "['glossary_term']", 'object_name': 'Vocabulary'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['curricula.Activity']"}),
            'glossary_term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reference.GlossaryTerm']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'edu_core.audiencetype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AudienceType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'default_audience_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edu_core.AudienceType']", 'null': 'True', 'blank': 'True'}),
            'default_reading_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edu_core.ReadingLevel']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'singular_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thinkfinity_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'edu_core.onpageitem': {
            'Meta': {'unique_together': "(('on_page', 'audience_type'),)", 'object_name': 'OnPageItem'},
            'audience_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edu_core.AudienceType']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'onpageitem_related'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'on_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['page.Page']"})
        },
        'edu_core.readinglevel': {
            'Meta': {'ordering': "('sort_order', 'id')", 'object_name': 'ReadingLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'edumetadata.alternatetype': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'AlternateType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alternate_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['edumetadata.AlternateType']"}),
            'resource_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'edumetadata.geologictime': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'GeologicTime'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end': ('django.db.models.fields.BigIntegerField', [], {}),
            'end_label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['edumetadata.GeologicTime']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start': ('django.db.models.fields.BigIntegerField', [], {}),
            'start_label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'edumetadata.grade': {
            'Meta': {'ordering': "('order', 'name')", 'object_name': 'Grade'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'default': '99'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'edumetadata.historicalera': {
            'Meta': {'object_name': 'HistoricalEra'},
            'end': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'era_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start': ('edumetadata.fields.HistoricalDateField', [], {})
        },
        'edumetadata.subject': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Subject'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'more_info_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['edumetadata.Subject']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'layout.layoutmode': {
            'Meta': {'object_name': 'LayoutMode'},
            'blocks': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'licensing.grantedlicense': {
            'Meta': {'object_name': 'GrantedLicense'},
            'agreement_expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'allowed_contexts': ('licensing.widgets.MultiSelectField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'allowed_jurisdictions': ('licensing.widgets.MultiSelectField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'allowed_media': ('licensing.widgets.MultiSelectField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'allowed_modifications': ('licensing.widgets.MultiSelectField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attribution_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'contact_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_expiration': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'content_expires_after': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licensor_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sublicensable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'page.page': {
            'Meta': {'unique_together': "(('site', 'url'), ('site', 'lookup_url', 'release_time'))", 'object_name': 'Page'},
            'a_z_page_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'approved': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'content_create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'embargo_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_pub_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_a_to_z': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_auto_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_only_maintained_manually': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_mod_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'last_pub_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'layout_mode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['layout.LayoutMode']", 'null': 'True'}),
            'lookup_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'modified': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ngphoto_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'pc_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_primary_content_ctype'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'pc_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.EmbeddedPhoto']", 'null': 'True', 'blank': 'True'}),
            'pm_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_primary_media_ctype'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'pm_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'primary_taxonomy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary_page_set'", 'null': 'True', 'to': "orm['taxonomy.Taxi']"}),
            'published': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'qa_check': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'release_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'retract_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_taxonomy': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'secondary_page_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['taxonomy.Taxi']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wpf_pages'", 'null': 'True', 'to': "orm['sites.Site']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'virtual_page': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'reference.fastfact': {
            'Meta': {'ordering': "('name',)", 'object_name': 'FastFact'},
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'fact': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'reference.fastfactitem': {
            'Meta': {'object_name': 'FastFactItem'},
            'fast_fact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'article_facts'", 'to': "orm['reference.FastFact']"}),
            'generic_article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reference.GenericArticle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'reference.genericarticle': {
            'Meta': {'unique_together': "(('slug', 'primary_content_type'),)", 'object_name': 'GenericArticle'},
            'ads_excluded': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'credit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['credits.CreditGroup']", 'null': 'True', 'blank': 'True'}),
            'eras': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.HistoricalEra']", 'null': 'True', 'blank': 'True'}),
            'fast_facts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reference.FastFact']", 'through': "orm['reference.FastFactItem']", 'symmetrical': 'False'}),
            'geologic_time': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edumetadata.GeologicTime']", 'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Grade']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'is_modular': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'key_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.NGPhoto']", 'null': 'True', 'blank': 'True'}),
            'license_name': ('django.db.models.fields.related.ForeignKey', [], {'default': '23', 'to': "orm['licensing.GrantedLicense']", 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'primary_content_type': ('edumetadata.fields.PrimaryContentTypeField', [], {'blank': 'True', 'related_name': "'primary_genericarticle_set'", 'null': 'True', 'to': "orm['edumetadata.AlternateType']"}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publish_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relevant_end': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'relevant_start': ('edumetadata.fields.HistoricalDateField', [], {'null': 'True', 'blank': 'True'}),
            'reporting_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['reporting.ReportingCategory']", 'null': 'True', 'blank': 'True'}),
            'secondary_content_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.AlternateType']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'subjects_and_disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['edumetadata.Subject']", 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tab_label': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'vocabulary': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reference.GlossaryTerm']", 'through': "orm['reference.Vocabulary']", 'symmetrical': 'False'})
        },
        'reference.glossaryterm': {
            'Meta': {'ordering': "('word_lower',)", 'object_name': 'GlossaryTerm'},
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'audio': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'definition': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'generic_article': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'glossary_term'", 'unique': 'True', 'null': 'True', 'to': "orm['reference.GenericArticle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.NGPhoto']", 'null': 'True', 'blank': 'True'}),
            'part_of_speech': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonetic': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'primary_content_type': ('edumetadata.fields.PrimaryContentTypeField', [], {'blank': 'True', 'related_name': "'primary_glossaryterm_set'", 'null': 'True', 'to': "orm['edumetadata.AlternateType']"}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'word_lower': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        'reference.vocabulary': {
            'Meta': {'ordering': "['glossary_term']", 'object_name': 'Vocabulary'},
            'generic_article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['reference.GenericArticle']"}),
            'glossary_term': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'article_terms'", 'to': "orm['reference.GlossaryTerm']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'reporting.reportingcategory': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'ReportingCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['reporting.ReportingCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'resource_carousel.externalresource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'ExternalResource'},
            'appropriate_for': ('django.db.models.fields.BigIntegerField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['resource_carousel.ResourceCategory']", 'null': 'True', 'blank': 'True'}),
            'citation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_ref': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'key_image_custom': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'key_image_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'key_image_related': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'externalresources'", 'null': 'True', 'to': "orm['core_media.NGPhoto']"}),
            'key_image_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resource_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'resource_carousel.resourcecategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ResourceCategory'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'externalresourcecategories'", 'null': 'True', 'to': "orm['core_media.NGPhoto']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'externalresourcecategories'", 'null': 'True', 'to': "orm['credits.CreditGroup']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.sitetaxonomy': {
            'Meta': {'object_name': 'SiteTaxonomy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'taxonomy.taxi': {
            'Meta': {'ordering': "['path']", 'object_name': 'Taxi'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Taxi']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site_taxonomy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.SiteTaxonomy']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['curricula']