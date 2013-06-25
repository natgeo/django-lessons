from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from genericcollection import GenericCollectionInlineModelAdmin

from models import (Activity, ActivityRelation, GroupingType,
                     LearningObjective, Lesson, LessonActivity, LessonRelation,
                     Material, ObjectiveRelation, QuestionAnswer, ResourceItem,
                     Skill, Standard, TeachingApproach, TeachingMethodType,
                     Tip, Vocabulary, Idea, IdeaCategory, CategoryIdea,
                     IdeaCategoryRelation)
if settings.DEBUG:
    from models import PluginType
from settings import (RELATION_MODELS, JAVASCRIPT_URL, KEY_IMAGE,
                      CREDIT_MODEL, REPORTING_MODEL)
from utils import truncate, get_audience_indices
from widgets import VocabularyIdWidget

from tinymce.widgets import TinyMCE
from audience.models import AUDIENCE_FLAGS
from audience.widgets import AdminBitFieldWidget, bitfield_display, VariationWidgetWrapper
from bitfield import BitField
from concepts.admin import ConceptItemInline
from contentrelations.admin import RelatedInline


class ResourceCarouselInline(RelatedInline):
    rel_name = 'resources'
    verbose_name_plural = "Resource Carousel"
    exclude = ('source_type', 'source_id', 'relation_type')


TINYMCE_FIELDS = ('description', 'assessment', 'learning_objectives', 'other_notes', 'background_information')
ACTIVITY_TINYMCE_FIELDS = TINYMCE_FIELDS + ('extending_the_learning', 'setup', 'accessibility_notes', 'prior_knowledge')
IDEACATEGORY_TINYMCE_FIELDS = ('content_body', 'description')
LESSON_TINYMCE_FIELDS = TINYMCE_FIELDS + ('subtitle_guiding_question', 'prior_knowledge')

MCE_SIMPLE_ATTRS = {
    'plugins': "rawmode,paste",
    'theme_advanced_buttons1': "pasteword,|,bold,underline,italic,strikethrough,|,link,unlink,|,numlist,bullist,|,charmap,|,rawmode",
    'theme_advanced_buttons2': "",
}

ACTIVITY_FIELDS = []
if KEY_IMAGE is not None:
    ACTIVITY_FIELDS.append(KEY_IMAGE)

LESSON_FIELDS = []
if KEY_IMAGE is not None:
    LESSON_FIELDS.append(KEY_IMAGE)
try:
    from django.contrib.admin.templatetags.admin_static import static
except ImportError:
    def static(somestring):
        return "%s%s" % (settings.ADMIN_MEDIA_PREFIX, somestring)

JAVASCRIPT_URL = settings.STATIC_URL + 'js/'

def rcs_name(title):
    return truncate("Lesson Overview - %s" % title, 47)


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
    class ActivityFormSet(forms.models.BaseInlineFormSet):
        def get_queryset(self):
            'Returns all ActivityRelation objects which point to our Lesson'
            return super(ActivityFormSet, self).get_queryset().exclude(relation_type__in=dict(ACTIVITY_FIELDS).keys())

    class InlineActivityRelation(GenericCollectionInlineModelAdmin):
        extra = 7
        model = ActivityRelation
        formset = ActivityFormSet
        template = 'admin/edit_inline/ic_coll_tabular.html'


class SpecificGenericRawIdWidget(forms.TextInput):
    def __init__(self, rel, attrs=None):
        self.rel = rel
        super(SpecificGenericRawIdWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        # if 'class' not in attrs:
        #     attrs['class'] = 'vGenericRawIdAdminField'  # The JavaScript looks for this hook.
        output = [super(SpecificGenericRawIdWidget, self).render(name, value, attrs)]
        output.append('<a id="lookup_id_%(name)s" class="related-lookup" onclick="return showGenericRequiredModelLookupPopup(this, \'%(rel)s\');" href="#">' %
            {'name': name, 'rel': self.rel})
        output.append('&nbsp;<img src="%s" width="16" height="16" alt="%s" /></a>' % (static('admin/img/selector-search.gif'), 'Lookup'))
        return mark_safe(u''.join(output))

    class Media:
        js = ('js/genericcollections.js', )


class ActivityForm(forms.ModelForm):
    learning_objs = forms.CharField(required=False, label='Learning objectives',
                                    widget=forms.Textarea(attrs={'cols': 128, 'rows': 5}),
                                    help_text="Each learning objective must be separated by a carriage return. Each line displays as a bulleted list.")

    class Media:
        js = (
            settings.STATIC_URL + 'js/jquery-1.7.1.js',
            settings.STATIC_URL + 'js/jquery/ui.core.js',
            settings.STATIC_URL + 'js/jquery/ui.sortable.js',
            settings.STATIC_URL + 'js/menu-sort.js',
        )

    class Meta:
        model = Activity

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)

        for field in ACTIVITY_FIELDS:
            field_name = field[0]
            model = get_model(*field[1].split('.'))
            self.fields[field_name] = forms.ModelChoiceField(queryset=model.objects.all(), widget=SpecificGenericRawIdWidget(rel=field[1]), required=False)
            # for existing records, initialize the fields
            if instance:
                objects = instance.activityrelation_set.filter(relation_type=field_name)
                if len(objects) > 0:
                    self.fields[field_name].initial = objects[0].object_id

        if instance:
            ctype = ContentType.objects.get_for_model(Activity)
            initial_objs = ''
            objectiverelations = ObjectiveRelation.objects.filter(
                                    content_type=ctype, object_id=instance.id)
            objectiverelations = objectiverelations.filter()
            for objectiverelation in objectiverelations:
                initial_objs += objectiverelation.objective.text
                initial_objs += '\r\n'
            self.fields['learning_objs'].initial = initial_objs.strip('\r\n')

    def clean(self):
        cleaned_data = super(ActivityForm, self).clean()
        for field in ACTIVITY_FIELDS:
            field_name = field[0]

            if field_name not in self.cleaned_data:
                raise forms.ValidationError("%s is required." % field_name)
        return cleaned_data

    def clean_assessment_type(self):
        atype = self.cleaned_data['assessment_type']
        assessment = self.cleaned_data['assessment']
        if assessment and not atype:
            raise forms.ValidationError("Assessment Type is required, when there is an Assessment.")

        return atype

    def clean_field(self, name):
        field = self.cleaned_data[name]
        if 'published' in self.cleaned_data and self.cleaned_data['published'] and not field:
            raise forms.ValidationError("This field is required, for published activities.")

        return field

    def clean_background_information(self):
        return self.clean_field('background_information')

    def clean_directions(self):
        return self.clean_field('directions')

    def clean_grades(self):
        return self.clean_field('grades')

    def clean_grouping_types(self):
        return self.clean_field('grouping_types')

    def clean_internet_access_type(self):
        return self.clean_field('internet_access_type')

    # def clean_materials(self):
    #     return self.clean_field('materials')

    # EDU-3361
    def clean_reporting_categories(self):
        return self.clean_field('reporting_categories')

    def clean_skills(self):
        return self.clean_field('skills')

    def clean_subjects(self):
        return self.clean_field('subjects')

    def clean_standards(self):
        return self.clean_field('standards')

    def clean_teaching_approaches(self):
        return self.clean_field('teaching_approaches')

    def clean_teaching_method_types(self):
        return self.clean_field('teaching_method_types')


class ContentAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
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
    varying_fields = ('assessment', 'background_information', 'description', 'extending_the_learning', 'subtitle_guiding_question', 'title', 'directions', 'learning_objectives', 'prior_knowledge')

    class Media:
        css = {'all': (
            "css/glossary_term.css",
        )}

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ActivityAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ACTIVITY_TINYMCE_FIELDS:
            formfield.widget = TinyMCE(mce_attrs=MCE_SIMPLE_ATTRS)
        elif db_field.name == 'subtitle_guiding_question':
            formfield.widget = TinyMCE(mce_attrs={
               'plugins': "rawmode,paste",
               'theme_advanced_buttons1': "pasteword,|,bold,underline,italic,strikethrough,|,link,unlink,|,numlist,bullist,|,charmap,|,rawmode",
               'theme_advanced_buttons2': "",
               'height': "150",
            })
        elif db_field.name == 'directions':
            formfield.widget = TinyMCE(mce_attrs={
                'content_css' : settings.STATIC_URL + "css/glossary_term.css",
                'theme_advanced_buttons1': 'glossify, fullscreen,preview,code,print,spellchecker,|,cut,copy,paste,pastetext,pasteword,undo,redo,|,search,replace,|,rawmode',
                'setup': 'add_button_callback',
            })
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
                items = obj.activityrelation_set.filter(relation_type=field)
                if len(items) > 0:
                    items[0].delete()
            else:
                try:
                    item = obj.activityrelation_set.get(relation_type=field)
                    item.object_id = form[field].data
                    item.save()
                except ActivityRelation.DoesNotExist:
                    app_label, model = model.split('.')
                    ctype = ContentType.objects.get(app_label=app_label, model=model)
                    item = obj.activityrelation_set.create(relation_type=field, object_id=form[field].data, content_type_id=ctype.id)

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


class ActivityInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super(ActivityInlineFormset, self).clean()

        for form in self.forms:
            if form.instance:
                model_instance = form.instance
            else:
                model_instance = form.save(commit=False)

            activity = form.cleaned_data.get('activity')
            if 'published' in self.data and activity and not activity.published:
                raise forms.ValidationError('Please publish all associated activities, before publishing this lesson.')


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
            formfield.widget = TinyMCE(mce_attrs=MCE_SIMPLE_ATTRS)

        return formfield

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


class IdeaCategoryForm(forms.ModelForm):
    class Meta:
        model = IdeaCategory

    def clean(self):
        cleaned_data = super(IdeaCategoryForm, self).clean()

        if CREDIT_MODEL:
            self.clean_field('credit')
        self.clean_field('grades')
        self.clean_field('license_name')
        self.clean_field('subjects')

        return cleaned_data

    def clean_field(self, name):
        field = self.cleaned_data[name]
        if 'published' in self.cleaned_data:
            if self.cleaned_data['published'] and not field:
                raise forms.ValidationError("%s is required, for published activities." % name.capitalize())


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
            formfield.widget = TinyMCE(mce_attrs=MCE_SIMPLE_ATTRS)

        return formfield

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


class LessonForm(forms.ModelForm):
    learning_objs = forms.CharField(required=False, label='Learning objectives',
                                    widget=forms.Textarea(attrs={'cols': 128, 'rows': 5}),
                                    help_text='''All learning objectives from the activities within the lesson will dynamically display. Only use this field if you need to add additional, lesson-level learning objectives.
                                                 Each learning objective must be separated by a carriage return. Each line displays as a bulleted list.''')

    class Media:
        js = (
            settings.STATIC_URL + 'js/jquery-1.7.1.js',
            settings.STATIC_URL + 'js/jquery/ui.core.js',
            settings.STATIC_URL + 'js/jquery/ui.sortable.js',
            settings.STATIC_URL + 'js/menu-sort.js',
        )

    class Meta:
        model = Lesson

    def initialize_values(self, kwargs, field_name):
        if kwargs.has_key('instance'):
            objects = kwargs['instance'].lessonrelation_set.filter(relation_type=field_name)
            if len(objects) > 0:
                self.fields[field_name].initial = objects[0].object_id

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        for field in LESSON_FIELDS:
            field_name = field[0]
            qset = get_model(*field[1].split('.')).objects.all()
            self.fields[field_name] = forms.ModelChoiceField(queryset=qset, widget=SpecificGenericRawIdWidget(rel=field[1]))
            self.initialize_values(kwargs, field_name)

        if instance:
            ctype = ContentType.objects.get_for_model(Lesson)
            initial_objs = ''
            objectiverelations = ObjectiveRelation.objects.filter(
                                    content_type=ctype, object_id=instance.id)
            for objectiverelation in objectiverelations:
                initial_objs += objectiverelation.objective.text
                initial_objs += '\r\n'
            self.fields['learning_objs'].initial = initial_objs.strip('\r\n')

    def clean(self):
        cleaned_data = super(LessonForm, self).clean()

        field_name = 'key_image'

        if field_name not in self.cleaned_data:
            raise forms.ValidationError("%s is required." % field_name)
        return cleaned_data

    # EDU-3361
    def clean_reporting_categories(self):
        reporting_categories = self.cleaned_data['reporting_categories']

        if self.cleaned_data['published'] and not reporting_categories:
            if len(reporting_categories) == 0:
                raise forms.ValidationError("Reporting Categories is required for published content.")

        return reporting_categories

class LessonAdmin(ContentAdmin):
    filter_horizontal = ['eras', 'materials', 'secondary_content_types', 'prior_lessons']
    if REPORTING_MODEL:
        filter_horizontal += ['reporting_categories']
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
    varying_fields = ('title', 'subtitle_guiding_question', 'description', 'directions', 'assessment', 'learning_objectives', 'background_information', 'prior_knowledge')

    class Media:
        css = {'all': (
            "css/glossary_term.css",
            settings.STATIC_URL + 'audience/bitfield.css'
        )}

    def appropriate_display(self, obj):
        activities = obj.get_activities()
        if len(activities) > 0:
            appropriate_for = activities[0].appropriate_for
            if len(activities) > 1:
                for i in range(1, len(activities)):
                    appropriate_for |= activities[i].appropriate_for
            return bitfield_display(appropriate_for)
        else:
            return ''

    appropriate_display.short_description = 'Appropriate For'
    appropriate_display.allow_tags = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(LessonAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in LESSON_TINYMCE_FIELDS:
            formfield.widget = TinyMCE(mce_attrs=MCE_SIMPLE_ATTRS)
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
            a_items = lessonvariation.audience.items()
            audience_indices = get_audience_indices(a_items)
            unique_indices = list(set(unique_indices + audience_indices))
            # reading level/ text difficulty 6 = Not Applicable
            rcs.body.create_ARs(
                '%s-[6]' % audience_indices,
                lessonvariation.variation)
        # default
        audience_indices = get_audience_indices(obj.appropriate_for.items())
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
