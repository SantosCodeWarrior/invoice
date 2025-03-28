# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0010_auto_20230824_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='nomination_date',
            field=models.DateField(null=True),
        ),
    ]
