# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0026_auto_20240720_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance_data',
            name='value_date',
            field=models.DateField(null=True),
        ),
    ]
