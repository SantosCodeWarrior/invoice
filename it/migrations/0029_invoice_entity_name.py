# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0028_invoice_nature_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='entity_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
