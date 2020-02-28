# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curricula', '0002_auto_20150423_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='archived',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ideacategory',
            name='archived',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lesson',
            name='archived',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='unit',
            name='archived',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
