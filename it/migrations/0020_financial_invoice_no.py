# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0019_remittance_data_tds_deducted'),
    ]

    operations = [
        migrations.CreateModel(
            name='financial_invoice_no',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fin_invoice_no', models.CharField(max_length=100, null=True)),
                ('entry_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
        ),
    ]
