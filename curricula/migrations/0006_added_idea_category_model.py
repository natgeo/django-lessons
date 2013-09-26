# encoding: utf-8
from django.db import models

from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IdeaCategory'
        db.create_table('curricula_ideacategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appropriate_for', self.gf('edumetadata.fields.BigIntegerField')()),
            ('content_body', self.gf('django.db.models.fields.TextField')()),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('credit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['credits.CreditGroup'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('geologic_time', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['edumetadata.GeologicTime'], null=True, blank=True)),
            ('key_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['core_media.NGPhoto'])),
            ('last_updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('license_name', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['licensing.GrantedLicense'])),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('relevant_start_date', self.gf('edumetadata.fields.HistoricalDateField')(null=True, blank=True)),
            ('relevant_end_date', self.gf('edumetadata.fields.HistoricalDateField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('subtitle_guiding_question', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('curricula', ['IdeaCategory'])

        # Adding model 'IdeaCategoryRelation'
        db.create_table('curricula_ideacategoryrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('idea_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.IdeaCategory'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('relation_type', self.gf('django.db.models.fields.CharField')(max_length='200', null=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['IdeaCategoryRelation'])

        # Adding M2M table for field secondary_content_types on 'IdeaCategory'
        db.create_table('curricula_ideacategory_secondary_content_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ideacategory', models.ForeignKey(orm['curricula.ideacategory'], null=False)),
            ('alternatetype', models.ForeignKey(orm['edumetadata.alternatetype'], null=False))
        ))
        db.create_unique('curricula_ideacategory_secondary_content_types', ['ideacategory_id', 'alternatetype_id'])

        # Adding M2M table for field reporting_categories on 'IdeaCategory'
        db.create_table('curricula_ideacategory_reporting_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ideacategory', models.ForeignKey(orm['curricula.ideacategory'], null=False)),
            ('reportingcategory', models.ForeignKey(orm['reporting.reportingcategory'], null=False))
        ))
        db.create_unique('curricula_ideacategory_reporting_categories', ['ideacategory_id', 'reportingcategory_id'])

        # Adding M2M table for field subjects on 'IdeaCategory'
        db.create_table('curricula_ideacategory_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ideacategory', models.ForeignKey(orm['curricula.ideacategory'], null=False)),
            ('subject', models.ForeignKey(orm['edumetadata.subject'], null=False)),
        ))
        db.create_unique('curricula_ideacategory_subjects', ['ideacategory_id', 'subject_id'])

        # Adding M2M table for field grades on 'IdeaCategory'
        db.create_table('curricula_ideacategory_grades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ideacategory', models.ForeignKey(orm['curricula.ideacategory'], null=False)),
            ('grade', models.ForeignKey(orm['edumetadata.grade'], null=False))
        ))
        db.create_unique('curricula_ideacategory_grades', ['ideacategory_id', 'grade_id'])

        # Adding M2M table for field eras on 'IdeaCategory'
        db.create_table('curricula_ideacategory_eras', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ideacategory', models.ForeignKey(orm['curricula.ideacategory'], null=False)),
            ('historicalera', models.ForeignKey(orm['edumetadata.historicalera'], null=False))
        ))
        db.create_unique('curricula_ideacategory_eras', ['ideacategory_id', 'historicalera_id'])

        # Adding model 'Idea'
        db.create_table('curricula_idea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appropriate_for', self.gf('edumetadata.fields.BigIntegerField')()),
            ('content_body', self.gf('django.db.models.fields.TextField')()),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('key_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['core_media.NGPhoto'])),
            ('last_updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['Idea'])

        # Adding model 'CategoryIdea'
        db.create_table('curricula_categoryidea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.IdeaCategory'])),
            ('idea', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.Idea'])),
            
        ))
        db.send_create_signal('curricula', ['CategoryIdea'])

    def backwards(self, orm):
        # Deleting model 'IdeaCategory'
        db.delete_table('curricula_ideacategory')

        # Deleting models
        db.delete_table('curricula_ideacategoryrelation')
        db.delete_table('curricula_categoryidea')

        # Removing M2M tables
        db.delete_table('curricula_ideacategory_secondary_content_types')
        db.delete_table('curricula_ideacategory_reporting_categories')
        db.delete_table('curricula_ideacategory_subjects')
        db.delete_table('curricula_ideacategory_grades')
        db.delete_table('curricula_ideacategory_eras')

        # Deleting model 'Idea'
        db.delete_table('curricula_idea')

    models = {
        'categories.category': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alternate_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'alternate_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_extra': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['categories.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core_media.ngphoto': {
            'Meta': {'object_name': 'NGPhoto'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'allowable_image_use': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'approved': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True'}),
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
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'e_mail': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_permission_letter': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'embargo_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'exif_data': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_pub_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'geocore_account_nbr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'geocore_purchased_for': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'model_release': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'ng_style_credit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'orientation': ('django.db.models.fields.CharField', [], {'default': "'Horizontal'", 'max_length': '50'}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'photoid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'project_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True'}),
            'retract_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rfp_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rights_clear': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'special_restrictions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'spi_record_nbr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'transmission_reference': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'uploaded_file_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vendor_id_nbr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'credits.creditgroup': {
            'Meta': {'ordering': "['title']", 'object_name': 'CreditGroup'},
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
            'appropriate_for': ('edumetadata.fields.BigIntegerField', [], {}),
            'assessment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'background_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'directions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'extending_the_learning': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumetadata.Grade']", 'null': 'True', 'blank': 'True'}),
            'grouping_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.GroupingType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'internet_access_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_modular': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'learner_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.LearnerGroup']", 'null': 'True', 'blank': 'True'}),
            'learning_objectives': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Material']", 'null': 'True', 'blank': 'True'}),
            'notes_on_readability_score': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'other_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pedagogical_purpose_type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'physical_space_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.PhysicalSpaceType']", 'null': 'True', 'blank': 'True'}),
            'plugin_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.PluginType']", 'null': 'True', 'blank': 'True'}),
            'prior_activities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'prior_activities_rel_+'", 'null': 'True', 'to': "orm['curricula.Activity']"}),
            'prior_knowledge': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_content_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumetadata.AlternateType']", 'null': 'True', 'blank': 'True'}),
            'setup': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Skill']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'standards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Standard']", 'null': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumetadata.Subject']", 'null': 'True', 'blank': 'True'}),
            'subtitle_guiding_question': ('django.db.models.fields.TextField', [], {}),
            'teaching_approaches': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.TeachingApproach']", 'null': 'True', 'blank': 'True'}),
            'teaching_method_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.TeachingMethodType']", 'null': 'True', 'blank': 'True'}),
            'tech_setup_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.TechSetupType']", 'null': 'True', 'blank': 'True'}),
            'tips': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Tip']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'curricula.activityrelation': {
            'Meta': {'object_name': 'ActivityRelation'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Activity']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'relation_type': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'null': 'True', 'blank': 'True'})
        },
        'curricula.glossaryterm': {
            'Meta': {'object_name': 'GlossaryTerm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'curricula.groupingtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'GroupingType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'curricula.idea': {
            'Meta': {'ordering': "['title']", 'object_name': 'Idea'},
            'appropriate_for': ('edumetadata.fields.BigIntegerField', [], {}),
            'content_body': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.NGPhoto']", 'null': 'True', 'blank': 'True'}),
            'last_updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
        },
        'curricula.ideacategory': {
            'Meta': {'ordering': "['title']", 'object_name': 'IdeaCategory'},
            'appropriate_for': ('edumetadata.fields.BigIntegerField', [], {}),
            'content_body': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumetadata.Grade']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.NGPhoto']", 'null': 'True', 'blank': 'True'}),
            'last_updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'license_name': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['licensing.GrantedLicense']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_content_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumetadata.AlternateType']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumetadata.Subject']", 'null': 'True', 'blank': 'True'}),
            'subtitle_guiding_question': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'curricula.ideacategoryrelation': {
            'Meta': {'object_name': 'IdeaCategoryRelation'},
            'idea_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.IdeaCategory']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'relation_type': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'null': 'True', 'blank': 'True'})
        },
        'curricula.learnergroup': {
            'Meta': {'object_name': 'LearnerGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
        },
        'curricula.learningobjective': {
            'Meta': {'object_name': 'LearningObjective'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
        },
        'curricula.lesson': {
            'Meta': {'ordering': "['title']", 'object_name': 'Lesson'},
            'ads_excluded': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'appropriate_for': ('edumetadata.fields.BigIntegerField', [], {}),
            'assessment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'background_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'is_modular': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'learning_objectives': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Material']", 'null': 'True', 'blank': 'True'}),
            'other_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'primary_category': ('categories.fields.CategoryFKField', [], {'blank': 'True', 'related_name': "'primary_cat'", 'null': 'True', 'to': "orm['categories.Category']"}),
            'prior_knowledge': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_categories': ('categories.fields.CategoryM2MField', [], {'to': "orm['categories.Category']", 'null': 'True', 'blank': 'True'}),
            'secondary_content_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumetadata.AlternateType']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'subtitle_guiding_question': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Lesson']"}),
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
            'objective': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.LearningObjective']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
        },
        'curricula.physicalspacetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'PhysicalSpaceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
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
            'appropriate_for': ('edumetadata.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'curricula.resource': {
            'Meta': {'object_name': 'Resource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'curricula.resourcecarouselslide': {
            'Meta': {'object_name': 'ResourceCarouselSlide'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'curricula.resourceitem': {
            'Meta': {'object_name': 'ResourceItem'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instructional_resource'", 'to': "orm['curricula.Resource']"})
        },
        'curricula.skill': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Skill'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'appropriate_for': ('edumetadata.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['curricula.Skill']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'curricula.standard': {
            'Meta': {'ordering': "['standard_type', 'name']", 'object_name': 'Standard'},
            'definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['edumetadata.Grade']"}),
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
            'appropriate_for': ('edumetadata.fields.BigIntegerField', [], {}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'curricula.vocabulary': {
            'Meta': {'ordering': "['glossary_term']", 'object_name': 'Vocabulary'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.Activity']"}),
            'glossary_term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curricula.GlossaryTerm']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'edumetadata.alternatetype': {
            'Meta': {'object_name': 'AlternateType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['edumetadata.AlternateType']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'edumetadata.geologictime': {
            'Meta': {'object_name': 'GeologicTime'},
            'end': ('edumetadata.fields.BigIntegerField', [], {}),
            'end_label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'editable': 'False', 'blank': 'True'}),
            'start': ('edumetadata.fields.BigIntegerField', [], {}),
            'start_label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'editable': 'False', 'blank': 'True'}),
        },
        'edumetadata.grade': {
            'Meta': {'ordering': "('order', 'name')", 'object_name': 'Grade'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'default': '99'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'edumetadata.historicalera': {
            'Meta': {'ordering': "('order', 'name')", 'object_name': 'HistoricalEra'},
            'era_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'licensing.grantedlicense': {
            'Meta': {'object_name': 'GrantedLicense'},
            'agreement_expires': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'attribution_name': ('django.db.models.fields.CharField', [], {'max_length': "'100'", 'blank': 'True'}),
            'contact_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_expiration': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'content_expires_after': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license_name': ('django.db.models.fields.CharField', [], {'max_length': "'100'", 'unique': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sublicensable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'})
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
        'resource_carousel.ResourceCategory': {
            'Meta': {'ordering': "('order', 'name')", 'object_name': 'ResourceCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'key_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_media.NGPhoto']", 'null': 'True', 'blank': 'True'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
        }
    }

    complete_apps = ['curricula']
