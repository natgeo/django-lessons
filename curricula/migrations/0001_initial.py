# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupingType'
        db.create_table('curricula_groupingtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('curricula', ['GroupingType'])

        # Adding model 'LearnerGroup'
        db.create_table('curricula_learnergroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=31)),
        ))
        db.send_create_signal('curricula', ['LearnerGroup'])

        # Adding model 'Material'
        db.create_table('curricula_material', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('curricula', ['Material'])

        # Adding model 'PhysicalSpaceType'
        db.create_table('curricula_physicalspacetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('is_default', self.gf('django.db.models.fields.NullBooleanField')(null=True)),
        ))
        db.send_create_signal('curricula', ['PhysicalSpaceType'])

        # Adding model 'PluginType'
        db.create_table('curricula_plugintype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('curricula', ['PluginType'])

        # Adding model 'Skill'
        db.create_table('curricula_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['curricula.Skill'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('appropriate_for', self.gf('edumetadata.fields.BigIntegerField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['Skill'])

        # Adding unique constraint on 'Skill', fields ['parent', 'name']
        db.create_unique('curricula_skill', ['parent_id', 'name'])

        # Adding model 'TeachingApproach'
        db.create_table('curricula_teachingapproach', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('curricula', ['TeachingApproach'])

        # Adding model 'TeachingMethodType'
        db.create_table('curricula_teachingmethodtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('curricula', ['TeachingMethodType'])

        # Adding model 'TechSetupType'
        db.create_table('curricula_techsetuptype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('curricula', ['TechSetupType'])

        # Adding model 'TipCategory'
        db.create_table('curricula_tipcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['curricula.TipCategory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('curricula', ['TipCategory'])

        # Adding unique constraint on 'TipCategory', fields ['parent', 'name']
        db.create_unique('curricula_tipcategory', ['parent_id', 'name'])

        # Adding model 'Tip'
        db.create_table('curricula_tip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appropriate_for', self.gf('edumetadata.fields.BigIntegerField')()),
            ('content_creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id_number', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('tip_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.TipCategory'], null=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['Tip'])

        # Adding model 'Standard'
        db.create_table('curricula_standard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('definition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('standard_type', self.gf('django.db.models.fields.IntegerField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('thinkfinity_code', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('when_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['Standard'])

        # Adding M2M table for field grades on 'Standard'
        db.create_table('curricula_standard_grades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('standard', models.ForeignKey(orm['curricula.standard'], null=False)),
            ('grade', models.ForeignKey(orm['edumetadata.grade'], null=False))
        ))
        db.create_unique('curricula_standard_grades', ['standard_id', 'grade_id'])

        # Adding model 'Activity'
        db.create_table('curricula_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appropriate_for', self.gf('edumetadata.fields.BigIntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('ads_excluded', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('assessment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('assessment_type', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('extending_the_learning', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('is_modular', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notes_on_readability_score', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pedagogical_purpose_type', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('subtitle_guiding_question', self.gf('django.db.models.fields.TextField')()),
            ('directions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('learning_objectives', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('accessibility_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('other_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('setup', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internet_access_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('background_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('prior_knowledge', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('credit', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True)),
            ('geologic_time', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True)),
            ('relevant_start_date', self.gf('edumetadata.fields.HistoricalDateField')(null=True, blank=True)),
            ('relevant_end_date', self.gf('edumetadata.fields.HistoricalDateField')(null=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['Activity'])

        # Adding M2M table for field grades on 'Activity'
        db.create_table('curricula_activity_grades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('grade', models.ForeignKey(orm['edumetadata.grade'], null=False))
        ))
        db.create_unique('curricula_activity_grades', ['activity_id', 'grade_id'])

        # Adding M2M table for field learner_groups on 'Activity'
        db.create_table('curricula_activity_learner_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('learnergroup', models.ForeignKey(orm['curricula.learnergroup'], null=False))
        ))
        db.create_unique('curricula_activity_learner_groups', ['activity_id', 'learnergroup_id'])

        # Adding M2M table for field standards on 'Activity'
        db.create_table('curricula_activity_standards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('standard', models.ForeignKey(orm['curricula.standard'], null=False))
        ))
        db.create_unique('curricula_activity_standards', ['activity_id', 'standard_id'])

        # Adding M2M table for field subjects on 'Activity'
        db.create_table('curricula_activity_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('subject', models.ForeignKey(orm['edumetadata.subject'], null=False))
        ))
        db.create_unique('curricula_activity_subjects', ['activity_id', 'subject_id'])

        # Adding M2M table for field tips on 'Activity'
        db.create_table('curricula_activity_tips', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('tip', models.ForeignKey(orm['curricula.tip'], null=False))
        ))
        db.create_unique('curricula_activity_tips', ['activity_id', 'tip_id'])

        # Adding M2M table for field skills on 'Activity'
        db.create_table('curricula_activity_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('skill', models.ForeignKey(orm['curricula.skill'], null=False))
        ))
        db.create_unique('curricula_activity_skills', ['activity_id', 'skill_id'])

        # Adding M2M table for field teaching_approaches on 'Activity'
        db.create_table('curricula_activity_teaching_approaches', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('teachingapproach', models.ForeignKey(orm['curricula.teachingapproach'], null=False))
        ))
        db.create_unique('curricula_activity_teaching_approaches', ['activity_id', 'teachingapproach_id'])

        # Adding M2M table for field teaching_method_types on 'Activity'
        db.create_table('curricula_activity_teaching_method_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('teachingmethodtype', models.ForeignKey(orm['curricula.teachingmethodtype'], null=False))
        ))
        db.create_unique('curricula_activity_teaching_method_types', ['activity_id', 'teachingmethodtype_id'])

        # Adding M2M table for field materials on 'Activity'
        db.create_table('curricula_activity_materials', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('material', models.ForeignKey(orm['curricula.material'], null=False))
        ))
        db.create_unique('curricula_activity_materials', ['activity_id', 'material_id'])

        # Adding M2M table for field grouping_types on 'Activity'
        db.create_table('curricula_activity_grouping_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('groupingtype', models.ForeignKey(orm['curricula.groupingtype'], null=False))
        ))
        db.create_unique('curricula_activity_grouping_types', ['activity_id', 'groupingtype_id'])

        # Adding M2M table for field physical_space_types on 'Activity'
        db.create_table('curricula_activity_physical_space_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('physicalspacetype', models.ForeignKey(orm['curricula.physicalspacetype'], null=False))
        ))
        db.create_unique('curricula_activity_physical_space_types', ['activity_id', 'physicalspacetype_id'])

        # Adding M2M table for field prior_activities on 'Activity'
        db.create_table('curricula_activity_prior_activities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('to_activity', models.ForeignKey(orm['curricula.activity'], null=False))
        ))
        db.create_unique('curricula_activity_prior_activities', ['from_activity_id', 'to_activity_id'])

        # Adding M2M table for field plugin_types on 'Activity'
        db.create_table('curricula_activity_plugin_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('plugintype', models.ForeignKey(orm['curricula.plugintype'], null=False))
        ))
        db.create_unique('curricula_activity_plugin_types', ['activity_id', 'plugintype_id'])

        # Adding M2M table for field tech_setup_types on 'Activity'
        db.create_table('curricula_activity_tech_setup_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('techsetuptype', models.ForeignKey(orm['curricula.techsetuptype'], null=False))
        ))
        db.create_unique('curricula_activity_tech_setup_types', ['activity_id', 'techsetuptype_id'])

        # Adding M2M table for field reporting_categories on 'Activity'
        db.create_table('curricula_activity_reporting_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('reporting_categories', models.ForeignKey(orm['reporting.reportingcategory'], null=False))
        ))
        db.create_unique('curricula_activity_reporting_categories', ['activity_id', 'reportingcategory_id'])

        # Adding M2M table for field secondary_content_types on 'Activity'
        db.create_table('curricula_activity_secondary_content_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('alternatetype', models.ForeignKey(orm['edumetadata.alternatetype'], null=False))
        ))
        db.create_unique('curricula_activity_secondary_content_types', ['activity_id', 'alternatetype_id'])

        # Adding M2M table for field eras on 'Activity'
        db.create_table('curricula_activity_eras', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['curricula.activity'], null=False)),
            ('historicalera', models.ForeignKey(orm['edumetadata.historicalera'], null=False))
        ))
        db.create_unique('curricula_activity_eras', ['activity_id', 'historicalera_id'])

        # Adding model 'Vocabulary'
        db.create_table('curricula_vocabulary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.Activity'])),
            ('glossary_term', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.GlossaryTerm'])),
        ))
        db.send_create_signal('curricula', ['Vocabulary'])

        # Adding model 'QuestionAnswer'
        db.create_table('curricula_questionanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.Activity'])),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('appropriate_for', self.gf('edumetadata.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['QuestionAnswer'])

        # Adding model 'ResourceItem'
        db.create_table('curricula_resourceitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.Activity'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instructional_resource', to=orm['curricula.Resource'])),
        ))
        db.send_create_signal('curricula', ['ResourceItem'])

        # Adding model 'ActivityRelation'
        db.create_table('curricula_activityrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.Activity'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('relation_type', self.gf('django.db.models.fields.CharField')(max_length='200', null=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['ActivityRelation'])

        # Adding model 'Lesson'
        db.create_table('curricula_lesson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('ads_excluded', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('geologic_time', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True)),
            ('id_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('is_modular', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('subtitle_guiding_question', self.gf('django.db.models.fields.TextField')()),
            ('assessment_type', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('assessment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('learning_objectives', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('other_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('background_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('appropriate_for', self.gf('edumetadata.fields.BigIntegerField')()),
            ('relevant_start_date', self.gf('edumetadata.fields.HistoricalDateField')(null=True, blank=True)),
            ('relevant_end_date', self.gf('edumetadata.fields.HistoricalDateField')(null=True, blank=True)),
            ('primary_category', self.gf('categories.fields.CategoryFKField')(blank=True, related_name='primary_cat', null=True, to=orm['categories.Category'])),
        ))
        db.send_create_signal('curricula', ['Lesson'])

        # Adding M2M table for field secondary_content_types on 'Lesson'
        db.create_table('curricula_lesson_secondary_content_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('alternatetype', models.ForeignKey(orm['edumetadata.alternatetype'], null=False))
        ))
        db.create_unique('curricula_lesson_secondary_content_types', ['lesson_id', 'alternatetype_id'])

        # Adding M2M table for field materials on 'Lesson'
        db.create_table('curricula_lesson_materials', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('material', models.ForeignKey(orm['curricula.material'], null=False))
        ))
        db.create_unique('curricula_lesson_materials', ['lesson_id', 'material_id'])

        # Adding M2M table for field reporting_categories on 'Lesson'
        db.create_table('curricula_lesson_reporting_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('reporting_categories', models.ForeignKey(orm['reporting.reportingcategory'], null=False))
        ))
        db.create_unique('curricula_lesson_reporting_categories', ['lesson_id', 'reportingcategory_id'])

        # Adding M2M table for field eras on 'Lesson'
        db.create_table('curricula_lesson_eras', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('historicalera', models.ForeignKey(orm['edumetadata.historicalera'], null=False))
        ))
        db.create_unique('curricula_lesson_eras', ['lesson_id', 'historicalera_id'])

        # Adding M2M table for field secondary_categories on 'Lesson'
        db.create_table('curricula_lesson_secondary_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['curricula.lesson'], null=False)),
            ('category', models.ForeignKey(orm['categories.category'], null=False))
        ))
        db.create_unique('curricula_lesson_secondary_categories', ['lesson_id', 'category_id'])

        # Adding model 'LessonRelation'
        db.create_table('curricula_lessonrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.Lesson'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('relation_type', self.gf('django.db.models.fields.CharField')(max_length='200', null=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['LessonRelation'])

        # Adding model 'LessonActivity'
        db.create_table('curricula_lessonactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.Lesson'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curricula.Activity'])),
            ('transition_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('curricula', ['LessonActivity'])


    def backwards(self, orm):
        
        # Removing unique constraints
        db.delete_unique('curricula_tipcategory', ['parent_id', 'name'])
        db.delete_unique('curricula_skill', ['parent_id', 'name'])

        # Deleting models
        db.delete_table('curricula_glossaryterm')
        db.delete_table('curricula_resource')
        db.delete_table('curricula_resourcecarouselslide')
        db.delete_table('curricula_groupingtype')
        db.delete_table('curricula_learnergroup')
        db.delete_table('curricula_material')
        db.delete_table('curricula_physicalspacetype')
        db.delete_table('curricula_plugintype')
        db.delete_table('curricula_skill')
        db.delete_table('curricula_teachingapproach')
        db.delete_table('curricula_teachingmethodtype')
        db.delete_table('curricula_techsetuptype')
        db.delete_table('curricula_tipcategory')
        db.delete_table('curricula_tip')
        db.delete_table('curricula_standard')

        # Removing M2M table for field grades on 'Standard'
        db.delete_table('curricula_standard_grades')

        # Deleting model 'Activity'
        db.delete_table('curricula_activity')

        # Removing M2M tables
        db.delete_table('curricula_activity_grades')
        db.delete_table('curricula_activity_learner_groups')
        db.delete_table('curricula_activity_standards')
        db.delete_table('curricula_activity_subjects')
        db.delete_table('curricula_activity_tips')
        db.delete_table('curricula_activity_skills')
        db.delete_table('curricula_activity_teaching_approaches')
        db.delete_table('curricula_activity_teaching_method_types')
        db.delete_table('curricula_activity_materials')
        db.delete_table('curricula_activity_grouping_types')
        db.delete_table('curricula_activity_physical_space_types')
        db.delete_table('curricula_activity_prior_activities')
        db.delete_table('curricula_activity_plugin_types')
        db.delete_table('curricula_activity_tech_setup_types')
        db.delete_table('curricula_activity_secondary_content_types')

        # Deleting models
        db.delete_table('curricula_vocabulary')
        db.delete_table('curricula_questionanswer')
        db.delete_table('curricula_resourceitem')
        db.delete_table('curricula_activityrelation')
        db.delete_table('curricula_lesson')

        # Removing M2M tables
        db.delete_table('curricula_lesson_secondary_content_types')
        db.delete_table('curricula_lesson_materials')
        db.delete_table('curricula_lesson_secondary_categories')

        # Deleting models
        db.delete_table('curricula_lessonrelation')
        db.delete_table('curricula_lessonactivity')


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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
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
        'curricula.learnergroup': {
            'Meta': {'object_name': 'LearnerGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'})
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
        'edumetadata.grade': {
            'Meta': {'ordering': "('order', 'name')", 'object_name': 'Grade'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'default': '99'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
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
        }
    }

    complete_apps = ['curricula']
