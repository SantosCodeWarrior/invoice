# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0036_invoice_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance_data',
            name='approved_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
