# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0048_users_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp_verification',
            name='current_date',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='otp_verification',
            name='user_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
