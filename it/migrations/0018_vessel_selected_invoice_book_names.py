# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0017_auto_20240108_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='vessel_selected_invoice',
            name='book_names',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
