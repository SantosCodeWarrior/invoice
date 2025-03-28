# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0030_auto_20240923_0506'),
    ]

    operations = [
        migrations.AddField(
            model_name='boss_client',
            name='day_calculate',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
