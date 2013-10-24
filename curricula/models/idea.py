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

from curricula.settings import (
                    RELATION_MODELS,
                      CREDIT_MODEL, DEFAULT_LICENSE,
                      REPORTING_MODEL, KEY_IMAGE
                      )

__all__ = ('IdeaCategory', 'Idea', 'CategoryIdea')

if KEY_IMAGE and len(KEY_IMAGE) > 0:
    KeyImageModel = KEY_IMAGE[1]
else:
    KeyImageModel = None


class IdeaManager(models.Manager):
    def get_published(self):
        qs = self.get_query_set()
        return qs.filter(published=True)


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
        credit = models.ForeignKey(CREDIT_MODEL,
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
        reporting_categories = models.ManyToManyField(REPORTING_MODEL,
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
        # idea_ids = [c.idea.id for c in CategoryIdea.objects.filter(category=self)]
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
            return self.ideacategoryrelation_set.filter(
                content_type__name=content_type)

        def get_relation_type(self, relation_type):
            """
            Get all relations of the specified relation type
            """
            return self.ideacategoryrelation_set.filter(
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
        return [category for category in categories
                if ar_a in category.appropriate_for.get_set_bits()]

    @property
    def tags(self):
        item_ids = self._concept_items().values_list('tag', flat=True)

        return Concept.objects.filter(id__in=item_ids)

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
        key_image = models.ForeignKey(KeyImageModel,
            blank=True,
            null=True)
    id_number = models.CharField(
        max_length=10,
        null=True,
        help_text="""This field is for the internal NG Education ID number. This
        is required for all instructional content.""")
    # Content Detail
    content_body = models.TextField()
    categories = models.ManyToManyField(IdeaCategory,
        through='CategoryIdea',
        related_name='ideas')

    def __unicode__(self):
        return self.title

    def _get_categories(self):
        return [ci.category for ci in CategoryIdea.objects.filter(idea=self)]

    # def appropriate_display(self):
    #     return bitfield_display(self.appropriate_for)
    # appropriate_display.allow_tags = True

    def get_categories(self):
        return [ic.title for ic in self._get_categories()]

    def thumbnail_html(self):
        if self.key_image:
            return '<img src="%s"/>' % self.key_image.thumbnail_url()
        else:
            return None

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
