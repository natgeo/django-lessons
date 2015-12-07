from django.db import models
from django.db.models.signals import pre_delete
from django.utils.html import strip_tags

from audience.settings import AUDIENCE_FLAGS
from bitfield import BitField
from concepts.models import delete_listener
from edumetadata.models import (AlternateType, GeologicTime, Grade,
                                HistoricalEra, Subject)
from edumetadata.fields import HistoricalDateField

from curricula.settings import RELATION_MODELS

from core_media.models import NGPhoto  # NOQA
from credits.models import CreditGroup  # NOQA
from taxonomy.managers import TaxonomyTaggableManager

__all__ = ('Unit', 'UnitLesson')


class UnitManager(models.Manager):
    def get_published(self):
        qs = self.get_queryset()
        return qs.filter(published=True)


class Unit(models.Model):
    # Unit-specific fields
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
    credit = models.ForeignKey(
        CreditGroup,
        blank=True,
        null=True)
    description = models.TextField()
    id_number = models.CharField(
        max_length=10,
        help_text="""This field is for the internal NG Education ID number.
        This is required for all instructional content.""")
    key_image = models.ForeignKey(NGPhoto)
    lessons = models.ManyToManyField(
        'curricula.Lesson',
        through='curricula.UnitLesson')
    overview = models.TextField()
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(
        blank=True,
        null=True)
    secondary_content_types = models.ManyToManyField(
        AlternateType,
        blank=True)
    slug = models.SlugField(
        unique=True,
        max_length=100,
        help_text="""The URL slug is auto-generated, but producers should adjust
        it if: a) punctuation in the title causes display errors; and/or b) the
        title changes after the slug has been generated.""")
    subtitle = models.TextField(
        blank=True,
        null=True)
    title = models.CharField(
        max_length=256,
        verbose_name="Unit Title",
        help_text="""GLOBAL: Use the text variations field to create versions
        for audiences other than the default.""")
    last_updated_date = models.DateTimeField(auto_now=True)

    # Read-only fields aggregated from lessons/activities
    eras = models.ManyToManyField(
        HistoricalEra,
        blank=True)
    geologic_time = models.ForeignKey(
        GeologicTime,
        blank=True,
        null=True)
    grades = models.ManyToManyField(
        Grade,
        blank=True)
    relevant_start_date = HistoricalDateField(
        blank=True,
        null=True)
    relevant_end_date = HistoricalDateField(
        blank=True,
        null=True)
    subjects = models.ManyToManyField(
        Subject,
        blank=True,
        limit_choices_to={'parent__isnull': False})
    archived = models.BooleanField(default=False)

    taxonomy = TaxonomyTaggableManager()
    objects = UnitManager()

    class Meta:
        app_label = 'curricula'
        ordering = ['title']

    def save(self, *args, **kwargs):
        """
        Roll up all pertinent metadata
        """
        if self.id is None:
            super(Unit, self).save(*args, **kwargs)
            kwargs['force_update'] = True
            kwargs['force_insert'] = False

        if self.lessons.count() == 0:
            return
        agg_activities = self.aggregate_activity_attr

        rsd = agg_activities('relevant_start_date')
        if rsd:
            self.relevant_start_date = min(rsd)
        red = agg_activities('relevant_end_date')
        if red:
            self.relevant_end_date = max(red)
        gt = agg_activities('geologic_time')
        if gt:
            self.geologic_time = min(gt)
        super(Unit, self).save(*args, **kwargs)
        self._sync_m2m(self.eras, agg_activities('eras'))
        self._sync_m2m(self.subjects, agg_activities('subjects', ignore_own=True))
        self._sync_m2m(self.grades, agg_activities('grades', ignore_own=True))

    def _sync_m2m(self, attr, new_set):
        """
        Synchronize the objects m2m objects in <attr> with the objects in <new_set>
        """
        current = set(attr.all())
        newer = set(new_set)
        to_remove = current - newer
        to_add = newer - current
        if to_add:
            attr.add(*list(to_add))
        if to_remove:
            attr.remove(*list(to_remove))

    def __unicode__(self):
        return strip_tags(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('unit-detail', (), {'slug': self.slug})

    def aggregate_activity_attr(self, attr_name, ignore_own=False):
        """
        Generic method to gather up the activities and deduplicate a specific
        attribute

        Can pass a list of IDs or a QuerySet
        """
        # from itertools import chain
        from curricula.models import Activity
        import operator

        # To find out if the attribute is a m2m or a regular field, we test for
        # attribute on the uninstantiated class. m2m Descriptors will be there,
        # regular fields will not
        if hasattr(Activity, attr_name):
            if hasattr(getattr(Activity, attr_name), 'through'):
                is_m2m = True
                is_fk = False
            else:
                is_fk = True
                is_m2m = False
        else:
            is_m2m = is_fk = False
        qset = reduce(operator.or_, [x.activities.all() for x in self.lessons.prefetch_related('activities')])
        if is_m2m:
            qset = qset.prefetch_related(attr_name)
            biglist = reduce(operator.or_, [getattr(x, attr_name).all() for x in qset])
            unique = set(biglist)
        elif is_fk:
            qset = qset.select_related(attr_name)
            unique = set([getattr(x, attr_name) for x in qset])
        else:
            unique = set(qset.values_list(attr_name, flat=True))
            if hasattr(self, attr_name) and not ignore_own:
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
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('order', )
        verbose_name_plural = 'UnitLessons'
        app_label = 'curricula'

pre_delete.connect(delete_listener, sender=Unit)
