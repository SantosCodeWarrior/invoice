# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0034_auto_20241224_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='voyage_id',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
