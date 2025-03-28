# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0003_invoice_heading'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='load_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='load_port',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
