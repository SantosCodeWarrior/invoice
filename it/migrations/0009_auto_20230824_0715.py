# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0008_auto_20230824_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank_name',
            name='account_name2',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='account_no2',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='bank_address2',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='contact_no2',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='swift_code2',
            field=models.CharField(max_length=1150, null=True),
        ),
    ]
