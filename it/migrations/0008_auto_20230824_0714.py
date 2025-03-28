# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0007_auto_20230824_0714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank_name',
            name='account_name2',
        ),
        migrations.RemoveField(
            model_name='bank_name',
            name='account_no2',
        ),
        migrations.RemoveField(
            model_name='bank_name',
            name='bank_address2',
        ),
        migrations.RemoveField(
            model_name='bank_name',
            name='contact_no2',
        ),
        migrations.RemoveField(
            model_name='bank_name',
            name='swift_code2',
        ),
    ]
