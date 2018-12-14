import json

from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.utils.html import strip_tags

from audience.settings import AUDIENCE_FLAGS
from bitfield import BitField
from edumetadata.models import (AlternateType, GeologicTime, Grade,
                                HistoricalEra, Subject)
from edumetadata.fields import HistoricalDateField
from concepts.models import delete_listener
from concepts.managers import ConceptManager

from curricula.settings import (ASSESSMENT_TYPES, RELATION_MODELS,
                                PEDAGOGICAL_PURPOSE_TYPE_CHOICES,
                                INTERNET_ACCESS_TYPES)
from curricula.utils import truncate
from taxonomy.managers import TaxonomyTaggableManager

__all__ = ('Activity', 'ResourceItem', 'Vocabulary', 'QuestionAnswer')

from core_media.models import NGPhoto  # NOQA
from credits.models import CreditGroup  # NOQA


class ActivityManager(models.Manager):
    def get_published(self):
        qs = self.get_queryset()
        return qs.filter(published=True)


class Activity(models.Model):
    accessibility_notes = models.TextField(
        blank=True, null=True)
    appropriate_for = BitField(
        flags=AUDIENCE_FLAGS,
        help_text='''Select the audience(s) for which this content is
        appropriate. Selecting audiences means that a separate audience view of
        the page will exist for those audiences.

        Note that the text you input in this form serves as the default text.
        If you indicate this activity is appropriate for multiple audiences,
        you either need to add text variations or the default text must be
        appropriate for those audiences.''')
    assessment = models.TextField(
        blank=True, null=True)
    assessment_type = models.CharField(
        max_length=15,
        blank=True, null=True,
        choices=ASSESSMENT_TYPES)
    background_information = models.TextField(
        blank=True, null=True,
        help_text="""If this activity is part of an already-created lesson and
        you update the background information, you must also make the same
        change in lesson for this field.""")
    concepts = ConceptManager()
    create_date = models.DateTimeField(auto_now_add=True)
    credit = models.ForeignKey(
        CreditGroup,
        blank=True, null=True)
    description = models.TextField()
    directions = models.TextField(
        blank=True, null=True)
    duration = models.IntegerField(verbose_name="Duration Minutes")
    eras = models.ManyToManyField(
        HistoricalEra,
        blank=True, )
    extending_the_learning = models.TextField(
        blank=True, null=True)
    geologic_time = models.ForeignKey(
        GeologicTime,
        blank=True, null=True)
    grades = models.ManyToManyField(
        Grade,
        blank=True, )
    grouping_types = models.ManyToManyField(
        'curricula.GroupingType',
        blank=True, )
    id_number = models.CharField(
        max_length=10,
        help_text="This field is for the internal NG Education ID number. "
        "This is required for all instructional content.")
    internet_access_type = models.IntegerField(
        blank=True, null=True,
        choices=INTERNET_ACCESS_TYPES)
    is_modular = models.BooleanField(
        default=True,
        help_text="""If unchecked, this field indicates that this activity
        should not appear as stand-alone outside of a lesson view.""")
    key_image = models.ForeignKey(
        NGPhoto,
        blank=True, null=True,
        on_delete=models.SET_NULL)
    last_updated_date = models.DateTimeField(auto_now=True)
    learner_groups = models.ManyToManyField(
        'curricula.LearnerGroup',
        blank=True, )
    learning_objective_set = GenericRelation('curricula.ObjectiveRelation')
    lessons = models.ManyToManyField(
        'curricula.Lesson',
        through='curricula.LessonActivity')
    materials = models.ManyToManyField(
        'curricula.Material',
        blank=True, )
    notes_on_readability_score = models.TextField(
        blank=True, null=True,
        help_text="""Use this internal-use only field to record any details
        related to the readability of reading passages, such as those on
        handouts. Include Lexile score, grade-level equivalent, and any
        criteria used to determine why a higher score is acceptable
        (proper nouns, difficult vocabulary, etc.).""")
    other_notes = models.TextField(
        blank=True, null=True)
    pedagogical_purpose_type = models.SmallIntegerField(
        blank=True, null=True,
        choices=PEDAGOGICAL_PURPOSE_TYPE_CHOICES)
    physical_space_types = models.ManyToManyField(
        'curricula.PhysicalSpaceType',
        blank=True, )
    plugin_types = models.ManyToManyField(
        'curricula.PluginType',
        blank=True, )
    prior_activities = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        verbose_name="Recommended Prior Activities")
    prior_knowledge = models.TextField(
        blank=True, null=True)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(
        blank=True, null=True)
    relevant_start_date = HistoricalDateField(
        blank=True, null=True)
    relevant_end_date = HistoricalDateField(
        blank=True, null=True)
    resource_items = models.ManyToManyField(
        'resource_carousel.ExternalResource',
        through='curricula.ResourceItem')
    secondary_content_types = models.ManyToManyField(
        AlternateType,
        blank=True, )
    setup = models.TextField(
        blank=True, null=True)
    skills = models.ManyToManyField(
        'curricula.Skill',
        blank=True,
        limit_choices_to={'children__isnull': True})
    slug = models.SlugField(
        unique=True,
        max_length=100,
        help_text="""The URL slug is auto-generated, but producers should adjust
        it if: a) punctuation in the title causes display errors; and/or b) the
        title changes after the slug has been generated.""")
    standards = models.ManyToManyField(
        'curricula.Standard',
        blank=True, )
    subjects = models.ManyToManyField(
        Subject,
        blank=True,
        # limit_choices_to={'parent__isnull': False},
        verbose_name="Subjects and Disciplines")
    subtitle_guiding_question = models.TextField(
        verbose_name="Subtitle or Guiding Question")
    teaching_approaches = models.ManyToManyField(
        'curricula.TeachingApproach',
        blank=True, )
    teaching_method_types = models.ManyToManyField(
        'curricula.TeachingMethodType',
        blank=True, )
    tech_setup_types = models.ManyToManyField(
        'curricula.TechSetupType',
        blank=True, )
    tips = models.ManyToManyField(
        'curricula.Tip',
        blank=True,
        verbose_name="Tips & Modifications")
    title = models.CharField(
        max_length=256,
        help_text="""GLOBAL: Use the text variations field to create versions
        for audiences other than the default.""")
    vocabulary = models.ManyToManyField(
        'reference.GlossaryTerm',
        through='curricula.Vocabulary')
    archived = models.BooleanField(default=False)

    taxonomy = TaxonomyTaggableManager()
    objects = ActivityManager()

    @models.permalink
    def get_absolute_url(self):
        return ('activity-detail', (), {'slug': self.slug})

    def __unicode__(self):
        return strip_tags(self.title)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = 'Activities'
        app_label = 'curricula'

    @property
    def prior_knowledge_items(self):
        return json.loads(self.prior_knowledge)

    def get_canonical_page(self):
        """
        Return the URL to the first audience set
        """
        return reverse('activity-detail', args=[self.slug])

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

    def get_credit_details(self):
        credit_details = OrderedDict()

        if self.credit and self.credit.credit_details:
            for detail in self.credit.credit_details.order_by(
                    'credit_category__order'):

                if detail.credit_category not in credit_details:
                    credit_details[detail.credit_category] = []

                credit_details[detail.credit_category].append(detail.entity)

        return credit_details

    if RELATION_MODELS:
        def get_related_content_type(self, content_type):
            """
            Get all related items of the specified content type
            """
            return self.relations.filter(
                content_type__model=content_type)

        def get_relation_type(self, relation_type):
            """
            Get all relations of the specified relation type
            """
            return self.relations.filter(
                relation_type__iexact=relation_type)

        def get_content_object(self, field):
            app_label, model = field[1].split('.')
            ctype = ContentType.objects.get_by_natural_key(app_label=app_label, model=model.lower())
            ar = self.get_related_content_type(ctype.name)
            if len(ar) > 0:
                return ar[0].content_object
            else:
                return None

        def get_key_image(self):
            from curricula.settings import KEY_IMAGE
            return self.get_content_object(KEY_IMAGE)


class Vocabulary(models.Model):
    activity = models.ForeignKey(Activity, related_name="+")
    glossary_term = models.ForeignKey('reference.GlossaryTerm')

    class Meta:
        ordering = ["glossary_term"]
        verbose_name_plural = 'Vocabulary'
        app_label = 'curricula'

    def __unicode__(self):
        return self.glossary_term.__unicode__()


class QuestionAnswer(models.Model):
    activity = models.ForeignKey(Activity)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    appropriate_for = BitField(flags=AUDIENCE_FLAGS, blank=True, null=True)

    class Meta:
        app_label = 'curricula'
        verbose_name = u'Question and Answer'
        verbose_name_plural = u'Questions and Answers'

    def __unicode__(self):
        return truncate(self.question)


class ResourceItem(models.Model):
    activity = models.ForeignKey(Activity, related_name="+")
    resource = models.ForeignKey(
        'resource_carousel.ExternalResource',
        related_name='instructional_resource')

    class Meta:
        app_label = 'curricula'


def aggregate_signaler(sender, instance, created, raw, using, *args, **kwargs):
    for lesson in instance.lessons.all():
        lesson.save()

pre_delete.connect(delete_listener, sender=Activity)
post_save.connect(aggregate_signaler, sender=Activity)
