try:
    from south.models.inspector import add_ignored_fields
    add_ignored_fields(["^concepts\.managers"])
except (ImportError, RuntimeError):
    pass

from metadata import (GroupingType, LearnerGroup, LearningObjective,  # NOQA
    Material, ObjectiveRelation, PhysicalSpaceType, PluginType, Skill,
    Standard, TeachingApproach, TeachingMethodType, TechSetupType, Tip,
    TipCategory)  # NOQA

from activity import Activity, ResourceItem, Vocabulary, QuestionAnswer  # NOQA
from lesson import Lesson, LessonActivity  # NOQA
from unit import Unit, UnitLesson  # NOQA
from idea import IdeaCategory, Idea, CategoryIdea  # NOQA
from relations import ActivityRelation, LessonRelation, UnitRelation, IdeaCategoryRelation  # NOQA
