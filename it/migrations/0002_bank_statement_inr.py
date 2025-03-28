# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bank_statement_inr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txn_date', models.DateField(null=True)),
                ('descs', models.TextField(blank=True)),
                ('amount_inr', models.FloatField(null=True)),
                ('d_c', models.CharField(max_length=20, null=True)),
                ('amount_balance', models.FloatField(null=True)),
                ('bank_name', models.CharField(max_length=850, null=True)),
                ('referencez', models.CharField(max_length=150, null=True)),
                ('reference_no', models.CharField(max_length=150, null=True)),
            ],
        ),
    ]
