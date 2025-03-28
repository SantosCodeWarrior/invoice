# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0025_conversion_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversion_rate',
            name='rate_avg',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='conversion_rate',
            name='rate_high',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='conversion_rate',
            name='rate_low',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='conversion_rate',
            name='rate_open',
            field=models.FloatField(null=True),
        ),
    ]
