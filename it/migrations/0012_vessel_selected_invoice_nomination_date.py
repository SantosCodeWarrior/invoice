# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0011_invoice_nomination_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='vessel_selected_invoice',
            name='nomination_date',
            field=models.DateField(null=True),
        ),
    ]
