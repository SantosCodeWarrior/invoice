# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0016_auto_20231005_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='ship_name',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
