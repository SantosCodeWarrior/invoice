# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0021_auto_20240408_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='bluewater',
            name='proj_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
