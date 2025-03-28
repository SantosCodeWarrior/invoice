# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0043_auto_20250122_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst10',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst3',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst4',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst5',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst6',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst7',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst8',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remittance_data_inr',
            name='igst9',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
