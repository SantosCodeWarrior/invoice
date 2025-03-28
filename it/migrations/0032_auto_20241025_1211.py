# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0031_boss_client_day_calculate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boss_client',
            name='day_calculate',
        ),
        migrations.AddField(
            model_name='client',
            name='day_calculate',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
