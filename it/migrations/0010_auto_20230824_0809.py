# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0009_auto_20230824_0715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank_name',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='bank_name',
            name='proj_name',
        ),
    ]
