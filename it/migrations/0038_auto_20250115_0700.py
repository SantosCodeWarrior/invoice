# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0037_remittance_data_approved_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remittance_data',
            name='approved_date',
            field=models.DateField(null=True),
        ),
    ]
