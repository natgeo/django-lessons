from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Avg
from django.db import models
from django.db.models.signals import pre_delete

from audience.settings import AUDIENCE_FLAGS
from bitfield import BitField
from edumetadata.models import (AlternateType, GeologicTime, Grade,
                                 HistoricalEra, Subject)
from edumetadata.fields import HistoricalDateField
from concepts.models import delete_listener, Concept, ConceptItem
from licensing.models import GrantedLicense
from acknowledge.models import Entity
from core_media.models import NGPhoto  # NOQA
from credits.models import CreditGroup  # NOQA

from curricula.settings import RELATION_MODELS, DEFAULT_LICENSE

__all__ = ('IdeaCategory', 'Idea', 'CategoryIdea')


class IdeaManager(models.Manager):
    def get_published(self):
        qs = self.get_queryset()
        return qs.filter(published=True)


class IdeaCategory(models.Model):
    """
    Idea-specific categories
    """
    appropriate_for = BitField(
        flags=AUDIENCE_FLAGS,
        help_text='''Select the audience(s) for which this content is
        appropriate.''')
    content_body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    credit = models.ForeignKey(CreditGroup,
        blank=True,
        null=True)
    description = models.TextField()
    eras = models.ManyToManyField(HistoricalEra,
        blank=True)
    geologic_time = models.ForeignKey(GeologicTime,
        blank=True,
        null=True)
    grades = models.ManyToManyField(Grade,
        blank=True)
    id_number = models.CharField(
        max_length=10,
        null=True,
        help_text="""This field is for the internal NG Education ID number. This
        is required for all instructional content.""")
    key_image = models.ForeignKey(
        NGPhoto,
        blank=True, null=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    license_name = models.ForeignKey(GrantedLicense,
        blank=True,
        null=True,
        default=DEFAULT_LICENSE)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(
        blank=True,
        null=True)
    relevant_start_date = HistoricalDateField(
        blank=True,
        null=True)
    relevant_end_date = HistoricalDateField(
        blank=True,
        null=True)
    secondary_content_types = models.ManyToManyField(AlternateType,
        blank=True)
    slug = models.SlugField(
        unique=True,
        help_text="""The URL slug is auto-generated, but producers should adjust
        it if: a) punctuation in the title causes display errors; and/or b) the
        title changes after the slug has been generated.""")
    subjects = models.ManyToManyField(Subject,
        blank=True,
        limit_choices_to={'parent__isnull': False},
        verbose_name="Subjects and Disciplines")
    subtitle_guiding_question = models.TextField(
        verbose_name="Subtitle or Guiding Question",
        blank=True,
        null=True)
    title = models.CharField(
        max_length=256)
    archived = models.BooleanField(default=False)

    objects = IdeaManager()

    class Meta:
        verbose_name_plural = 'Idea categories'
        app_label = 'curricula'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('idea-detail', (), {'slug': self.slug})

    def _concept_items(self):
        idea_ids = self.ideas.all().values_list('id', flat=True)
        ct1 = ContentType.objects.get_for_model(self)
        ct2 = ContentType.objects.get_for_model(Idea)

        q1 = Q(content_type=ct1, object_id=self.id)
        q2 = Q(content_type=ct2, object_id__in=idea_ids)

        return ConceptItem.objects.filter(q1 | q2).filter(weight__gt=0)

    def get_concepts(self):
        items = self._concept_items()

        concepts = list(items.values('tag').annotate(avg_weight=Avg('weight')).order_by('tag').distinct())
        con_ids = [x['tag'] for x in concepts]
        tags = Concept.objects.filter(id__in=con_ids).values('id', 'name', 'url')
        tag_dict = dict((x['id'], x) for x in tags)
        for tag in concepts:
            tag['tag'] = tag_dict[tag['tag']]
            tag['weight'] = int(round(tag['avg_weight'] / 5.0) * 5)

        return concepts

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

    def more_like_this(self, ar_a):
        ct1 = ContentType.objects.get_for_model(self)
        ct2 = ContentType.objects.get_for_model(Idea)

        q1 = Q(content_type=ct1)
        q2 = Q(content_type=ct2)
        concepts = self.tags

        items = ConceptItem.objects.filter(q1 | q2)
        items = items.filter(tag__in=concepts, weight__gt=0)
        categories = [item.content_object for item in items.filter(content_type=ct1)]
        for item in items.filter(content_type=ct2):
            if item.content_object:
                categories += item.content_object._get_categories()

        categories = list(set(categories))
        categories.remove(self)
        return categories

    @property
    def tags(self):
        item_ids = self._concept_items().values_list('tag', flat=True)

        return Concept.objects.filter(id__in=item_ids)


class Idea(models.Model):
    appropriate_for = BitField(
        flags=AUDIENCE_FLAGS,
        help_text='''Select the audience(s) for which this content is
        appropriate.''')
    categories = models.ManyToManyField(IdeaCategory,
        through='CategoryIdea',
        related_name='ideas')
    content_body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    id_number = models.CharField(
        max_length=10,
        null=True,
        help_text="""This field is for the internal NG Education ID number. This
        is required for all instructional content.""")
    key_image = models.ForeignKey(NGPhoto,
        blank=True,
        null=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(
        Entity,
        related_name='ideas',
        null=True, blank=True)
    title = models.CharField(
        max_length=256,
        null=True)

    def __unicode__(self):
        return self.title

    def _get_categories(self):
        return [ci.category for ci in CategoryIdea.objects.filter(idea=self)]

    def get_categories(self):
        return [ic.title for ic in self._get_categories()]

    class Meta:
        app_label = 'curricula'


class CategoryIdea(models.Model):
    category = models.ForeignKey(IdeaCategory, null=True)
    idea = models.ForeignKey(Idea, null=True)

    class Meta:
        app_label = 'curricula'

    def __unicode__(self):
        return self.category.title

pre_delete.connect(delete_listener, sender=IdeaCategory)
