# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0004_auto_20230808_1112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bank_name',
            old_name='bank_address',
            new_name='bank_address1',
        ),
        migrations.AddField(
            model_name='bank_name',
            name='bank_address2',
            field=models.CharField(max_length=1150, null=True),
        ),
    ]
