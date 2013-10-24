from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^concepts\.managers"])

from metadata import (GroupingType,
    LearnerGroup,
    LearningObjective,
    Material,
    ObjectiveRelation,
    PhysicalSpaceType,
    PluginType,
    Skill,
    Standard,
    TeachingApproach,
    TeachingMethodType,
    TechSetupType,
    Tip,
    TipCategory)

from activity import (Activity, ResourceItem, Vocabulary, QuestionAnswer)
from lesson import (Lesson, LessonActivity,)
from unit import (Unit, UnitLesson)
from idea import (IdeaCategory, Idea, CategoryIdea)
from relations import (ActivityRelation, LessonRelation, UnitRelation, IdeaCategoryRelation)

