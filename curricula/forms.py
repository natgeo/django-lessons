from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model

from .models import Activity, ObjectiveRelation, Lesson, IdeaCategory, Unit
from .settings import ACTIVITY_FIELDS, LESSON_FIELDS, CREDIT_MODEL
from .widgets import SpecificGenericRawIdWidget

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
        exclude = ['concepts']

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)

        for field in ACTIVITY_FIELDS:
            field_name = field[0]
            model = get_model(*field[1].split('.'))
            self.fields[field_name] = forms.ModelChoiceField(
                queryset=model.objects.all(),
                widget=SpecificGenericRawIdWidget(rel=field[1]),
                required=False)
            # for existing records, initialize the fields
            if instance:
                objects = instance.relations.filter(relation_type=field_name)
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


class ActivityFormSet(forms.models.BaseInlineFormSet):
    def get_queryset(self):
        'Returns all ActivityRelation objects which point to our Lesson'
        return super(ActivityFormSet, self).get_queryset().exclude(relation_type__in=dict(ACTIVITY_FIELDS).keys())


class ActivityInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super(ActivityInlineFormset, self).clean()

        for form in self.forms:
            if not form.instance:
                form.save(commit=False)

            order = form.cleaned_data.get('order')
            if not order:
                pass

            activity = form.cleaned_data.get('activity')
            if 'published' in self.data and activity and not activity.published:
                raise forms.ValidationError('Please publish all associated activities, before publishing this lesson.')


class LessonInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super(LessonInlineFormset, self).clean()

        count = 0
        for form in self.forms:
            if form.cleaned_data != {} and form.cleaned_data['DELETE'] == False:
                count += 1
        if count <= 0:
            if 'published' in self.data:
                raise forms.ValidationError('Please include at least one lesson, before publishing this unit.')


class LessonForm(forms.ModelForm):
    learning_objs = forms.CharField(
        required=False,
        label='Learning objectives',
        widget=forms.Textarea(attrs={'cols': 128, 'rows': 5}),
        help_text='''All learning objectives from the activities within the
        lesson will dynamically display. Only use this field if you need to add
        additional, lesson-level learning objectives.

        Each learning objective must be separated by a carriage return. Each
        line displays as a bulleted list.''')

    class Media:
        js = (
            settings.STATIC_URL + 'js/jquery-1.7.1.js',
            settings.STATIC_URL + 'js/jquery/ui.core.js',
            settings.STATIC_URL + 'js/jquery/ui.sortable.js',
            settings.STATIC_URL + 'js/menu-sort.js',
        )

    class Meta:
        model = Lesson
        exclude = ['concepts']

    def initialize_values(self, kwargs, field_name):
        if kwargs.has_key('instance'):
            objects = kwargs['instance'].relations.filter(relation_type=field_name)
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

    # def clean_reporting_categories(self):
    #     reporting_categories = self.cleaned_data['reporting_categories']

    #     if self.cleaned_data['published'] and not reporting_categories:
    #         if len(reporting_categories) == 0:
    #             raise forms.ValidationError("Reporting Categories is required for published content.")

    #     return reporting_categories


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


class UnitForm(forms.ModelForm):
    class Media:
        css = {
            'all': (settings.STATIC_URL + 'audience/bitfield.css',),
        }
        js = (
            settings.STATIC_URL + 'js/jquery-1.7.1.js',
            settings.STATIC_URL + 'js/jquery/ui.core.js',
            settings.STATIC_URL + 'js/jquery/ui.sortable.js',
            settings.STATIC_URL + 'js/menu-sort.js',
        )

    class Meta:
        model = Unit

    def clean(self):
        cleaned_data = super(UnitForm, self).clean()

        if cleaned_data['published']:
            if cleaned_data['credit'] is None:
                raise forms.ValidationError("Credit is required for published units.")
            # for field in ['grades', 'subjects']:
            #     if not cleaned_data[field]:
            #         raise forms.ValidationError("%s is required for published units." % field.replace('_', ' ').capitalize())

            # content_type = ContentType.objects.get_for_model(Unit)
            # concept_items = ConceptItem.objects.filter(content_type=content_type,
            #                                            object_id=self.instance.id,
            #                                            weight__gt=0)
            # if len(concept_items) <= 0:
            #     raise forms.ValidationError("Please uncheck Publish, create at least one tag with weight greater than zero, and then save, before attempting to mark this object as published.")
        return cleaned_data

    def clean_appropriate_for(self):
        appropriate_for = self.cleaned_data['appropriate_for']
        if appropriate_for == 0:
            raise forms.ValidationError("Appropriate for is a required field for units.")

        return appropriate_for
