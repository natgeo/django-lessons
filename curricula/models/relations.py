from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models


from curricula.settings import (RELATIONS, RELATION_TYPES)

if RELATIONS:
    relation_limits = reduce(lambda x, y: x | y, RELATIONS)
else:
    relation_limits = []


class RelationManager(models.Manager):
    def get_content_type(self, content_type):
        qs = self.get_queryset()
        return qs.filter(content_type__model=content_type)

    def get_relation_type(self, relation_type):
        qs = self.get_queryset()
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
        app_label = 'curricula'


class ActivityRelation(ModelRelation):
    activity = models.ForeignKey('curricula.Activity', related_name='relations')

    def __unicode__(self):
        out = u"%s related to %s" % (self.content_object, self.activity)
        if self.relation_type:
            out += u" as %s" % self.relation_type
        return out


class LessonRelation(ModelRelation):
    lesson = models.ForeignKey('curricula.Lesson', related_name='relations')

    def __unicode__(self):
        out = u"%s related to %s" % (self.content_object, self.lesson)
        if self.relation_type:
            out += u" as %s" % self.relation_type
        return out


class UnitRelation(ModelRelation):
    unit = models.ForeignKey('curricula.Unit', related_name='relations')

    def __unicode__(self):
        out = u"%s related to %s" % (self.content_object, self.unit)
        if self.relation_type:
            out += u" as %s" % self.relation_type
        return out


class IdeaCategoryRelation(ModelRelation):
    idea_category = models.ForeignKey('curricula.IdeaCategory', related_name='relations')

    def __unicode__(self):
        out = u"%s related to %s" % (self.content_object, self.idea_category)
        if self.relation_type:
            out += u" as %s" % self.relation_type
        return out
