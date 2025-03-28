# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0033_log_sessions_login_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance_data',
            name='amount21',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount22',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount23',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount24',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount25',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no21',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no22',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no23',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no24',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no25',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services21',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services22',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services23',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services24',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services25',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
