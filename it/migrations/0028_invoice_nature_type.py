# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0027_remittance_data_value_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='nature_type',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
