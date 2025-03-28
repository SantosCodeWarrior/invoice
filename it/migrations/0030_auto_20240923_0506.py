# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0029_invoice_entity_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance_data',
            name='amount16',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount17',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount18',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount19',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='amount20',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no16',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no17',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no18',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no19',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='invoice_no20',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services16',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services17',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services18',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services19',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='remittance_data',
            name='services20',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
