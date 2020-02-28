from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.utils.html import strip_tags
from django.utils.html import escape, conditional_escape

from audience.settings import AUDIENCE_FIELDS
from audience.widgets import AdminBitFieldWidget, bitfield_display, VariationWidgetWrapper
from bitfield import BitField
from concepts.admin import ConceptItemInline
from resource_carousel.admin import RCRelatedInline
from contentrelations.genericcollection import GenericCollectionInlineModelAdmin
from tinymce.widgets import TinyMCE
from ckeditor.widgets import CKEditorWidget
from .settings import (RELATION_MODELS,
                       MCE_ATTRS, ACTIVITY_TINYMCE_FIELDS,
                       IDEACATEGORY_TINYMCE_FIELDS, LESSON_TINYMCE_FIELDS,
                       UNIT_TINYMCE_FIELDS, THUMBNAIL_SIZE
)
from .utils import truncate
from .widgets import VocabularyIdWidget, DynalistWidget
from taxonomy.admin import autotag_action
from .models import (Activity, ActivityRelation, GroupingType,
                     LearningObjective, Lesson, LessonActivity, LessonRelation,
                     Material, ObjectiveRelation, QuestionAnswer, ResourceItem,
                     Skill, Standard, TeachingApproach, TeachingMethodType,
                     Tip, Vocabulary, Idea, IdeaCategory, CategoryIdea,
                     IdeaCategoryRelation, Unit, UnitLesson, UnitRelation,
                     )
from .forms import ActivityForm, ActivityInlineFormset, LessonInlineFormset, LessonForm, IdeaCategoryForm, UnitForm

if settings.DEBUG:
    from .models import PluginType


def thumbnail_display(obj):
    if obj.key_image is None:
        return ''
    w, h = THUMBNAIL_SIZE.split('x')
    bits = [
        '<img src="',
        obj.key_image._get_SIZE_url(THUMBNAIL_SIZE),
        '" alt="',
        obj.title,
        '" width="%s" height="%s" />' % (w, h)]
    return "".join(bits)
thumbnail_display.allow_tags = True
thumbnail_display.short_description = 'Thumbnail'


class ResourceCarouselInline(RCRelatedInline):
    rel_name = 'resources'
    ct_field = "object_type"
    ct_fk_field = "object_id"

    verbose_name_plural = "Resource Carousel"
    exclude = ('source_type', 'source_id', 'relation_type')


class TagInline(ConceptItemInline):
    pass


class VocabularyInline(admin.TabularInline):
    model = Vocabulary
    raw_id_fields = ('glossary_term',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(VocabularyInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'glossary_term':
            formfield.widget = VocabularyIdWidget(Vocabulary._meta.get_field('glossary_term').rel, self.admin_site)
        return formfield


class QuestionAnswerInline(admin.StackedInline):
    extra = 1
    formfield_overrides = {
        BitField: {
            # 'choices': AUDIENCE_FLAGS,
            'required': False,
            'widget': AdminBitFieldWidget()
        }
    }
    model = QuestionAnswer
    verbose_name_plural = 'Question Answers (S/F/K Quiz Yourself!)'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('question', 'answer'):
            return db_field.formfield(widget=CKEditorWidget(config_name='simple_3line_micro'))
        return super(QuestionAnswerInline, self).formfield_for_dbfield(db_field, **kwargs)


class ResourceInline(admin.TabularInline):
    model = ResourceItem
    raw_id_fields = ('resource',)

if RELATION_MODELS:
    from .forms import ActivityFormSet

    class InlineActivityRelation(GenericCollectionInlineModelAdmin):
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
        'Taxonomy': 0,
        'Global Metadata': 1,
        'Content Related Metadata': 1,
        'Time and Date Metadata': 1,
        'Publishing': 2,
    }

    formfield_overrides = {
        BitField: {
            # 'choices': AUDIENCE_FLAGS,
            'initial': 1,
            'widget': AdminBitFieldWidget()
        }
    }
    prepopulated_fields = {"slug": ("title",)}

    def get_title(self, obj):
        return strip_tags(obj.title)
    get_title.short_description = 'Title'


class StandardsWidget(admin.widgets.FilteredSelectMultiple):
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = ' selected="selected"'
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        standard = Standard.objects.get(pk=option_value)
        title = "%s: %s: %s" % (standard.get_standard_type_display(),
                                 standard.name,
                                 strip_tags(standard.definition))

        return '<option value="%s" title="%s"%s>%s</option>' % (
            escape(option_value), title, selected_html,
            conditional_escape(force_text(option_label)))


class SkillAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {
            # 'choices': AUDIENCE_FLAGS,
            'initial': 1,
            'widget': AdminBitFieldWidget()
        }
    }


class ActivityAdmin(ContentAdmin):
    filter_horizontal = ['eras', 'grades', 'grouping_types', 'materials',
                         'physical_space_types', 'prior_activities',
                         'subjects', 'teaching_method_types',
                         'tech_setup_types', 'tips', 'teaching_approaches',
                         'secondary_content_types', 'learner_groups',
                         'plugin_types']
    filter_vertical = ['standards', 'skills']
    form = ActivityForm
    actions = [autotag_action]
    inlines = [ResourceCarouselInline, TagInline, VocabularyInline,
               ResourceInline, QuestionAnswerInline]
    if RELATION_MODELS:
        inlines.append(InlineActivityRelation)

    list_display = ('get_title', thumbnail_display, 'description',
        'pedagogical_purpose_type', 'grade_levels', 'published_date')
    list_filter = ('pedagogical_purpose_type', 'published', 'published_date', 'archived')
    object_name = 'activity'
    raw_id_fields = ("credit", "key_image", )

    search_fields = ['title', 'subtitle_guiding_question', 'description', 'id_number']
    varying_fields = AUDIENCE_FIELDS.get('curricula.Activity', [])

    class Media:
        css = {'all': (
            "css/glossary_term.css",
        )}

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ActivityAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ACTIVITY_TINYMCE_FIELDS:
            if db_field.name in ('directions', ):
                formfield.widget = TinyMCE(mce_attrs=MCE_ATTRS[db_field.name])
            else:
                formfield.widget = CKEditorWidget(config_name='simple_paragraph')
        elif db_field.name == 'prior_knowledge':
            formfield.widget = DynalistWidget()
        if db_field.name in self.varying_fields:
            request = kwargs.get('request', None)
            if request:
                obj_id = request.path.split('/')[-2]
                if not obj_id.isdigit():
                    obj_id = None
            else:
                obj_id = None
            formfield.widget = VariationWidgetWrapper(
                formfield.widget,
                self.admin_site, obj_id=obj_id, field=db_field.name,
                object_name=self.object_name)

        return formfield

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        formfield = super(ActivityAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

        if db_field.name.lower() == 'standards':
            formfield.widget = StandardsWidget(db_field.verbose_name, True)

        return formfield

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Overview', {
                'fields': [
                    'appropriate_for', 'title', 'slug',
                    'subtitle_guiding_question', 'pedagogical_purpose_type',
                    'key_image', 'description', 'duration', 'learner_groups',
                    'is_modular', 'id_number', 'notes_on_readability_score'
                ],
                'classes': ['collapse']
            }),
            ('Directions', {
                'fields': [
                    'directions', 'assessment_type', 'assessment',
                    'extending_the_learning', 'tips'
                ],
                'classes': ['collapse']
            }),
            ('Objectives', {
                'fields': [
                    'learning_objs', 'teaching_approaches',
                    'teaching_method_types', 'skills', 'standards'
                ],
                'classes': ['collapse']
            }),
            ('Preparation', {
                'fields': [
                    'materials', 'tech_setup_types', 'internet_access_type',
                    'plugin_types', 'physical_space_types', 'setup',
                    'grouping_types', 'accessibility_notes', 'other_notes'
                ],
                'classes': ['collapse']
            }),
            ('Background & Vocabulary', {
                'fields': [
                    'background_information', 'prior_knowledge',
                    'prior_activities'
                ],
                'classes': ['collapse']
            }),
            ('Credits, Sponsors, Partners', {
                'fields': ['credit'],
                'classes': ['collapse']}),
            ('Global Metadata', {
                'fields': ['secondary_content_types'],
                'classes': ['collapse']}),
            ('Content Related Metadata', {
                'fields': ['subjects', 'grades'],
                'classes': ['collapse']}),
            ('Time and Date Metadata', {
                'fields': ['eras', 'geologic_time', 'relevant_start_date', 'relevant_end_date'],
                'classes': ['collapse']}),
            ('Publishing', {
                'fields': ['published', 'published_date', 'archived'],
                'classes': ['collapse']}),
            ('Taxonomy', {
                'fields': ['taxonomy'],
            }),
        ]
        return fieldsets

    def grade_levels(self, obj):
        return obj.grades.all().as_grade_range()

    def save_model(self, request, obj, form, change, *args, **kwargs):
        super(ActivityAdmin, self).save_model(request, obj, form, change, *args, **kwargs)
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
            return db_field.formfield(widget=CKEditorWidget(config_name='simple_3line_micro'))
        return super(ActivityInline, self).formfield_for_dbfield(db_field, **kwargs)


if RELATION_MODELS:
    class InlineIdeaCategoryRelation(GenericCollectionInlineModelAdmin):
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
            return db_field.formfield(widget=CKEditorWidget(config_name='simple_3line_micro'))
        return super(LessonInline, self).formfield_for_dbfield(db_field, **kwargs)


class IdeaAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
    formfield_overrides = {
        BitField: {
            # 'choices': AUDIENCE_FLAGS,
            'initial': 1,
            'widget': AdminBitFieldWidget()
        }
    }
    fieldsets = [
        (None, {
            'fields': ['appropriate_for', ]
        }),
        ('Content', {
            'fields': ['title', 'id_number', 'content_body', 'key_image', 'source']
        }),
    ]
    inlines = [TagInline, IdeaCategoryInline]
    list_display = ('title', thumbnail_display, 'categories_display', 'appropriate_display')
    raw_id_fields = ("key_image", 'source', )
    search_fields = ['title', 'content_body']
    varying_fields = AUDIENCE_FIELDS.get('curricula.Idea', [])
    object_name = 'idea'

    class Media:
        css = {'all': ('audience/bitfield.css', )}
        js = ('js/genericcollections.js', )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(IdeaAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'content_body':
            formfield.widget = CKEditorWidget('simple_paragraph')
        if db_field.name in self.varying_fields:
            request = kwargs.get('request', None)
            if request:
                obj_id = request.path.split('/')[-2]
                if not obj_id.isdigit():
                    obj_id = None
            else:
                obj_id = None
            formfield.widget = VariationWidgetWrapper(
                formfield.widget,
                self.admin_site, obj_id=obj_id, field=db_field.name,
                object_name=self.object_name)

        return formfield

    def appropriate_display(self, obj):
        return bitfield_display(obj.appropriate_for)
    appropriate_display.short_description = 'Appropriate For'
    appropriate_display.allow_tags = True

    def categories_display(self, obj):
        return (',').join(obj.get_categories())


class IdeaInline(admin.TabularInline):
    model = CategoryIdea
    raw_id_fields = ('idea', )
    verbose_name = "Idea"
    verbose_name_plural = "Ideas"


class IdeaCategoryAdmin(ContentAdmin):
    filter_horizontal = ['eras', 'grades', 'secondary_content_types', 'subjects', ]
    form = IdeaCategoryForm
    list_display = ('title', 'content_body', thumbnail_display, 'appropriate_display', 'grade_levels', 'published_date')
    list_filter = ('grades', 'published', 'published_date', 'archived')
    inlines = [TagInline, IdeaInline]
    if RELATION_MODELS:
        inlines.append(InlineIdeaCategoryRelation)
    raw_id_fields = ("geologic_time", "license_name", "credit", "key_image", )
    search_fields = ['title', 'content_body']
    object_name = 'ideacategory'
    varying_fields = AUDIENCE_FIELDS.get('curricula.IdeaCategory', [])

    class Media:
        css = {'all': (settings.STATIC_URL + 'audience/bitfield.css', )}
        js = ('js/genericcollections.js', )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(IdeaCategoryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in IDEACATEGORY_TINYMCE_FIELDS:
            formfield.widget = CKEditorWidget(config_name='simple_paragraph')
        if db_field.name in self.varying_fields:
            request = kwargs.get('request', None)
            if request:
                obj_id = request.path.split('/')[-2]
                if not obj_id.isdigit():
                    obj_id = None
            else:
                obj_id = None
            formfield.widget = VariationWidgetWrapper(
                formfield.widget,
                self.admin_site, obj_id=obj_id, field=db_field.name,
                object_name=self.object_name)

        return formfield

    def appropriate_display(self, obj):
        return bitfield_display(obj.appropriate_for)
    appropriate_display.short_description = 'Appropriate For'
    appropriate_display.allow_tags = True

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Overview', {'fields': ['appropriate_for', 'title', 'slug', 'description', 'key_image', 'id_number'], 'classes': ['collapse']}),
            ('Content Detail', {'fields': ['content_body', ], 'classes': ['collapse']}),
        ]
        fieldsets.append(('Credits, Sponsors, Partners', {'fields': ['credit', ], 'classes': ['collapse']}))
        fieldsets.append(('Licensing', {'fields': ['license_name', ], 'classes': ['collapse']}))
        fieldsets.append(('Global Metadata', {'fields': ['secondary_content_types'], 'classes': ['collapse']}))
        fieldsets += [
            ('Content Related Metadata', {'fields': ['subjects', 'grades'], 'classes': ['collapse']}),
            ('Time and Date Metadata', {'fields': ['eras', 'geologic_time', 'relevant_start_date', 'relevant_end_date'], 'classes': ['collapse']}),
            ('Publishing', {'fields': ['published', 'published_date', 'archived'], 'classes': ['collapse']}),
        ]
        return fieldsets

    def grade_levels(self, obj):
        return obj.grades.all().as_grade_range()


if RELATION_MODELS:
    class InlineLessonRelation(GenericCollectionInlineModelAdmin):
        model = LessonRelation
        template = 'admin/edit_inline/ic_coll_tabular.html'


class LessonAdmin(ContentAdmin):
    filter_horizontal = ['materials', 'secondary_content_types', 'prior_lessons']
    readonly_fields = [
        'accessibility_notes', 'eras', 'prior_knowledge',
        'relevant_start_date', 'relevant_end_date', 'geologic_time', 'subjects',
        'grades', 'duration', 'physical_space_types', 'plugin_types',
        'tech_setup_types'
    ]

    form = LessonForm
    if RELATION_MODELS:
        inlines = [ResourceCarouselInline, ActivityInline, TagInline, InlineLessonRelation, ]
    else:
        inlines = [ResourceCarouselInline, ActivityInline, ]
    list_display = ('get_title', thumbnail_display, 'get_description', 'appropriate_display', 'published_date')
    list_filter = ('published_date', 'published', 'archived')
    object_name = 'lesson'
    raw_id_fields = ("credit", "key_image", )
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
            formfield.widget = CKEditorWidget(config_name='simple_paragraph')
        if db_field.name in self.varying_fields:
            request = kwargs.get('request', None)
            if request:
                obj_id = request.path.split('/')[-2]
                if not obj_id.isdigit():
                    obj_id = None
            else:
                obj_id = None
            formfield.widget = VariationWidgetWrapper(
                formfield.widget,
                self.admin_site, obj_id=obj_id, field=db_field.name,
                object_name=self.object_name)

        return formfield

    def get_description(self, obj):
        return truncate(strip_tags(obj.description), 180)
    get_description.short_description = 'Description'

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Overview', {
                'fields': [
                    'appropriate_for', 'title', 'slug', 'subtitle_guiding_question',
                    'key_image', 'description', 'is_modular', 'id_number', 'instructional_pathways',
                ],
                'classes': ['collapse']}),
            ('Directions', {
                'fields': [
                    'assessment_type', 'assessment'
                ],
                'classes': ['collapse']}),
            ('Objectives', {
                'fields': ['learning_objs'],
                'classes': ['collapse']}),
            ('Preparation', {
                'fields': ['materials', 'other_notes'],
                'classes': ['collapse']}),
            ('Background & Vocabulary', {
                'fields': [
                    'background_information', 'prior_knowledge', 'prior_lessons'
                ],
                'classes': ['collapse']}),
            ('Credits, Sponsors, Partners', {
                'fields': ['credit'],
                'classes': ['collapse']}),
            ('Global Metadata', {
                'fields': ['secondary_content_types'],
                'classes': ['collapse']}),
            ('Content Related Metadata', {
                'fields': ['subjects', 'grades'],
                'classes': ['collapse']}),
            ('Time and Date Metadata', {
                'fields': [
                    'eras', 'geologic_time', 'relevant_start_date', 'relevant_end_date'
                ], 'classes': ['collapse']}),
            ('Publishing', {
                'fields': ['published', 'published_date', 'archived'],
                'classes': ['collapse']}),
        ]
        return fieldsets

    def save_model(self, request, obj, form, change, *args, **kwargs):
        super(LessonAdmin, self).save_model(request, obj, form, change, *args, **kwargs)
        learning_objectives = form.cleaned_data['learning_objs']
        ctype = ContentType.objects.get_for_model(Lesson)
        # clear existing
        objectiverelations = ObjectiveRelation.objects.filter(
            content_type=ctype,
            object_id=obj.id)

        for objectiverelation in objectiverelations:
            objectiverelation.objective.delete()
            objectiverelation.delete()

        # create new
        for learning_objective in learning_objectives.split('\r\n'):
            if learning_objective and len(learning_objective) > 0:
                lo, created = LearningObjective.objects.get_or_create(text=learning_objective)
                o_rel = ObjectiveRelation(objective=lo, content_type=ctype, object_id=obj.id)
                o_rel.save()

    def response_add(self, request, obj, post_url_continue=None):
        obj.save()
        import django
        if post_url_continue is None and django.VERSION[1] < 5:
            post_url_continue = '../%s/'
        return super(LessonAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        obj.save()
        return super(LessonAdmin, self).response_change(request, obj)

    def update_ARs(self, obj, rcs):  # NOQA
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
    list_filter = ('standard_type', 'grades')
    search_fields = ['name', 'definition']
    fields = ('standard_type', 'name', 'definition', 'state', 'url', 'grades', )

    def grade_levels(self, obj):
        return obj.grades.all().as_grade_range()
    grade_levels.short_description = 'Grades'


class TipAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {
            # 'choices': AUDIENCE_FLAGS,
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
        js = ()

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
            formfield.widget = CKEditorWidget(config_name='simple_paragraph')
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
        model = UnitRelation
        template = 'admin/edit_inline/ic_coll_tabular.html'


class UnitAdmin(admin.ModelAdmin):
    date_hierarchy = 'published_date'
    filter_horizontal = ['secondary_content_types', ]
    readonly_fields = ['eras', 'relevant_start_date', 'relevant_end_date',
        'geologic_time', 'subjects', 'grades', ]
    form = UnitForm
    formfield_overrides = {
        BitField: {
            # 'choices': AUDIENCE_FLAGS,
            'initial': 1,
            'widget': AdminBitFieldWidget()
        }
    }
    object_name = 'unit'
    inlines = [ResourceCarouselInline, LessonInline, TagInline]
    if RELATION_MODELS:
        inlines += [InlineUnitRelation, ]
    list_display = ('title', thumbnail_display, 'overview_display', 'appropriate_display', 'published_date')
    list_filter = ('published_date', 'published', 'archived')
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("key_image", "credit", )
    tabs = {
        'Overview': 0,
        'Credits, Sponsors, Partners': 0,
        'Global Metadata': 1,
        'Content Related Metadata': 1,
        'Time and Date Metadata': 1,
        'Publishing': 2,
    }
    varying_fields = AUDIENCE_FIELDS.get('curricula.Unit', [])

    class Media:
        css = {
            'all': ('audience/bitfield.css',),
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
            formfield.widget = CKEditorWidget(config_name='simple_paragraph')
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
        fieldsets.append(
            ('Overview', {'fields': ['appropriate_for', 'title', 'slug', 'subtitle', 'key_image', 'description', 'overview', 'id_number'], 'classes': ['collapse']}),
        )

        fieldsets.append(('Credits, Sponsors, Partners', {'fields': ['credit'], 'classes': ['collapse']}))
        fieldsets.append(('Global Metadata', {'fields': ['secondary_content_types'], 'classes': ['collapse']}))
        fieldsets += [
            ('Content Related Metadata', {'fields': ['subjects', 'grades'], 'classes': ['collapse']}),
            ('Time and Date Metadata', {'fields': ['eras', 'geologic_time', 'relevant_start_date', 'relevant_end_date'], 'classes': ['collapse']}),
            ('Publishing', {'fields': ['published', 'published_date', 'archived'], 'classes': ['collapse']}),
        ]
        return fieldsets

    def response_add(self, request, obj, post_url_continue=None):
        obj.save()
        import django
        if post_url_continue is None and django.VERSION[1] < 5:
            post_url_continue = '../%s/'
        return super(UnitAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        obj.save()
        return super(UnitAdmin, self).response_change(request, obj)


admin.site.register(Activity, ActivityAdmin)
admin.site.register(GroupingType)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaCategory, IdeaCategoryAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Material, TypeAdmin)
admin.site.register(Skill, SkillAdmin)
if settings.DEBUG:
    admin.site.register(LearningObjective)
    admin.site.register(PluginType)
    admin.site.register(QuestionAnswer)
    admin.site.register(TeachingApproach)
admin.site.register(Standard, StandardAdmin)
admin.site.register(TeachingMethodType, TypeAdmin)
admin.site.register(Tip, TipAdmin)
admin.site.register(Unit, UnitAdmin)
