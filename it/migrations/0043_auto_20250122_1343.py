# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0042_auto_20250122_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst1',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst2',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
