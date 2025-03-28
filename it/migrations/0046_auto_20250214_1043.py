# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0045_auto_20250123_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance_data',
            name='amount26',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount27',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount28',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount29',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount30',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no26',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no27',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no28',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no29',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no30',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services26',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services27',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services28',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services29',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services30',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
