# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('it', '0032_auto_20241025_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='log_sessions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('url_name', models.CharField(max_length=200, null=True)),
                ('user_name', models.CharField(max_length=200, null=True)),
                ('invoice_no', models.CharField(max_length=500, null=True)),
                ('invoice_generate', models.CharField(max_length=500, null=True)),
                ('approved', models.CharField(max_length=500, null=True)),
                ('status', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='login_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_adress', models.CharField(max_length=200, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('e_date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
