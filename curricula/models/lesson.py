from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete
from django.utils.html import strip_tags

from audience.settings import AUDIENCE_FLAGS
from bitfield import BitField
from edumetadata.models import (AlternateType, GeologicTime, Grade,
                                 HistoricalEra, Subject)
from edumetadata.fields import HistoricalDateField
from concepts.models import delete_listener  #, Concept, ConceptItem
from concepts.managers import ConceptManager

from curricula.utils import ul_as_list
from curricula.settings import (ASSESSMENT_TYPES,
                    RELATION_MODELS,
                      CREDIT_MODEL,
                      REPORTING_MODEL
                      )

__all__ = ('Lesson', 'LessonActivity',)


class LessonManager(models.Manager):
    def get_published(self):
        qs = self.get_query_set()
        return qs.filter(published=True)

class Lesson(models.Model):
    # Lesson-specific fields
    activities = models.ManyToManyField('curricula.Activity',
        through='curricula.LessonActivity')
    ads_excluded = models.BooleanField(
        default=True,
        help_text="""If unchecked, this field indicates that external ads are
        allowed.""")
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
    background_information = models.TextField(
        blank=True,
        null=True,
        help_text="""Producers can either copy/paste background information
        into this field, or click the "import text" link to import background
        information from all activities in this lesson into this field and edit
        them. If you click "import text from activities" and revise/override the
        imported text, note that clicking "import text from activities" again
        will re-set the text back to the imported version.""")
    create_date = models.DateTimeField(auto_now_add=True)
    if CREDIT_MODEL:
        credit = models.ForeignKey(CREDIT_MODEL,
            blank=True,
            null=True,
            help_text="""All activity-level credits will dynamically display in
            the lesson credits, broken out by activity number. Only use this
            field if you need to add additional, lesson-level credits.""")
    concepts = ConceptManager()
    description = models.TextField()
    title = models.CharField(
        max_length=256,
        help_text="""GLOBAL: Use the text variations field to create versions
        for audiences other than the default.""")
    id_number = models.CharField(
        max_length=10,
        help_text="""This field is for the internal NG Education ID number.
        This is required for all instructional content.""")
    is_modular = models.BooleanField(
        default=True,
        help_text="""If unchecked, this field indicates that this lesson should
        NOT appear as stand-alone outside of a unit view.""")
    last_updated_date = models.DateTimeField(auto_now=True)
    materials = models.ManyToManyField('curricula.Material',
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
    prior_lessons = models.ManyToManyField('self',
        symmetrical=False,
        blank=True,
        null=True)
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
    units = models.ManyToManyField('curricula.Unit',
        through='curricula.UnitLesson')


  # Read-only fields aggregated from Activities
    eras = models.ManyToManyField(HistoricalEra,
        blank=True,
        null=True)
    prior_knowledge = models.TextField(
        blank=True,
        null=True)
    if REPORTING_MODEL:
        reporting_categories = models.ManyToManyField(REPORTING_MODEL,
            blank=True,
            null=True)
    relevant_start_date = HistoricalDateField(
        blank=True,
        null=True)
    relevant_end_date = HistoricalDateField(
        blank=True,
        null=True)
    geologic_time = models.ForeignKey(GeologicTime,
        blank=True,
        null=True)

    objects = LessonManager()

    @models.permalink
    def get_absolute_url(self):
        return ('lesson-detail', (), {'slug': self.slug})

    def get_canonical_page(self):
        for i in range(0, 5):
            if self.appropriate_for.get_bit(i).is_set:
                return '%s?ar_a=%s' % (reverse('lesson-detail', args=[self.slug]), i + 1)

    def __unicode__(self):
        return strip_tags(self.title)

    class Meta:
        ordering = ["title"]
        app_label = 'curricula'

    if RELATION_MODELS:
        def get_related_content_type(self, content_type):
            """
            Get all related items of the specified content type
            """
            return self.relations.filter(
                content_type__name=content_type)

        def get_relation_type(self, relation_type):
            """
            Get all relations of the specified relation type
            """
            return self.relations.filter(
                relation_type__iexact=relation_type)

    ## Activity Aggregations

    def aggregate_activity_attr(self, activities, attr_name):
        """
        Generic method to gather up the activities and deduplicate a specific attribute

        Can pass a list of IDs or a QuerySet
        """
        if not activities:
            return []
        from django.db.models.query import QuerySet
        from itertools import chain
        from curricula.models import Activity

        # To find out if the attribute is a m2m or a regular field, we test for
        # attribute on the Uninstantiated class. m2m Descriptors will be there,
        # regular fields will not
        is_m2m = hasattr(Activity, attr_name)
        if isinstance(activities, (list, tuple)):
            if isinstance(activities[0], Activity):
                # We have a bunch of individual Activities. Hate to do this,
                # but we need a QuerySet
                activities = [a.pk for a in activities]
            qset = Activity.objects.filter(pk__in=activities)
        elif isinstance(activities, QuerySet):
            qset = activities
        else:
            return []
        if is_m2m:
            qset = qset.prefetch_related(attr_name)
            listoflists = [getattr(x, attr_name).all() for x in qset]
            if hasattr(self, attr_name):
                listoflists.append(getattr(self, attr_name).all())
            biglist = chain(*listoflists)
            unique = set(biglist)
        else:
            unique = set(qset.values_list(attr_name, flat=True))
            if hasattr(self, attr_name):
                unique.add(getattr(self, attr_name))

        return list(unique)


    def get_accessibility(self, activities=None):
        activities = activities or self.activities.all()
        accessibility_notes = [ul_as_list(activity.accessibility_notes) for activity in activities]
        deduped_notes = set(accessibility_notes)
        return list(deduped_notes)

    def get_duration(self, activities=None):
        activities = activities or self.activities.all()
        return sum([activity.duration for activity in activities])

    def get_background_information(self, activities=None):
        '''Used by the admin to import text'''
        activities = activities or self.activities.all()
        bg_info = [activity.background_information for activity in activities]
        deduped_info = set(bg_info)
        return list(deduped_info)

    def get_grades(self):
        return self.aggregate_activity_attr(self.activities.all(), 'grades')

    def get_grades_and_ages(self):
        grades = Grade.objects.none()

        for activity in self.activities.all().prefetch_related('grades'):
            grades |= activity.grades.all()

        return (grades.as_grade_range(), grades.as_age_range())

    def get_materials(self, activities=None):
        activities = activities or self.activities.all()
        return self.aggregate_activity_attr(activities, 'materials')

    def get_other_notes(self, activities=None):
        activities = activities or self.activities.all()
        return self.aggregate_activity_attr(activities, 'other_notes')

    def get_physical_space(self, activities=None):
        activities = activities or self.activities.all()
        return self.aggregate_activity_attr(activities, 'physical_space_types')

    def get_required_technology(self, activities=None):
        activities = activities or self.activities.all()
        plugin_types = self.aggregate_activity_attr(activities, 'plugin_types')
        tech_setup_types = self.aggregate_activity_attr(activities, 'tech_setup_types')
        return plugin_types + tech_setup_types

    def get_setup(self, activities=None):
        activities = activities or self.activities.all()
        setup = [ul_as_list(activity.setup) for activity in activities]
        deduped_setup = set(setup)
        return list(deduped_setup)

    def get_subjects(self, activities=None):
        activities = activities or self.activities.all()
        return self.aggregate_activity_attr(activities, 'subjects')

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


class LessonActivity(models.Model):
    lesson = models.ForeignKey('curricula.Lesson')
    activity = models.ForeignKey('curricula.Activity')
    transition_text = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('order',)
        verbose_name_plural = 'LessonActivities'
        app_label = 'curricula'


pre_delete.connect(delete_listener, sender=Lesson)
