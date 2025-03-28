# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0023_auto_20240611_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance_data',
            name='market_rate',
            field=models.FloatField(null=True),
        ),
    ]
