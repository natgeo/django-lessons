from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from localflavor.us.us_states import STATE_CHOICES
from django.db import models
from django.db.models import Q
from django.utils.html import strip_tags

from audience.settings import AUDIENCE_FLAGS
from bitfield import BitField
from categories.models import CategoryBase

from curricula.settings import TIP_TYPE_CHOICES, STANDARD_TYPES
from curricula.utils import truncate
from edumetadata.models import Grade

__all__ = (
    'GroupingType',
    'LearnerGroup',
    'LearningObjective',
    'Material',
    'ObjectiveRelation',
    'PhysicalSpaceType',
    'PluginType',
    'Skill',
    'Standard',
    'TeachingApproach',
    'TeachingMethodType',
    'TechSetupType',
    'Tip',
    'TipCategory',
)


class MetadataBase(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        abstract = True
        ordering = ["name"]
        app_label = 'curricula'

    def __unicode__(self):
        return self.name


class GroupingType(MetadataBase):
    pass


class LearnerGroup(models.Model):
    name = models.CharField(max_length=31)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        app_label = 'curricula'


class LearningObjective(models.Model):
    text = models.TextField()

    class Meta:
        ordering = ['text']
        app_label = 'curricula'

    def __unicode__(self):
        return self.text


OBJ_REL_MODELS = ('curricula.activity', 'curricula.lesson')
OBJ_RELS = [Q(app_label=al, model=m) for al, m in [x.split('.') for x in OBJ_REL_MODELS]]
obj_rel_limits = reduce(lambda x, y: x | y, OBJ_RELS)


class ObjectiveRelation(models.Model):
    objective = models.ForeignKey(LearningObjective)
    content_type = models.ForeignKey(
        ContentType, limit_choices_to=obj_rel_limits)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        app_label = 'curricula'

    def __unicode__(self):
        return self.objective.__unicode__()


class Material(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        app_label = 'curricula'


class PhysicalSpaceType(MetadataBase):
    is_default = models.NullBooleanField()


class PluginType(MetadataBase):
    source_url = models.CharField(max_length=128)


class Skill(CategoryBase):
    appropriate_for = BitField(flags=AUDIENCE_FLAGS)
    url = models.CharField(max_length=128, blank=True, null=True)

    class Meta(CategoryBase.Meta):
        app_label = 'curricula'


class TeachingApproach(MetadataBase):
    pass


class TeachingMethodType(MetadataBase):
    pass


class TechSetupType(models.Model):
    title = models.CharField(max_length=64)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        app_label = 'curricula'


class TipCategory(CategoryBase):
    """
    Tip-specific categories
    """
    pass

    class Meta(CategoryBase.Meta):
        app_label = 'curricula'


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
        app_label = 'curricula'

    def __unicode__(self):
        if self.category:
            return u'%s: %s' % (self.category.name,
                                truncate(strip_tags(self.body), 45))
        else:
            return truncate(strip_tags(self.body), 75)


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
        return u"%s: %s: %s" % (truncate(self.get_standard_type_display(), 54),
                                truncate(self.name, 44),
                                truncate(strip_tags(self.definition), 54))

    class Meta:
        ordering = ["standard_type", "name"]
        app_label = 'curricula'
