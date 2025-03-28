# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0005_auto_20230824_0612'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank_name',
            name='account_name1',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='account_name2',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='account_no1',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='account_no2',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='swift_code1',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='swift_code2',
            field=models.CharField(max_length=1150, null=True),
        ),
    ]
