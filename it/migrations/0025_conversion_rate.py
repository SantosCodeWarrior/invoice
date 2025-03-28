# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0024_remittance_data_market_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='conversion_rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate_date', models.DateField(null=True)),
                ('rate_price', models.FloatField(null=True)),
                ('rate_open', models.CharField(max_length=150, null=True)),
                ('rate_high', models.CharField(max_length=150, null=True)),
                ('entry_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('rate_low', models.TextField(max_length=2000, null=True)),
                ('remarks', models.CharField(max_length=200, null=True)),
                ('rate_avg', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
    ]
