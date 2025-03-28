# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0022_bluewater_proj_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='remark',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
