from django.test import TestCase
from django.contrib import admin
from django.contrib.auth.models import User

from .models import (Activity, TeachingApproach, Skill, TeachingMethodType,
        GroupingType, Standard, Lesson, LessonActivity, Unit, UnitLesson)
from edumetadata.models import Grade, Subject
from .settings import (ASSESSMENT_TYPES, PEDAGOGICAL_PURPOSE_TYPE_CHOICES,
                INTERNET_ACCESS_TYPES)

admin.autodiscover()
activityadmin = admin.site._registry[Activity]
lessonadmin = admin.site._registry[Lesson]


class BaseTestCase(TestCase):
    """
    Stuff used by all the tests
    """
    fixtures = ['fixtures/edumetadata.json', ] #'fixtures/skills.json',
                # 'fixtures/tipcategories.json', 'fixtures/tips.json',
                # 'fixtures/standards.json']
    def setUp(self):
        pass

    def _get_activity_data(self, **kwargs):
        """
        provide the basic data to create an Activity
        """
        data = dict(
            appropriate_for=31,
            title="title",
            ads_excluded=True,
            assessment="assessment",
            assessment_type=ASSESSMENT_TYPES[0][0],
            description="description",
            duration=60,
            id_number="1234",
            is_modular=True,
            pedagogical_purpose_type=PEDAGOGICAL_PURPOSE_TYPE_CHOICES[0][0],
            slug="title",
            subtitle_guiding_question="Subtitle",
            directions="These are directions",
            accessibility_notes="accessibility_notes",
            other_notes="Other notes",
            setup="there is no setup",
            internet_access_type=INTERNET_ACCESS_TYPES[0][0],
            background_information="Background info",
            prior_knowledge="prior knowledge",
        )
        data.update(kwargs)
        return data

    def _get_lesson_data(self, **kwargs):
        """
        provide the basic data to create a Lesson
        """
        data = dict(
            appropriate_for=31,
            title="title",
            ads_excluded=True,
            assessment="assessment",
            assessment_type=ASSESSMENT_TYPES[0][0],
            description="description",
            id_number="1234",
            is_modular=True,
            slug="title",
            subtitle_guiding_question="Subtitle",
            other_notes="Other notes",
            background_information="Background info",
            prior_knowledge="prior knowledge"
        )
        data.update(kwargs)
        return data

    def _get_unit_data(self, **kwargs):
        """
        provide the basic data to create a Unit
        """
        data = dict(
            appropriate_for=31,
            title="title",
            description="description",
            id_number="1234",
            slug="title",
            subtitle="Subtitle",
            overview="overview"
        )
        data.update(**kwargs)
        return data


class ActivityTest(BaseTestCase):
    """
    Tests for Activity Models
    """
    fixtures = ['fixtures/edumetadata.json', 'fixtures/skills.json',
                # 'fixtures/tipcategories.json', 'fixtures/tips.json',
                'fixtures/standards.json']
    def setUp(self):
        pass

    def test_admin_creation(self):
        """
        Use the admin form to save an activity to test for validation
        """
        user = User.objects.create_superuser('test', 'test@test.com', 'test')

        adminform = activityadmin.get_form(type("request", (), {'user': user}))
        initialdata = self._get_activity_data()
        self.assertTrue(adminform(initialdata).is_valid())


    def test_admin_publish(self):
        """
        Use the admin form to save an activity with publish=True
        """
        user = User.objects.create_superuser('test', 'test@test.com', 'test')
        adminform = activityadmin.get_form(type("request", (), {'user': user}))
        initialdata = self._get_activity_data()
        initialdata['published'] = True
        self.assertFalse(adminform(initialdata).is_valid())
        initialdata['grades'] = [Grade.objects.all()[0].id]
        initialdata['teaching_approaches'] = [TeachingApproach.objects.all()[0].id]
        initialdata['skills'] = [Skill.objects.filter(children__isnull=True)[0].id]
        initialdata['teaching_method_types'] = [TeachingMethodType.objects.all()[0].id]
        initialdata['subjects'] = [Subject.objects.filter(parent__isnull=False)[0].id]
        initialdata['grouping_types'] = [GroupingType.objects.all()[0].id]
        initialdata['standards'] = [Standard.objects.all()[0].id]
        af = adminform(initialdata)
        self.assertTrue(af.is_valid())
        # a.learner_groups.add()
        # a.tips.add()
        # a.materials.add()
        # a.physical_space_types.add()
        # a.prior_activities.add()
        # a.plugin_types.add()
        # a.tech_setup_types.add()
        # a.eras.add()

class LessonTest(BaseTestCase):
    """
    Tests for Lesson Models
    """
    def test_activity_aggregation(self):
        a1 = Activity.objects.create(**self._get_activity_data())
        a2 = Activity.objects.create(**self._get_activity_data(slug='12345', other_notes='other notes 2'))
        l = Lesson.objects.create(**self._get_lesson_data())
        grades = Grade.objects.all()[:3]

        a1.grades.add(grades[0])
        a2.grades.add(grades[1])
        LessonActivity.objects.create(lesson=l, activity=a1)
        LessonActivity.objects.create(lesson=l, activity=a2)
        l.save()
        lesson_grades = l.grades.all()
        self.assertEqual(len(lesson_grades), 2)
        self.assertTrue(lesson_grades[0] in grades)
        self.assertTrue(lesson_grades[1] in grades)
        other_notes = l.get_other_notes()
        self.assertEqual(len(other_notes), 2)
        l.other_notes = 'lesson notes'
        other_notes = l.get_other_notes()
        self.assertEqual(len(other_notes), 3)
        a1.grades.add(grades[2])
        a1.save()
        self.assertEqual(l.grades.count(), 3)
        a1.grades.remove(grades[0])
        a1.save()
        self.assertEqual(a1.grades.count(), 1)
        self.assertEqual(l.grades.count(), 2)

class UnitsTest(BaseTestCase):
    def test_activity_aggregation(self):
        a1 = Activity.objects.create(**self._get_activity_data())
        a2 = Activity.objects.create(**self._get_activity_data(slug='12345', other_notes='other notes 2'))
        l = Lesson.objects.create(**self._get_lesson_data())
        u = Unit.objects.create(**self._get_unit_data())
        grades = Grade.objects.all()[:3]

        a1.grades.add(grades[0])
        a2.grades.add(grades[1])
        LessonActivity.objects.create(lesson=l, activity=a1)
        LessonActivity.objects.create(lesson=l, activity=a2)
        UnitLesson.objects.create(unit=u, lesson=l)
        l.save()

        self.assertEqual(l.grades.count(), u.grades.count())

