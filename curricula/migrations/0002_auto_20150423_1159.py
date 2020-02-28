# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_media', '0001_initial'),
        ('curricula', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='ads_excluded',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='ads_excluded',
        ),
        migrations.AddField(
            model_name='activity',
            name='key_image',
            field=models.ForeignKey(blank=True, to='core_media.NGPhoto', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lesson',
            name='key_image',
            field=models.ForeignKey(blank=True, to='core_media.NGPhoto', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ideacategory',
            name='key_image',
            field=models.ForeignKey(blank=True, to='core_media.NGPhoto', null=True),
            preserve_default=True,
        ),
    ]
