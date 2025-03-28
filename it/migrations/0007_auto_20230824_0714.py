# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0006_auto_20230824_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank_name',
            name='contact_no1',
            field=models.CharField(max_length=1150, null=True),
        ),
        migrations.AddField(
            model_name='bank_name',
            name='contact_no2',
            field=models.CharField(max_length=1150, null=True),
        ),
    ]
