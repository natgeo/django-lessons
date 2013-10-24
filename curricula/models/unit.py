from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete
from django.utils.html import strip_tags

from audience.settings import AUDIENCE_FLAGS
from bitfield import BitField
from concepts.models import delete_listener  #, Concept, ConceptItem
from edumetadata.models import (GeologicTime, Grade,
                                 HistoricalEra, Subject)
from edumetadata.fields import HistoricalDateField

from curricula.settings import (
                    RELATION_MODELS,
                      CREDIT_MODEL,
                      REPORTING_MODEL, KEY_IMAGE
                      )

__all__ = ('Unit', 'UnitLesson')

if KEY_IMAGE and len(KEY_IMAGE) > 0:
    KeyImageModel = KEY_IMAGE[1]
else:
    KeyImageModel = None


class UnitManager(models.Manager):
    def get_published(self):
        qs = self.get_query_set()
        return qs.filter(published=True)


class Unit(models.Model):
    # Global Metadata
    appropriate_for = BitField(
        flags=AUDIENCE_FLAGS,
        help_text='''Select the audience(s) for which this content is
        appropriate. Selecting audiences means that a separate audience view of
        the page will exist for those audiences.

        Note that the text you input in this form serves as the default text.
        If you indicate this unit is appropriate for multiple audiences,
        you either need to add text variations or the default text must be
        appropriate for those audiences.''')
    create_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        unique=True,
        max_length=100,
        help_text="""The URL slug is auto-generated, but producers should adjust
        it if: a) punctuation in the title causes display errors; and/or b) the
        title changes after the slug has been generated.""")
    title = models.CharField(
        max_length=256,
        verbose_name="Unit Title",
        help_text="""GLOBAL: Use the text variations field to create versions
        for audiences other than the default.""")
    subtitle = models.TextField(
        blank=True,
        null=True)
    if KeyImageModel:
        key_image = models.ForeignKey(KeyImageModel)
    description = models.TextField()
    overview = models.TextField()
    id_number = models.CharField(
        max_length=10,
        help_text="""This field is for the internal NG Education ID number.
        This is required for all instructional content.""")
    grades = models.ManyToManyField(Grade,
        blank=True,
        null=True)
    subjects = models.ManyToManyField(Subject,
        blank=True,
        null=True,
        limit_choices_to={'parent__isnull': False})
    # Credits, Sponsors, Partners
    if CREDIT_MODEL:
        credit = models.ForeignKey(CREDIT_MODEL,
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
    # Schedule Metadata
    published = models.BooleanField()
    published_date = models.DateTimeField(
        blank=True,
        null=True)

    lessons = models.ManyToManyField('curricula.Lesson',
        through='curricula.UnitLesson')
    objects = UnitManager()

    class Meta:
        app_label = 'curricula'
        ordering = ['title']

    def save(self, *args, **kwargs):
        """
        Roll up all pertinent metadata
        """


    def __unicode__(self):
        return strip_tags(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('unit-detail', (), {'slug': self.slug})

    def aggregate_activity_attr(self, attr_name):
        """
        Generic method to gather up the activities and deduplicate a specific attribute

        Can pass a list of IDs or a QuerySet
        """
        # from itertools import chain
        from curricula.models import Activity
        import operator

        # To find out if the attribute is a m2m or a regular field, we test for
        # attribute on the uninstantiated class. m2m Descriptors will be there,
        # regular fields will not
        is_m2m = hasattr(Activity, attr_name)
        qset = reduce(operator.or_, [x.activities.all() for x in self.lessons.prefetch_related('activities')])
        if is_m2m:
            qset = qset.prefetch_related(attr_name)
            biglist = reduce(operator.or_, [getattr(x, attr_name).all() for x in qset])
            unique = set(biglist)
        else:
            unique = set(qset.values_list(attr_name, flat=True))
            if hasattr(self, attr_name):
                unique.add(getattr(self, attr_name))

        return list(unique)

    def get_grades_and_ages(self):
        return self.grades.all().as_grade_age_range()

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

    def get_vocabulary(self):
        return self.aggregate_activity_attr('vocabulary')


class UnitLesson(models.Model):
    unit = models.ForeignKey('curricula.Unit')
    lesson = models.ForeignKey('curricula.Lesson')
    transition_text = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True) #, verbose_name='Sort Order')

    class Meta:
        ordering = ('order', )
        verbose_name_plural = 'UnitLessons'
        app_label = 'curricula'

pre_delete.connect(delete_listener, sender=Unit)
