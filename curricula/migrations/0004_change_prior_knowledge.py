# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from curricula.utils import ul_as_list
import json


def reformat_prior_knowledge(apps, schema_editor):
    """
    Converts the HTML <ul> into a json array
    """
    Activity = apps.get_model("curricula", "Activity")  # NOQA
    Lesson = apps.get_model("curricula", "Lesson")  # NOQA

    for activity in Activity.objects.all():
        new_list = ul_as_list(activity.prior_knowledge)
        activity.prior_knowledge = json.dumps(new_list)
        activity.save()

    for lesson in Lesson.objects.all():
        new_list = ul_as_list(lesson.prior_knowledge)
        lesson.prior_knowledge = json.dumps(new_list)
        lesson.save()


class Migration(migrations.Migration):

    dependencies = [
        ('curricula', '0003_add_archived'),
    ]

    operations = [
        migrations.RunPython(reformat_prior_knowledge),
    ]
