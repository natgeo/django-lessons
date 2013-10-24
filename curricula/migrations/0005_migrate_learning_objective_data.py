# encoding: utf-8
from django.contrib.contenttypes.models import ContentType

from south.v2 import SchemaMigration

from curricula.models import Activity, LearningObjective, ObjectiveRelation
from curricula.utils import ul_as_list

class Migration(SchemaMigration):

    def forwards(self, orm):
        ctype = ContentType.objects.get_for_model(Activity)
        for activity in Activity.objects.all():
            if activity.learning_objectives:
                for li in ul_as_list(activity.learning_objectives):
                    lo, created = LearningObjective.objects.get_or_create(text=li)
                    ObjectiveRelation.objects.get_or_create(
                        objective=lo, object_id=activity.id, content_type=ctype)

    def backwards(self, orm):
        pass

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
            'prior_activities': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['curricula.Activity']", 'null': 'True', 'blank': 'True'}),
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
