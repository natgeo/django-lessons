#import datetime
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.utils.html import strip_tags

from settings import (ASSESSMENT_TYPES, STANDARD_TYPES,
                      PEDAGOGICAL_PURPOSE_TYPE_CHOICES, RELATION_MODELS,
                      RELATIONS, CREDIT_MODEL, INTERNET_ACCESS_TYPES,
                      REPORTING_MODEL, KEY_IMAGE, RESOURCE_CAROUSEL,
                      GLOSSARY_MODEL, RESOURCE_MODEL, RELATION_TYPES,
                      DEFAULT_LICENSE)
from utils import truncate, ul_as_list

from audience.models import AUDIENCE_FLAGS
from audience.widgets import bitfield_display
from bitfield import BitField
from categories.models import CategoryBase
from concepts.models import delete_listener

from edumetadata.models import (AlternateType, GeologicTime, Grade,
                                 HistoricalEra, Subject)
from edumetadata.fields import HistoricalDateField
from licensing.models import GrantedLicense
#from publisher import register
#from publisher.models import Publish

if len(KEY_IMAGE) > 0:
    KeyImageModel = KEY_IMAGE[1]
if CREDIT_MODEL is not None:
    CreditModel = get_model(*CREDIT_MODEL.split('.'))
if REPORTING_MODEL is not None:
    ReportingModel = get_model(*REPORTING_MODEL.split('.'))

def gradesDict(grades_list):
    g = {}
    special = {'K': 0, 'preschool': -1, 'post-secondary': 13}
    for item in grades_list:
        if item.isdigit():
            g[item] = int(item)
        else:
            try:
                g[item] = special[item]
            except KeyError:
                pass
    return g


def grades_html(grades):
    if not grades:
        return ''

    min_age = min([grade.min_age for grade in grades])
    max_age = max([grade.max_age for grade in grades])
    grades_grad = [x.name if x.name != u'13' else u'12+' for x in grades]

    if 'Unknown' in grades_grad:
        _grades_html = "<span class='grades'>Grades: Unknown</span><br>Ages: Unknown"
    elif 'All' in grades_grad:
        _grades_html = "Grades: All<br>Ages: All"
    elif len(grades_grad) == 1:
        if grades_grad[0] == u'12+':
            _grades_html = "<span class='grades'>Post-secondary</span><br/>Age %s" % (
                min_age)
        else:
            _grades_html = "<span class='grades'>Grade %s</span><br/>Age %s" % (
                grades_grad[0], min_age)
    elif len(grades_grad) > 1:
        gradestuple = sorted(gradesDict(grades_grad).iteritems(),
                key=lambda (k, v): (v, k))
        _grades_html = "<span class='grades'>Grades %s-%s</span><br/>Ages %s-%s" % (
                gradestuple[0][0], gradestuple[-1][0],
                    min_age, max_age) if \
                gradestuple[0][0] != gradestuple[-1][0] else \
                    "Grade %s<br>Age %s" % \
                    (gradestuple[0][0], min_age)

    return _grades_html


class TypeModel(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class GroupingType(TypeModel):
    pass


class LearnerGroup(models.Model):
    name = models.CharField(max_length=31)

    def __unicode__(self):
        return self.name

OBJ_REL_MODELS = ('curricula.activity', 'curricula.lesson')
OBJ_RELS = [Q(app_label=al, model=m) for al, m in [x.split('.') for x in OBJ_REL_MODELS]]
obj_rel_limits = reduce(lambda x, y: x | y, OBJ_RELS)


class LearningObjective(models.Model):
    text = models.TextField()

    def __unicode__(self):
        return self.text


class ObjectiveRelation(models.Model):
    objective = models.ForeignKey(LearningObjective)
    content_type = models.ForeignKey(
        ContentType, limit_choices_to=obj_rel_limits)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()


class Material(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class PhysicalSpaceType(TypeModel):
    is_default = models.NullBooleanField()


class PluginType(TypeModel):
    source_url = models.CharField(max_length=128)


class Skill(CategoryBase):
    appropriate_for = BitField(flags=AUDIENCE_FLAGS)
    url = models.CharField(max_length=128, blank=True, null=True)


class TeachingApproach(TypeModel):
    pass


class TeachingMethodType(TypeModel):
    pass


class TechSetupType(models.Model):
    title = models.CharField(max_length=64)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]

TIP_TYPE_CHOICES = (
    (1, 'Tip'),
    (2, 'Modification'),
)


class TipCategory(CategoryBase):
    """
    Tip-specific categories
    """
    pass


class Tip(models.Model):
    appropriate_for = BitField(flags=AUDIENCE_FLAGS)
    content_creation_time = models.DateTimeField(auto_now_add=True)
    id_number = models.CharField(max_length=5, blank=True, null=True)
    tip_type = models.PositiveSmallIntegerField(choices=TIP_TYPE_CHOICES)
    body = models.TextField()
    category = models.ForeignKey(TipCategory, blank=True, null=True)

    class Meta:
        ordering = ["category", "body"]
        verbose_name_plural = "Tips & Modifications"

    def __unicode__(self):
        if self.category:
            return u'%s: %s' % (self.category.name,
                               truncate(strip_tags(self.body), 38))
        else:
            return truncate(strip_tags(self.body), 71)


class Standard(models.Model):
    definition = models.TextField('Standard text', null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    standard_type = models.IntegerField(choices=STANDARD_TYPES)
    state = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        choices=STATE_CHOICES)
    thinkfinity_code = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    when_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    grades = models.ManyToManyField(Grade)

    def __unicode__(self):
        return u"%s: %s: %s" % (truncate(self.get_standard_type_display(), 50),
                               truncate(self.name, 40),
                               truncate(strip_tags(self.definition), 50))

    class Meta:
        ordering = ["standard_type", "name"]


class ContentManager(models.Manager):
    def get_published(self):
        qs = self.get_query_set()
        return qs.filter(published=True)


class Activity(models.Model):
    appropriate_for = BitField(
        flags=AUDIENCE_FLAGS,
        help_text='''Select the audience(s) for which this content is
        appropriate. Selecting audiences means that a separate audience view of
        the page will exist for those audiences.

        Note that the text you input in this form serves as the default text.
        If you indicate this activity is appropriate for multiple audiences,
        you either need to add text variations or the default text must be
        appropriate for those audiences.''')
    title = models.CharField(
        max_length=256,
        help_text="""GLOBAL: Use the text variations field to create versions
        for audiences other than the default.""")
    ads_excluded = models.BooleanField(
        default=True, verbose_name="Are ads excluded?",
        help_text="""If unchecked, this field indicates that external ads are
        allowed.""")
    assessment = models.TextField(
        blank=True,
        null=True)
    assessment_type = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        choices=ASSESSMENT_TYPES)
    create_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    duration = models.IntegerField(verbose_name="Duration Minutes")
    extending_the_learning = models.TextField(
        blank=True,
        null=True)
    grades = models.ManyToManyField(Grade,
        blank=True,
        null=True)
    id_number = models.CharField(
        max_length=10,
        help_text="""This field is for the internal NG Education ID number. This
        is required for all instructional content.""")
    is_modular = models.BooleanField(
        default=True,
        help_text="""If unchecked, this field indicates that this activity
        should not appear as stand-alone outside of a lesson view.""")
    learner_groups = models.ManyToManyField(LearnerGroup,
        blank=True,
        null=True)
    notes_on_readability_score = models.TextField(
        blank=True,
        null=True,
        help_text="""Use this internal-use only field to record any details
        related to the readability of reading passages, such as those on
        handouts. Include Lexile score, grade-level equivalent, and any
        criteria used to determine why a higher score is acceptable
        (proper nouns, difficult vocabulary, etc.).""")
    pedagogical_purpose_type = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=PEDAGOGICAL_PURPOSE_TYPE_CHOICES)
    published = models.BooleanField()
    published_date = models.DateTimeField(
        blank=True,
        null=True)
    slug = models.SlugField(
        unique=True,
        max_length=100,
        help_text="""The URL slug is auto-generated, but producers should adjust
        it if: a) punctuation in the title causes display errors; and/or b) the
        title changes after the slug has been generated.""")
    standards = models.ManyToManyField(Standard,
        blank=True,
        null=True)
    subjects = models.ManyToManyField(Subject,
        blank=True,
        null=True,
        limit_choices_to={'parent__isnull': False},
        verbose_name="Subjects and Disciplines")
    subtitle_guiding_question = models.TextField(
        verbose_name="Subtitle or Guiding Question")

   #Directions
    directions = models.TextField(
        blank=True,
        null=True)
    tips = models.ManyToManyField(Tip,
        blank=True,
        null=True,
        verbose_name="Tips & Modifications")

   #Objectives
    learning_objective_set = generic.GenericRelation(ObjectiveRelation)
    skills = models.ManyToManyField(Skill,
        blank=True,
        null=True,
        limit_choices_to={'children__isnull': True})
    teaching_approaches = models.ManyToManyField(TeachingApproach,
        blank=True,
        null=True)
    teaching_method_types = models.ManyToManyField(TeachingMethodType,
        blank=True,
        null=True)

   #Preparation
    accessibility_notes = models.TextField(
        blank=True,
        null=True)
    materials = models.ManyToManyField(Material,
        blank=True,
        null=True)
    grouping_types = models.ManyToManyField(GroupingType,
        blank=True,
        null=True)
    other_notes = models.TextField(
        blank=True,
        null=True)
    physical_space_types = models.ManyToManyField(PhysicalSpaceType,
        blank=True,
        null=True)
    prior_activities = models.ManyToManyField('self',
        blank=True,
        null=True,
        symmetrical=False,
        verbose_name="Recommended Prior Activities")
    setup = models.TextField(
        blank=True,
        null=True)

   #Required Technology
    internet_access_type = models.IntegerField(
        blank=True,
        null=True,
        choices=INTERNET_ACCESS_TYPES)
    plugin_types = models.ManyToManyField(PluginType,
        blank=True,
        null=True)
    tech_setup_types = models.ManyToManyField(TechSetupType,
        blank=True,
        null=True)

   #Background & Vocabulary
    background_information = models.TextField(
        blank=True,
        null=True,
        help_text="""If this activity is part of an already-created lesson and
        you update the background information, you must also make the same
        change in lesson for this field.""")
    prior_knowledge = models.TextField(
        blank=True,
        null=True)

  # Credits, Sponsors, Partners
    if CREDIT_MODEL:
        credit = models.ForeignKey(CreditModel,
            blank=True,
            null=True)

  # Global Metadata
    if REPORTING_MODEL:
        reporting_categories = models.ManyToManyField(ReportingModel,
            blank=True,
            null=True)

  # Content Related Metadata
    secondary_content_types = models.ManyToManyField(AlternateType,
        blank=True,
        null=True)

  # Time and Date Metadata
    eras = models.ManyToManyField(HistoricalEra,
        blank=True,
        null=True)
    geologic_time = models.ForeignKey(GeologicTime,
        blank=True,
        null=True)
    relevant_start_date = HistoricalDateField(
        blank=True,
        null=True)
    relevant_end_date = HistoricalDateField(
        blank=True,
        null=True)

    objects = ContentManager()

    @models.permalink
    def get_absolute_url(self):
        return ('activity-detail', (), {'slug': self.slug})

    def __unicode__(self):
        return strip_tags(self.title)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = 'Activities'

    def get_canonical_page(self):
        for i in range(0, 5):
            if self.appropriate_for.get_bit(i).is_set:
                return '%s?ar_a=%s' % (reverse('activity-detail', args=[self.slug]), i + 1)

    def get_grades_and_ages(self):
        return self.grades.all().as_grade_age_range()

    @property
    def get_grades_html(self):
        from django.template.loader import render_to_string
        ctxt = self.grades.all().as_struct()
        return render_to_string('curricula/grades.html', ctxt)

    @property
    def get_grades_range(self):
        from django.template.loader import render_to_string
        ctxt = self.grades.all().as_struct()
        return render_to_string('curricula/grades_range.html', ctxt)

    def get_lessons(self):
        lessonactivities = LessonActivity.objects.filter(activity=self)
        return [lessonactivity.lesson for lessonactivity in lessonactivities]

    def get_published_lessons(self):
        return [lesson for lesson in self.get_lessons() if lesson.published]

    if CREDIT_MODEL:
        def get_credit_details(self):
            # [EDU-3431] Credit Category display order not working
            credit_details = SortedDict()
            if self.credit and self.credit.credit_details:
                for detail in self.credit.credit_details.order_by('credit_category__order'):
                    if detail.credit_category not in credit_details:
                        credit_details[detail.credit_category] = []
                    credit_details[detail.credit_category].append(detail.entity)
            return credit_details

    if RELATION_MODELS:
        def get_related_content_type(self, content_type):
            """
            Get all related items of the specified content type
            """
            return self.activityrelation_set.filter(
                content_type__name=content_type)

        def get_relation_type(self, relation_type):
            """
            Get all relations of the specified relation type
            """
            return self.activityrelation_set.filter(
                relation_type__iexact=relation_type)

        def get_content_object(self, field):
            app_label, model = field[1].split('.')
            ctype = ContentType.objects.get(app_label=app_label, model=model.lower())
            ar = self.get_related_content_type(ctype.name)
            if len(ar) > 0:
                return ar[0].content_object
            else:
                return None

        def get_key_image(self):
            return self.get_content_object(KEY_IMAGE)

        def key_image(self):
            content_object = self.get_key_image()
            if content_object:
                return content_object.thumbnail_url()
            else:
                return None

        def thumbnail_html(self):
            # [EDU-2866]
            key_image = self.key_image()
            if key_image:
                return '<img src="%s"/>' % self.key_image()
            else:
                return None


class Vocabulary(models.Model):
    activity = models.ForeignKey(Activity)
    glossary_term = models.ForeignKey(GLOSSARY_MODEL)

    class Meta:
        ordering = ["glossary_term"]
        verbose_name_plural = 'Vocabulary'

    def __unicode__(self):
        return self.glossary_term.__unicode__()


class QuestionAnswer(models.Model):
    activity = models.ForeignKey(Activity)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    appropriate_for = BitField(flags=AUDIENCE_FLAGS, blank=True, null=True)

    def __unicode__(self):
        # truncate
        limit = 44
        return self.question[:limit] + (self.question[limit:] and u'...')


class ResourceItem(models.Model):
    activity = models.ForeignKey(Activity)
    resource = models.ForeignKey(RESOURCE_MODEL, related_name='instructional_resource')

relation_limits = reduce(lambda x, y: x | y, RELATIONS)


class RelationManager(models.Manager):
    def get_content_type(self, content_type):
        qs = self.get_query_set()
        return qs.filter(content_type__name=content_type)

    def get_relation_type(self, relation_type):
        qs = self.get_query_set()
        return qs.filter(relation_type=relation_type)


class ModelRelation(models.Model):
    content_type = models.ForeignKey(
        ContentType, limit_choices_to=relation_limits)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    relation_type = models.CharField("Relation Type",
        max_length="200",
        blank=True,
        null=True,
        choices=RELATION_TYPES,
        help_text="A generic text field to tag a relation, like 'primaryphoto'.")

    objects = RelationManager()

    class Meta:
        abstract = True


class ActivityRelation(ModelRelation):
    activity = models.ForeignKey(Activity)

    def __unicode__(self):
        out = u"%s related to %s" % (self.content_object, self.activity)
        if self.relation_type:
            out += u" as %s" % self.relation_type
        return out


class Lesson(models.Model):  # Publish):
    title = models.CharField(
        max_length=256,
        help_text="""GLOBAL: Use the text variations field to create versions
        for audiences other than the default.""")
    ads_excluded = models.BooleanField(
        default=True,
        help_text="""If unchecked, this field indicates that external ads are
        allowed.""")
    create_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    geologic_time = models.ForeignKey(GeologicTime,
        blank=True,
        null=True)
    id_number = models.CharField(
        max_length=10,
        help_text="""This field is for the internal NG Education ID number.
        This is required for all instructional content.""")
    is_modular = models.BooleanField(
        default=True,
        help_text="""If unchecked, this field indicates that this lesson should
        NOT appear as stand-alone outside of a unit view.""")
    last_updated_date = models.DateTimeField(auto_now=True)
    published = models.BooleanField()
    published_date = models.DateTimeField(
        blank=True,
        null=True)
    secondary_content_types = models.ManyToManyField(AlternateType,
        blank=True,
        null=True)
    slug = models.SlugField(
        unique=True,
        help_text="""The URL slug is auto-generated, but producers should adjust
        it if: a) punctuation in the title causes display errors; and/or b) the
        title changes after the slug has been generated.""")
    subtitle_guiding_question = models.TextField(
        verbose_name="Subtitle or Guiding Question")

  # Directions
    assessment_type = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        choices=ASSESSMENT_TYPES)
    assessment = models.TextField(
        blank=True,
        null=True,
        help_text="""This field is for a new, lesson-level assessment. It is
        not impacted by activity-level assessments.""")

  # Preparation
    materials = models.ManyToManyField(Material,
        blank=True,
        null=True,
        help_text="""This field is for additional, lesson-level materials a
        teacher will need to provide; for example, new materials needed in
        order to conduct the lesson-level assessment. Do not repeat activity-
        specific materials.""")
    other_notes = models.TextField(
        blank=True,
        null=True,
        help_text="""This field has multiple uses, but one possible use is to
        indicate the larger context into which the lesson fits. Example: This
        is lesson 1 in a series of 10 lessons in a unit on Europe.""")
  # Background & Vocabulary
    background_information = models.TextField(
        blank=True,
        null=True,
        help_text="""Producers can either copy/paste background information
        into this field, or click the "import text" link to import background
        information from all activities in this lesson into this field and edit
        them. If you click "import text from activities" and revise/override the
        imported text, note that clicking "import text from activities" again
        will re-set the text back to the imported version.""")
    prior_knowledge = models.TextField(
        blank=True,
        null=True)
    prior_activities = models.ManyToManyField(Activity,
        blank=True,
        null=True)

  # Credits, Sponsors, Partners
    if CREDIT_MODEL:
        credit = models.ForeignKey(CreditModel,
            blank=True,
            null=True,
            help_text="""All activity-level credits will dynamically display in
            the lesson credits, broken out by activity number. Only use this
            field if you need to add additional, lesson-level credits.""")

  # Global Metadata
    appropriate_for = BitField(
        flags=AUDIENCE_FLAGS,
        help_text='''Select the audience(s) for which this content is
        appropriate. Selecting audiences means that a separate audience view of
        the page will exist for those audiences. For a lesson, the only possible
        choices are Teachers and Informal Educators.

        Note that the text you input in this form serves as the default text.
        If you indicate this activity is appropriate for both T/IE audiences,
        you either need to add text variations or the default text must be
        appropriate for for both audiences.''')
    if REPORTING_MODEL:
        reporting_categories = models.ManyToManyField(ReportingModel,
            blank=True,
            null=True)

  # Time and Date Metadata
    eras = models.ManyToManyField(HistoricalEra,
        blank=True,
        null=True)
    relevant_start_date = HistoricalDateField(
        blank=True,
        null=True)
    relevant_end_date = HistoricalDateField(
        blank=True,
        null=True)

    objects = ContentManager()

    @models.permalink
    def get_absolute_url(self):
        return ('lesson-detail', (), {'slug': self.slug})

    def __unicode__(self):
        return strip_tags(self.title)

    class Meta:
        ordering = ["title"]

  # class PublishingMeta:
  #     published_datefield = 'publish_date'

    if RELATION_MODELS:
        def get_related_content_type(self, content_type):
            """
            Get all related items of the specified content type
            """
            return self.lessonrelation_set.filter(
                content_type__name=content_type)

        def get_relation_type(self, relation_type):
            """
            Get all relations of the specified relation type
            """
            return self.lessonrelation_set.filter(
                relation_type__iexact=relation_type)

    def get_activities(self, filter=None):
        """
        filter should be a dictionary for lookups
        """
        if filter is None:
            return [lessonactivity.activity for lessonactivity in self.lessonactivity_set.all()]
        else:
            return [lessonactivity.activity for lessonactivity in self.lessonactivity_set.filter(**filter)]

    def get_accessibility(self, activities=None):
        accessibility_notes = []

        if activities is None:
            activities = self.get_activities()
        for activity in activities:
            accessibility_notes += ul_as_list(activity.accessibility_notes)
        deduped_notes = set(accessibility_notes)
        return list(deduped_notes)

    def get_canonical_page(self):
        for i in range(0, 5):
            if self.appropriate_for.get_bit(i).is_set:
                return '%s?ar_a=%s' % (reverse('lesson-detail', args=[self.slug]), i + 1)

    def get_duration(self, activities=None):
        if activities is None:
            activities = self.get_activities()
        return sum([activity.duration for activity in activities])

    # TODO
    def get_glossary(self):
        pass

    def get_learning_objectives(self):
        # [EDU-2791] Learning Objectives
        ctype = ContentType.objects.get_for_model(Lesson)
        objectiverelations = ObjectiveRelation.objects.filter(
                                        content_type=ctype, object_id=self.id)
        return [objrel.objective.text for objrel in objectiverelations]

    def get_background_information(self, activities=None):
        '''Used by the admin to import text'''
        bg_info = []
        deduped_info = []

        if activities is None:
            activities = self.get_activities()
        for activity in activities:
            bg_info.append(activity.background_information)
        for info in bg_info:
            if info not in deduped_info:
                deduped_info.append(info)
        return deduped_info

    def get_grades(self):
        grades = []

        for activity in self.get_activities():
            grades += activity.grades.all()

        deduped_grades = set(grades)
        return list(deduped_grades)

    def get_grades_and_ages(self):
        grades = Grade.objects.none()

        for activity in self.get_activities():
            grades |= activity.grades.all()

        return (grades.as_grade_range(), grades.as_age_range())

    # copied from education.edu_core.models.BaseGradeMethod
    @property
    def get_grades_html(self):
        return grades_html(self.get_grades())

    def get_materials(self, activities=None):
        materials = self.materials.all()

        if activities is None:
            activities = self.get_activities()
        for activity in activities:
            materials |= activity.materials.all()
        deduped_materials = set(materials)
        return list(deduped_materials)

    def get_other_notes(self, activities=None):
        other_notes = self.other_notes

        if activities is None:
            activities = self.get_activities()
        for activity in activities:
            other_notes += activity.other_notes
        return other_notes

    def get_physical_space(self, activities=None):
        physical_space_types = []

        if activities is None:
            activities = self.get_activities()
        for activity in activities:
            physical_space_types += activity.physical_space_types.all()
        deduped_physical_space_types = set(physical_space_types)
        return list(deduped_physical_space_types)

    def get_required_technology(self, activities=None):
        required_technology = []

        if activities is None:
            activities = self.get_activities()
        for activity in activities:
            for plugin_type in activity.plugin_types.all():
                required_technology += plugin_type
            required_technology += activity.tech_setup_types.all()
        deduped_technology = set(required_technology)
        return list(deduped_technology)

    def get_setup(self, activities=None):
        setup = []

        if activities is None:
            activities = self.get_activities()
        for activity in activities:
            setup += ul_as_list(activity.setup)
        deduped_setup = set(setup)
        return list(deduped_setup)

    def get_subjects(self, activities=None):
        subjects = []

        if activities is None:
            activities = self.get_activities()
        for activity in activities:
            for subject in activity.subjects.all():
                subjects.append(subject)
        deduped_subjects = set(subjects)
        return list(deduped_subjects)

    def get_key_image(self):
        ctype = ContentType.objects.get(app_label='core_media', model='ngphoto')
        lr = self.get_related_content_type(ctype.name)
        if len(lr) > 0:
            return lr[0].content_object
        else:
            return None

    def key_image(self):
        image = self.get_key_image()
        if image:
            return image.thumbnail_url()
        else:
            return None

    def thumbnail_html(self):
        key_image = self.key_image()
        if key_image:
            return '<img src="%s"/>' % self.key_image()
        else:
            return None


class LessonRelation(ModelRelation):
    lesson = models.ForeignKey(Lesson)

    def __unicode__(self):
        out = u"%s related to %s" % (self.content_object, self.lesson)
        if self.relation_type:
            out += u" as %s" % self.relation_type
        return out


class LessonActivity(models.Model):
    lesson = models.ForeignKey(Lesson)
    activity = models.ForeignKey(Activity)
    transition_text = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('order',)
        verbose_name_plural = 'Activities'


class IdeaCategory(models.Model):
    """
    Idea-specific categories
    """
    create_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    # Overview
    appropriate_for = BitField(
        flags=AUDIENCE_FLAGS,
        help_text='''Select the audience(s) for which this content is
        appropriate.''')
    title = models.CharField(
        max_length=256)
    slug = models.SlugField(
        unique=True,
        help_text="""The URL slug is auto-generated, but producers should adjust
        it if: a) punctuation in the title causes display errors; and/or b) the
        title changes after the slug has been generated.""")
    subtitle_guiding_question = models.TextField(
        verbose_name="Subtitle or Guiding Question",
        blank=True,
        null=True)
    if KeyImageModel:
        key_image = models.ForeignKey(KeyImageModel)
    description = models.TextField()
    id_number = models.CharField(
        max_length=10,
        null=True,
        help_text="""This field is for the internal NG Education ID number. This
        is required for all instructional content.""")
    # Content Detail
    content_body = models.TextField()
    # Credits, Sponsors, Partners
    if CREDIT_MODEL:
        credit = models.ForeignKey(CreditModel,
            blank=True,
            null=True)
    # Licensing
    license_name = models.ForeignKey(GrantedLicense,
        blank=True,
        null=True,
        default=DEFAULT_LICENSE)
    # Global Metadata
    secondary_content_types = models.ManyToManyField(AlternateType,
        blank=True,
        null=True)
    if REPORTING_MODEL:
        reporting_categories = models.ManyToManyField(ReportingModel,
            blank=True,
            null=True)
    # Content Related Metadata
    subjects = models.ManyToManyField(Subject,
        blank=True,
        null=True,
        limit_choices_to={'parent__isnull': False},
        verbose_name="Subjects and Disciplines")
    grades = models.ManyToManyField(Grade,
        blank=True,
        null=True)
    # Time and Date Metadata
    eras = models.ManyToManyField(HistoricalEra,
        blank=True,
        null=True)
    geologic_time = models.ForeignKey(GeologicTime,
        blank=True,
        null=True)
    relevant_start_date = HistoricalDateField(
        blank=True,
        null=True)
    relevant_end_date = HistoricalDateField(
        blank=True,
        null=True)
    # Schedule
    published = models.BooleanField()
    published_date = models.DateTimeField(
        blank=True,
        null=True)

    objects = ContentManager()

    class Meta:
        verbose_name_plural = 'Idea categories'

    def __unicode__(self):
        return self.title

    def appropriate_display(self):
        return bitfield_display(self.appropriate_for)
    appropriate_display.allow_tags = True

    def thumbnail_html(self):
        if self.key_image:
            return '<img src="%s"/>' % self.key_image.thumbnail_url()
        else:
            return None


class Idea(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    # Overview
    appropriate_for = BitField(
        flags=AUDIENCE_FLAGS,
        help_text='''Select the audience(s) for which this content is
        appropriate.''')
    title = models.CharField(
        max_length=256,
        null=True)
    if KeyImageModel:
        key_image = models.ForeignKey(KeyImageModel)
    id_number = models.CharField(
        max_length=10,
        null=True,
        help_text="""This field is for the internal NG Education ID number. This
        is required for all instructional content.""")
    # Content Detail
    content_body = models.TextField()

    def appropriate_display(self):
        return bitfield_display(self.appropriate_for)
    appropriate_display.allow_tags = True

    def get_categories(self):
        return [ci.category.title for ci in CategoryIdea.objects.filter(idea=self)]

    def thumbnail_html(self):
        if self.key_image:
            return '<img src="%s"/>' % self.key_image.thumbnail_url()
        else:
            return None


class CategoryIdea(models.Model):
    category = models.ForeignKey(IdeaCategory, null=True)
    idea = models.ForeignKey(Idea, null=True)

    def __unicode__(self):
        return self.category.title


class IdeaCategoryRelation(ModelRelation):
    idea_category = models.ForeignKey(IdeaCategory)

    def __unicode__(self):
        out = u"%s related to %s" % (self.content_object, self.idea_category)
        if self.relation_type:
            out += u" as %s" % self.relation_type
        return out


pre_delete.connect(delete_listener, sender=Activity)

#register(Activity)
#register(Lesson)
