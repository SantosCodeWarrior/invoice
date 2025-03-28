# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0035_invoice_voyage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='approved',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
