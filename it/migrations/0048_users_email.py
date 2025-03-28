# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0047_otp_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
