# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0014_auto_20231005_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='qty',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
