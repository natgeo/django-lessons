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
        pk = activity.prior_knowledge or ""
        pk = pk.replace("\n", "")
        new_list = ul_as_list(pk)
        new_list = [x.strip() for x in new_list]
        activity.prior_knowledge = json.dumps([x for x in new_list if x])
        activity.save()

    for lesson in Lesson.objects.all():
        pk = lesson.prior_knowledge or ""
        pk = pk.replace("\n", "")
        new_list = ul_as_list(pk)
        new_list = [x.strip() for x in new_list]
        lesson.prior_knowledge = json.dumps([x for x in new_list if x])
        lesson.save()


class Migration(migrations.Migration):

    dependencies = [
        ('curricula', '0003_add_archived'),
    ]

    operations = [
        migrations.RunPython(reformat_prior_knowledge),
    ]
