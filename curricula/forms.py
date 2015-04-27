from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from .models import Activity, ObjectiveRelation, Lesson, IdeaCategory, Unit


class ActivityForm(forms.ModelForm):
    learning_objs = forms.CharField(
        required=False,
        label='Learning objectives',
        widget=forms.Textarea(attrs={'cols': 128, 'rows': 5}),
        help_text="Each learning objective must be separated by a carriage "
                  "return. Each line displays as a bulleted list.")

    class Media:
        js = (
            # 'js/jquery/ui.core.js',
            # 'js/jquery/ui.sortable.js',
            # 'js/menu-sort.js',
        )

    class Meta:
        model = Activity
        exclude = ['concepts']

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)

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
        atype = cleaned_data['assessment_type']
        assessment = cleaned_data['assessment']
        if assessment and not atype:
            raise forms.ValidationError("Assessment Type is required, when "
                                        "there is an Assessment.")
        return cleaned_data

    def clean_field(self, name):
        field = self.cleaned_data[name]
        if 'published' in self.cleaned_data and self.cleaned_data['published'] and not field:
            raise forms.ValidationError("This field is required for "
                                        "published activities.")

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
        return super(ActivityFormSet, self).get_queryset()


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
                msg = "Please publish all associated activities before " \
                      "publishing this lesson."
                raise forms.ValidationError(msg)


class LessonInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super(LessonInlineFormset, self).clean()

        count = 0
        for form in self.forms:
            if form.cleaned_data != {} and not form.cleaned_data['DELETE']:
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
            # 'js/jquery/ui.core.js',
            # 'js/jquery/ui.sortable.js',
            # 'js/menu-sort.js',
        )

    class Meta:
        model = Lesson
        exclude = ['concepts']

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)

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


class IdeaCategoryForm(forms.ModelForm):
    class Meta:
        model = IdeaCategory

    def clean(self):
        cleaned_data = super(IdeaCategoryForm, self).clean()
        self.clean_field('credit')
        self.clean_field('grades')
        self.clean_field('license_name')
        self.clean_field('subjects')

        return cleaned_data

    def clean_field(self, name):
        field = self.cleaned_data[name]
        msg = "%s is required for published idea categories." % name.capitalize()
        if 'published' in self.cleaned_data:
            if self.cleaned_data['published'] and not field:
                raise forms.ValidationError(msg)


class UnitForm(forms.ModelForm):
    class Media:
        css = {
            'all': (settings.STATIC_URL + 'audience/bitfield.css',),
        }
        js = (
            # 'js/jquery/ui.core.js',
            # 'js/jquery/ui.sortable.js',
            # 'js/menu-sort.js',
        )

    class Meta:
        model = Unit
        fields = ['appropriate_for', 'credit', 'description', 'id_number',
            'key_image', 'lessons', 'overview', 'published', 'published_date',
            'secondary_content_types', 'slug', 'subtitle', 'title', 'eras',
            'geologic_time', 'grades', 'relevant_start_date',
            'relevant_end_date', 'subjects', ]

    def clean(self):
        cleaned_data = super(UnitForm, self).clean()

        if cleaned_data['published']:
            if cleaned_data['credit'] is None:
                raise forms.ValidationError("Credit is required for published units.")
        return cleaned_data

    def clean_appropriate_for(self):
        appropriate_for = self.cleaned_data['appropriate_for']
        if appropriate_for == 0:
            raise forms.ValidationError("Appropriate for is a required field for units.")

        return appropriate_for
