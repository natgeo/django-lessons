from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags

from audience.models import AUDIENCE_FLAGS
from audience.settings import AUDIENCE_FIELDS
from audience.widgets import AdminBitFieldWidget, bitfield_display, VariationWidgetWrapper
from bitfield import BitField
from concepts.admin import ConceptItemInline
from concepts.models import ConceptItem
from contentrelations.admin import RelatedInline
from genericcollection import GenericCollectionInlineModelAdmin
from tinymce.widgets import TinyMCE

from .forms import ActivityForm, ActivityInlineFormset, LessonInlineFormset, LessonForm, IdeaCategoryForm, UnitForm
from .models import (Activity, ActivityRelation, GroupingType,
                     LearningObjective, Lesson, LessonActivity, LessonRelation,
                     Material, ObjectiveRelation, QuestionAnswer, ResourceItem,
                     Skill, Standard, TeachingApproach, TeachingMethodType,
                     Tip, Vocabulary, Idea, IdeaCategory, CategoryIdea,
                     IdeaCategoryRelation, Unit, UnitLesson, UnitRelation,
                     )
if settings.DEBUG:
    from .models import PluginType
from .settings import (RELATION_MODELS, JAVASCRIPT_URL, KEY_IMAGE,
                      CREDIT_MODEL, REPORTING_MODEL, ACTIVITY_FIELDS,
                      MCE_ATTRS, ACTIVITY_TINYMCE_FIELDS,
                      IDEACATEGORY_TINYMCE_FIELDS, LESSON_TINYMCE_FIELDS,
                      UNIT_TINYMCE_FIELDS)
from .utils import truncate
from .widgets import VocabularyIdWidget



class ResourceCarouselInline(RelatedInline):
    rel_name = 'resources'
    verbose_name_plural = "Resource Carousel"
    exclude = ('source_type', 'source_id', 'relation_type')


class TagInline(ConceptItemInline):
    extra = 10


class VocabularyInline(admin.TabularInline):
    extra = 10
    model = Vocabulary
    raw_id_fields = ('glossary_term',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(VocabularyInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'glossary_term':
            formfield.widget = VocabularyIdWidget(Vocabulary._meta.get_field('glossary_term').rel, self.admin_site)
        return formfield


class QuestionAnswerInline(admin.TabularInline):
    extra = 3
    formfield_overrides = {
        BitField: {
            'choices': AUDIENCE_FLAGS,
            'required': False,
            'widget': AdminBitFieldWidget()
        }
    }
    model = QuestionAnswer
    verbose_name_plural = 'Question Answers (S/F/K Quiz Yourself!)'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('question', 'answer'):
            return db_field.formfield(widget=TinyMCE(mce_attrs={'theme': "simple", 'width': 30, 'height': 5}))
        return super(QuestionAnswerInline, self).formfield_for_dbfield(db_field, **kwargs)


class ResourceInline(admin.TabularInline):
    model = ResourceItem
    raw_id_fields = ('resource',)

if RELATION_MODELS:
    from .forms import ActivityFormSet

    class InlineActivityRelation(GenericCollectionInlineModelAdmin):
        extra = 7
        model = ActivityRelation
        formset = ActivityFormSet
        template = 'admin/edit_inline/ic_coll_tabular.html'


class ContentAdmin(admin.ModelAdmin):
    date_hierarchy = 'published_date'
    tabs = {
        'Overview': 0,
        'Directions': 0,
        'Objectives': 0,
        'Background & Vocabulary': 0,
        'Credits, Sponsors, Partners': 0,
        'Global Metadata': 1,
        'Content Related Metadata': 1,
        'Time and Date Metadata': 1,
        'Publishing': 2,
    }

    formfield_overrides = {
        BitField: {
            'choices': AUDIENCE_FLAGS,
            'initial': 1,
            'widget': AdminBitFieldWidget()
        }
    }
    prepopulated_fields = {"slug": ("title",)}

    def get_title(self, obj):
        return strip_tags(obj.title)
    get_title.short_description = 'Title'

    def thumbnail_display(self, obj):
        return obj.thumbnail_html()
    thumbnail_display.allow_tags = True


class ActivityAdmin(ContentAdmin):
    filter_horizontal = ['eras', 'grades', 'grouping_types', 'materials',
                         'physical_space_types', 'prior_activities',
                         'subjects', 'teaching_method_types',
                         'tech_setup_types', 'tips', 'teaching_approaches',
                         'secondary_content_types', 'learner_groups',
                         'plugin_types']
    if REPORTING_MODEL:
        filter_horizontal += ['reporting_categories']
    filter_vertical = ['standards', 'skills']
    form = ActivityForm
    inlines = [ResourceCarouselInline, TagInline, VocabularyInline,
               ResourceInline, QuestionAnswerInline]
    if RELATION_MODELS:
        inlines.append(InlineActivityRelation)

    list_display = ('get_title', 'thumbnail_display', 'description', 'pedagogical_purpose_type', 'grade_levels', 'published_date')
    list_filter = ('pedagogical_purpose_type', 'published', 'published_date')
    object_name = 'activity'
    if CREDIT_MODEL is not None:
        raw_id_fields = ("credit", )

    search_fields = ['title', 'subtitle_guiding_question', 'description', 'id_number']
    varying_fields = AUDIENCE_FIELDS.get('curricula.Activity', [])

    class Media:
        css = {'all': (
            "css/glossary_term.css",
        )}

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ActivityAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ACTIVITY_TINYMCE_FIELDS:
            if db_field.name in MCE_ATTRS:
                formfield.widget = TinyMCE(mce_attrs=MCE_ATTRS[db_field.name])
            else:
                formfield.widget = TinyMCE(mce_attrs=MCE_ATTRS['default'])
        if db_field.name in self.varying_fields:
            request = kwargs.get('request', None)
            if request:
                obj_id = request.path.split('/')[-2]
                if not obj_id.isdigit():
                    obj_id = None
            else:
                obj_id = None
            formfield.widget = VariationWidgetWrapper(formfield.widget,
                self.admin_site, obj_id=obj_id, field=db_field.name,
                object_name=self.object_name)

        return formfield

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Overview',
                {'fields': [
                    'appropriate_for', 'title', 'slug',
                    'subtitle_guiding_question', 'pedagogical_purpose_type',
                    'description', 'duration', 'learner_groups', 'is_modular',
                    'ads_excluded', 'id_number', 'notes_on_readability_score'
                 ],
                 'classes': ['collapse']}),
            ('Directions',
                {'fields': [
                    'directions', 'assessment_type', 'assessment',
                    'extending_the_learning', 'tips'
                ],
                'classes': ['collapse']}),
            ('Objectives',
                {'fields': [
                    'learning_objs', 'teaching_approaches',
                    'teaching_method_types', 'skills', 'standards'
                ],
                'classes': ['collapse']}),
            ('Preparation',
                {'fields': [
                    'materials', 'tech_setup_types', 'internet_access_type',
                    'plugin_types', 'physical_space_types', 'setup',
                    'grouping_types', 'accessibility_notes', 'other_notes'
                 ],
                 'classes': ['collapse']}),
            ('Background & Vocabulary',
                {'fields': [
                    'background_information', 'prior_knowledge',
                    'prior_activities'
                ],
                'classes': ['collapse']}),
        ]
        if CREDIT_MODEL is not None:
            fieldsets.append(('Credits, Sponsors, Partners', {'fields': ['credit'], 'classes': ['collapse']}))
        if REPORTING_MODEL is None:
            fieldsets.append(('Global Metadata', {'fields': ['secondary_content_types'], 'classes': ['collapse']}))
        else:
            fieldsets.append(('Global Metadata', {'fields': ['secondary_content_types', 'reporting_categories'], 'classes': ['collapse']}))
        fieldsets += [
            ('Content Related Metadata', {'fields': ['subjects', 'grades'], 'classes': ['collapse']}),
            ('Time and Date Metadata', {'fields': ['eras', 'geologic_time', 'relevant_start_date', 'relevant_end_date'], 'classes': ['collapse']}),
            ('Publishing', {'fields': ['published', 'published_date'], 'classes': ['collapse']}),
        ]
        for field in ACTIVITY_FIELDS:
            fieldsets[0][1]['fields'].insert(5, field[0])
        return fieldsets

    def grade_levels(self, obj):
        return obj.grades.all().as_grade_range()

    def save_model(self, request, obj, form, change, *args, **kwargs):
        super(ActivityAdmin, self).save_model(request, obj, form, change, *args, **kwargs)

        for field, model in ACTIVITY_FIELDS:
            if form[field].data == None or form[field].data == '':
                # user cleared the field
                items = obj.relations.filter(relation_type=field)
                if len(items) > 0:
                    items[0].delete()
            else:
                try:
                    item = obj.relations.get(relation_type=field)
                    item.object_id = form[field].data
                    item.save()
                except ActivityRelation.DoesNotExist:
                    app_label, model = model.split('.')
                    ctype = ContentType.objects.get(app_label=app_label, model=model)
                    item = obj.relations.create(relation_type=field, object_id=form[field].data, content_type_id=ctype.id)

        learning_objectives = form.cleaned_data['learning_objs']
        ctype = ContentType.objects.get_for_model(Activity)
        # clear existing
        objectiverelations = ObjectiveRelation.objects.filter(
                                content_type=ctype, object_id=obj.id)

        for objectiverelation in objectiverelations:
            try:
                objectiverelation.objective.delete()
            except LearningObjective.DoesNotExist:
                pass
            objectiverelation.delete()

        # create new
        for learning_objective in learning_objectives.split('\r\n'):
            if learning_objective and len(learning_objective) > 0:
                lo, created = LearningObjective.objects.get_or_create(text=learning_objective)

                o_rel = ObjectiveRelation(objective=lo, content_type=ctype,
                                          object_id=obj.id)
                o_rel.save()


class ActivityInline(admin.TabularInline):
    formset = ActivityInlineFormset
    model = LessonActivity
    raw_id_fields = ('activity',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'transition_text':
            return db_field.formfield(widget=TinyMCE(mce_attrs={'theme': "simple", 'height': 5}))
        return super(ActivityInline, self).formfield_for_dbfield(db_field, **kwargs)


if RELATION_MODELS:
    class InlineIdeaCategoryRelation(GenericCollectionInlineModelAdmin):
        extra = 7
        model = IdeaCategoryRelation
        template = 'admin/edit_inline/ic_coll_tabular.html'


class IdeaCategoryInline(admin.TabularInline):
    model = CategoryIdea
    raw_id_fields = ('category', )
    verbose_name = "Idea Category"
    verbose_name_plural = "Idea Categories"


class LessonInline(admin.TabularInline):
    formset = LessonInlineFormset
    model = UnitLesson
    raw_id_fields = ('lesson', )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'transition_text':
            return db_field.formfield(widget=TinyMCE(mce_attrs={'theme': "simple", 'height': 5}))
        return super(LessonInline, self).formfield_for_dbfield(db_field, **kwargs)


class IdeaAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
    formfield_overrides = {
        BitField: {
            'choices': AUDIENCE_FLAGS,
            'initial': 1,
            'widget': AdminBitFieldWidget()
        }
    }
    inlines = [TagInline, IdeaCategoryInline]
    list_display = ('title', 'thumbnail_display', 'categories_display', 'appropriate_display')
    if KEY_IMAGE:
        raw_id_fields = ("key_image", )
    search_fields = ['title', 'content_body']

    class Media:
        css = {'all': (settings.STATIC_URL + 'audience/bitfield.css', )}
        js = ('/media/static/audience/bitfield.js',
              JAVASCRIPT_URL + 'jquery-1.7.1.min.js',
              JAVASCRIPT_URL + 'genericcollections.js',
              JAVASCRIPT_URL + 'admin.js',
              JAVASCRIPT_URL + 'reference_tinymce_widget.js',
              settings.STATIC_URL + 'js_scss/libs/jquery.ui.core.min.js',
        )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(IdeaAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'content_body':
            formfield.widget = TinyMCE(mce_attrs=MCE_ATTRS['default'])

        return formfield

    def appropriate_display(self, obj):
        return bitfield_display(obj.appropriate_for)
    appropriate_display.short_description = 'Appropriate For'
    appropriate_display.allow_tags = True

    def categories_display(self, obj):
        return (',').join(obj.get_categories())

    def thumbnail_display(self, obj):
        return obj.thumbnail_html()
    thumbnail_display.allow_tags = True


class IdeaInline(admin.TabularInline):
    model = CategoryIdea
    raw_id_fields = ('idea', )
    verbose_name = "Idea"
    verbose_name_plural = "Ideas"


class IdeaCategoryAdmin(ContentAdmin):
    filter_horizontal = ['eras', 'grades', 'secondary_content_types', 'subjects', ]
    if REPORTING_MODEL:
        filter_horizontal += ['reporting_categories']
    form = IdeaCategoryForm
    list_display = ('title', 'content_body', 'thumbnail_display', 'appropriate_display', 'grade_levels', 'published_date')
    list_filter = ('grades', 'published', 'published_date')
    inlines = [TagInline, IdeaInline]
    if RELATION_MODELS:
        inlines.append(InlineIdeaCategoryRelation)
    raw_id_fields = ("geologic_time", "license_name")
    if CREDIT_MODEL:
        raw_id_fields += ("credit", )
    if KEY_IMAGE:
        raw_id_fields += ("key_image", )
    search_fields = ['title', 'content_body']

    class Media:
        css = {'all': (settings.STATIC_URL + 'audience/bitfield.css', )}
        js = ('/media/static/audience/bitfield.js',
              JAVASCRIPT_URL + 'jquery-1.7.1.min.js',
              JAVASCRIPT_URL + 'genericcollections.js',
              JAVASCRIPT_URL + 'admin.js',
              JAVASCRIPT_URL + 'reference_tinymce_widget.js',
              settings.STATIC_URL + 'js_scss/libs/jquery.ui.core.min.js',
        )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(IdeaCategoryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in IDEACATEGORY_TINYMCE_FIELDS:
            formfield.widget = TinyMCE(mce_attrs=MCE_ATTRS['default'])

        return formfield

    def appropriate_display(self, obj):
        return bitfield_display(obj.appropriate_for)
    appropriate_display.short_description = 'Appropriate For'
    appropriate_display.allow_tags = True

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Overview', {'fields': ['appropriate_for', 'title', 'slug', 'description', 'id_number'], 'classes': ['collapse']}),
            ('Content Detail', {'fields': ['content_body', ], 'classes': ['collapse']}),
        ]
        if CREDIT_MODEL is not None:
            fieldsets.append(('Credits, Sponsors, Partners', {'fields': ['credit', ], 'classes': ['collapse']}))
        fieldsets.append(('Licensing', {'fields': ['license_name', ], 'classes': ['collapse']}))
        if REPORTING_MODEL is None:
            fieldsets.append(('Global Metadata', {'fields': ['secondary_content_types'], 'classes': ['collapse']}))
        else:
            fieldsets.append(('Global Metadata', {'fields': ['secondary_content_types', 'reporting_categories'], 'classes': ['collapse']}))
        fieldsets += [
            ('Content Related Metadata', {'fields': ['subjects', 'grades'], 'classes': ['collapse']}),
            ('Time and Date Metadata', {'fields': ['eras', 'geologic_time', 'relevant_start_date', 'relevant_end_date'], 'classes': ['collapse']}),
            ('Publishing', {'fields': ['published', 'published_date'], 'classes': ['collapse']}),
        ]
        fieldsets[0][1]['fields'].insert(4, KEY_IMAGE[0])
        return fieldsets

    def grade_levels(self, obj):
        return obj.grades.all().as_grade_range()


if RELATION_MODELS:
    class InlineLessonRelation(GenericCollectionInlineModelAdmin):
        extra = 7
        model = LessonRelation
        template = 'admin/edit_inline/ic_coll_tabular.html'


class LessonAdmin(ContentAdmin):
    filter_horizontal = ['materials', 'secondary_content_types', 'prior_lessons']
    readonly_fields = ['accessibility_notes', 'eras', 'prior_knowledge',
        'relevant_start_date', 'relevant_end_date', 'geologic_time', 'subjects',
        'grades', 'duration', 'physical_space_types', 'plugin_types',
        'tech_setup_types']
    if REPORTING_MODEL:
        filter_horizontal += ['reporting_categories']
    readonly_fields += ['reporting_categories',]

    form = LessonForm
    if RELATION_MODELS:
        inlines = [ResourceCarouselInline, ActivityInline, TagInline, InlineLessonRelation, ]
    else:
        inlines = [ResourceCarouselInline, ActivityInline, ]
    list_display = ('get_title', 'thumbnail_display', 'get_description', 'appropriate_display', 'published_date')
    list_filter = ('published_date', 'published')
    object_name = 'lesson'
    if CREDIT_MODEL is not None:
        raw_id_fields = ("credit",)
    search_fields = ['title', 'description', 'id_number']
    varying_fields = AUDIENCE_FIELDS.get('curricula.Lesson', [])

    class Media:
        css = {'all': (
            "css/glossary_term.css",
            settings.STATIC_URL + 'audience/bitfield.css'
        )}

    def appropriate_display(self, obj):
        return bitfield_display(obj.appropriate_for)
    appropriate_display.short_description = 'Appropriate For'
    appropriate_display.allow_tags = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(LessonAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in LESSON_TINYMCE_FIELDS:
            formfield.widget = TinyMCE(mce_attrs=MCE_ATTRS['default'])
        if db_field.name in self.varying_fields:
            request = kwargs.get('request', None)
            if request:
                obj_id = request.path.split('/')[-2]
                if not obj_id.isdigit():
                    obj_id = None
            else:
                obj_id = None
            formfield.widget = VariationWidgetWrapper(formfield.widget,
                self.admin_site, obj_id=obj_id, field=db_field.name,
                object_name=self.object_name)

        return formfield

    def get_description(self, obj):
        return truncate(strip_tags(obj.description), 180)
    get_description.short_description = 'Description'

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Overview', {'fields': ['appropriate_for', 'title', 'slug', 'subtitle_guiding_question', 'description', 'is_modular', 'ads_excluded', 'id_number'], 'classes': ['collapse']}), # , 'create_date', 'last_updated_date'], 'classes': ['collapse']}),
            ('Directions', {'fields': ['assessment_type', 'assessment'], 'classes': ['collapse']}),
            ('Objectives', {'fields': ['learning_objs'], 'classes': ['collapse']}),
            ('Preparation', {'fields': ['materials', 'other_notes'], 'classes': ['collapse']}),
            ('Background & Vocabulary', {'fields': ['background_information', 'prior_knowledge', 'prior_lessons'], 'classes': ['collapse']}),
        ]
        if CREDIT_MODEL is not None:
            fieldsets.append(('Credits, Sponsors, Partners', {'fields': ['credit'], 'classes': ['collapse']}))
        if REPORTING_MODEL is None:
            fieldsets.append(('Global Metadata', {'fields': ['secondary_content_types'], 'classes': ['collapse']}))
        else:
            fieldsets.append(('Global Metadata', {'fields': ['secondary_content_types', 'reporting_categories'], 'classes': ['collapse']}))
        fieldsets += [
            ('Time and Date Metadata', {'fields': ['eras', 'geologic_time', 'relevant_start_date', 'relevant_end_date'], 'classes': ['collapse']}),
            ('Publishing', {'fields': ['published', 'published_date'], 'classes': ['collapse']}),
        ]
        fieldsets[0][1]['fields'].insert(4, KEY_IMAGE[0])
        return fieldsets

    def save_model(self, request, obj, form, change, *args, **kwargs):
        super(LessonAdmin, self).save_model(request, obj, form, change, *args, **kwargs)

        field, model = KEY_IMAGE
        if form[field].data != None and form[field].data != '':
            try:
                item = obj.lessonrelation_set.get(relation_type=field)
                item.object_id = form[field].data
                item.save()
            except LessonRelation.DoesNotExist:
                app_label, model = model.split('.')
                ctype = ContentType.objects.get(app_label=app_label, model=model)
                item = obj.lessonrelation_set.create(relation_type=field, object_id=form[field].data, content_type_id=ctype.id)

        learning_objectives = form.cleaned_data['learning_objs']
        ctype = ContentType.objects.get_for_model(Lesson)
        # clear existing
        objectiverelations = ObjectiveRelation.objects.filter(
                                content_type=ctype, object_id=obj.id)

        for objectiverelation in objectiverelations:
            objectiverelation.objective.delete()
            objectiverelation.delete()

        # create new
        for learning_objective in learning_objectives.split('\r\n'):
            if learning_objective and len(learning_objective) > 0:
                lo, created = LearningObjective.objects.get_or_create(text=learning_objective)

                o_rel = ObjectiveRelation(objective=lo, content_type=ctype,
                                          object_id=obj.id)
                o_rel.save()

    def update_ARs(self, obj, rcs):
        unique_indices = []
        # clear existing, first
        rcs.body.delete_ARs()

        for lessonvariation in obj.variations.filter(field='description'):
            audience_indices = lessonvariation.audience.get_set_bits()
            unique_indices = list(set(unique_indices + audience_indices))
            # reading level/ text difficulty 6 = Not Applicable
            rcs.body.create_ARs(
                '%s-[6]' % audience_indices,
                lessonvariation.variation)
        # default
        audience_indices = obj.appropriate_for.get_set_bits()
        indices = [i for i in audience_indices if i not in unique_indices]
        if indices:
            rcs.body.create_ARs('%s-[6]' % indices, obj.description)
        rcs.body.save()


class TypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


class StandardAdmin(admin.ModelAdmin):
    filter_horizontal = ['grades']
    list_display = ('standard_type', 'name', 'definition', 'grade_levels')
    list_filter = ('standard_type', 'state', 'grades')
    search_fields = ['name', 'definition']

    def grade_levels(self, obj):
        return obj.grades.all().as_grade_range()
    grade_levels.short_description = 'Grades'


class TipAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {
            'choices': AUDIENCE_FLAGS,
            'widget': AdminBitFieldWidget()
        }
    }
    list_display = ('body_display', 'tip_type', 'appropriate_display')
    list_filter = ('tip_type',)
    object_name = 'tip'
    search_fields = ['body', 'id_number']
    varying_fields = ('body',)

    class Media:
        css = {'all': ('/media/static/audience/bitfield.css',)}
        js = ('/media/static/audience/bitfield.js',
              JAVASCRIPT_URL + 'jquery-1.7.1.min.js')

    def appropriate_display(self, obj):
        return bitfield_display(obj.appropriate_for)
    appropriate_display.short_description = 'Appropriate For'
    appropriate_display.allow_tags = True

    def body_display(self, obj):
        return truncate(strip_tags(obj.body), 90)
    body_display.short_description = 'Body'

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(TipAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'body':
            formfield.widget = TinyMCE()
        if db_field.name in self.varying_fields:
            request = kwargs.get('request', None)
            if request:
                obj_id = request.path.split('/')[-2]
                if not obj_id.isdigit():
                    obj_id = None
            else:
                obj_id = None
            formfield.widget = VariationWidgetWrapper(formfield.widget,
                self.admin_site, obj_id=obj_id, field=db_field.name,
                object_name=self.object_name)

        return formfield


if RELATION_MODELS:
    class InlineUnitRelation(GenericCollectionInlineModelAdmin):
        extra = 7
        model = UnitRelation
        template = 'admin/edit_inline/ic_coll_tabular.html'


class UnitAdmin(admin.ModelAdmin):
    date_hierarchy = 'published_date'
    filter_horizontal = ['eras', 'grades', 'subjects']
    form = UnitForm
    formfield_overrides = {
        BitField: {
            'choices': AUDIENCE_FLAGS,
            'initial': 1,
            'widget': AdminBitFieldWidget()
        }
    }
    inlines = [LessonInline, TagInline]
    if RELATION_MODELS:
        inlines += [InlineUnitRelation, ]
    list_display = ('title', 'thumbnail_display', 'overview_display', 'appropriate_display', 'published_date')
    list_filter = ('published_date', 'published')
    prepopulated_fields = {"slug": ("title",)}
    if KEY_IMAGE:
        raw_id_fields = ("key_image", )
    if CREDIT_MODEL is not None:
        raw_id_fields += ("credit", )
    tabs = {
        'Overview': 0,
        'Credits, Sponsors, Partners': 0,
        'Content Related Metadata': 1,
        'Time and Date Metadata': 1,
        'Publishing': 2,
    }
    varying_fields = AUDIENCE_FIELDS.get('curricula.Unit', [])

    class Media:
        css = {
            'all': (settings.STATIC_URL + 'audience/bitfield.css',),
        }

    def appropriate_display(self, obj):
        return bitfield_display(obj.appropriate_for)
    appropriate_display.short_description = 'Appropriate For'
    appropriate_display.allow_tags = True

    def overview_display(self, obj):
        return strip_tags(obj.overview)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(UnitAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in UNIT_TINYMCE_FIELDS:
            formfield.widget = TinyMCE(mce_attrs=MCE_ATTRS['default'])
        if db_field.name in self.varying_fields:
            request = kwargs.get('request', None)
            if request:
                obj_id = request.path.split('/')[-2]
                if not obj_id.isdigit():
                    obj_id = None
            else:
                obj_id = None
            formfield.widget = VariationWidgetWrapper(formfield.widget,
                self.admin_site, obj_id=obj_id, field=db_field.name,
                object_name=self.object_name)

        return formfield

    def get_fieldsets(self, request, obj=None):
        fieldsets = []
        if KEY_IMAGE:
            fieldsets.append(
                ('Overview', {'fields': ['appropriate_for', 'title', 'slug', 'subtitle', 'key_image', 'description', 'overview', 'id_number'], 'classes': ['collapse']}),
            )
        else:
            fieldsets.append(
                ('Overview', {'fields': ['appropriate_for', 'title', 'slug', 'subtitle', 'description', 'overview', 'id_number'], 'classes': ['collapse']}),
            )

        if CREDIT_MODEL is not None:
            fieldsets.append(('Credits, Sponsors, Partners', {'fields': ['credit'], 'classes': ['collapse']}))
        fieldsets += [
            ('Content Related Metadata', {'fields': ['subjects', 'grades'], 'classes': ['collapse']}),
            ('Time and Date Metadata', {'fields': ['eras', 'geologic_time', 'relevant_start_date', 'relevant_end_date'], 'classes': ['collapse']}),
            ('Publishing', {'fields': ['published', 'published_date'], 'classes': ['collapse']}),
        ]
        return fieldsets

    def thumbnail_display(self, obj):
        return '<img src="%s"/>' % obj.key_image.thumbnail_url()
    thumbnail_display.allow_tags = True

admin.site.register(Activity, ActivityAdmin)
admin.site.register(GroupingType)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaCategory, IdeaCategoryAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Material, TypeAdmin)
if settings.DEBUG:
    admin.site.register(LearningObjective)
    admin.site.register(PluginType)
    admin.site.register(QuestionAnswer)
    admin.site.register(Skill)
    admin.site.register(TeachingApproach)
admin.site.register(Standard, StandardAdmin)
admin.site.register(TeachingMethodType, TypeAdmin)
admin.site.register(Tip, TipAdmin)
admin.site.register(Unit, UnitAdmin)
