# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0040_remittance_data_approved_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='reference_no',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
