# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0012_vessel_selected_invoice_nomination_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool_master',
            name='address',
            field=models.TextField(max_length=2900, null=True),
        ),
    ]
