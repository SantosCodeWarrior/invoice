# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0020_financial_invoice_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financial_invoice_no',
            name='entry_date',
            field=models.DateField(default=datetime.datetime.now, blank=True),
        ),
    ]
