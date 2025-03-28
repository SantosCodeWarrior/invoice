# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0044_auto_20250122_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='remittance_data_inr',
            name='remitt_amount10',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='remittance_data_inr',
            name='remitt_amount2',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='remittance_data_inr',
            name='remitt_amount3',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='remittance_data_inr',
            name='remitt_amount4',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='remittance_data_inr',
            name='remitt_amount5',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='remittance_data_inr',
            name='remitt_amount6',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='remittance_data_inr',
            name='remitt_amount7',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='remittance_data_inr',
            name='remitt_amount8',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='remittance_data_inr',
            name='remitt_amount9',
            field=models.FloatField(null=True),
        ),
    ]
