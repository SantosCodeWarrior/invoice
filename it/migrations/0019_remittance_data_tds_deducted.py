# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0018_vessel_selected_invoice_book_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance_data',
            name='tds_deducted',
            field=models.FloatField(null=True),
        ),
    ]
