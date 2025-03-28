# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0046_auto_20250214_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='otp_verification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('otps', models.TextField(max_length=100, null=True)),
            ],
        ),
    ]
