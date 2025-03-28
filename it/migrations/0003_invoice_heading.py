# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0002_bank_statement_inr'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='heading',
            field=models.TextField(max_length=800, null=True),
        ),
    ]
