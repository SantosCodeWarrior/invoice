# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0038_auto_20250115_0700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remittance_data',
            name='approved_date',
        ),
    ]
