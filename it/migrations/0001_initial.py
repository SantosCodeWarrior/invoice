# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.db.models.deletion
from django.conf import settings
import it.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='api_client_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ship_id', models.CharField(max_length=150, null=True)),
                ('account_tab', models.CharField(max_length=150, null=True)),
                ('client_id', models.CharField(max_length=150, null=True)),
                ('ship_name', models.CharField(max_length=100, null=True)),
                ('address', models.TextField(max_length=2000, null=True)),
                ('curr_date', models.DateField(default=datetime.datetime.now, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='bank_name',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bank_name', models.TextField(max_length=2000, null=True)),
                ('currency', models.CharField(max_length=150, null=True)),
                ('proj_name', models.CharField(max_length=150, null=True)),
                ('flag_bank', models.CharField(max_length=150, null=True)),
                ('bank_address', models.CharField(max_length=1150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='bank_statement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txn_date', models.DateField(null=True)),
                ('descs', models.TextField(blank=True)),
                ('amount_inr', models.FloatField(null=True)),
                ('d_c', models.CharField(max_length=20, null=True)),
                ('amount_balance', models.FloatField(null=True)),
                ('bank_name', models.CharField(max_length=850, null=True)),
                ('referencez', models.CharField(max_length=150, null=True)),
                ('reference_no', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlueWater',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_name', models.CharField(max_length=200, null=True)),
                ('tin_number', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='boss_client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_name', models.CharField(max_length=200, null=True)),
                ('proj_name', models.CharField(max_length=50, null=True)),
                ('currency_type', models.CharField(max_length=50, null=True)),
                ('duration_type', models.CharField(max_length=50, null=True)),
                ('price', models.FloatField(null=True)),
                ('price_type', models.CharField(max_length=100, null=True)),
                ('rate', models.FloatField(null=True)),
                ('tin_number', models.CharField(max_length=100, null=True)),
                ('vm_name', models.CharField(max_length=200, null=True)),
                ('status', models.IntegerField(default=0, null=True)),
                ('change_dollar', models.IntegerField(default=0, null=True)),
                ('actives', models.IntegerField(default=0, null=True)),
                ('curr_date', models.DateField(null=True)),
                ('tax', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='chm_client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_name', models.CharField(max_length=200, null=True)),
                ('proj_name', models.CharField(max_length=50, null=True)),
                ('currency_type', models.CharField(max_length=50, null=True)),
                ('duration_type', models.CharField(max_length=50, null=True)),
                ('price', models.FloatField(null=True)),
                ('price_type', models.CharField(max_length=100, null=True)),
                ('rate', models.FloatField(null=True)),
                ('tin_number', models.CharField(max_length=100, null=True)),
                ('vm_name', models.CharField(max_length=200, null=True)),
                ('status', models.IntegerField(default=0, null=True)),
                ('change_dollar', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_name', models.CharField(max_length=200, null=True)),
                ('proj_name', models.CharField(max_length=50, null=True)),
                ('currency_type', models.CharField(max_length=50, null=True)),
                ('duration_type', models.CharField(max_length=50, null=True)),
                ('price', models.FloatField(null=True)),
                ('price_type', models.CharField(max_length=100, null=True)),
                ('rate', models.FloatField(null=True)),
                ('tin_number', models.CharField(max_length=100, null=True)),
                ('vm_name', models.CharField(max_length=200, null=True)),
                ('status', models.IntegerField(default=0, null=True)),
                ('change_dollar', models.IntegerField(default=0, null=True)),
                ('tax', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='copy_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ship_name', models.CharField(max_length=150, null=True)),
                ('voyage_no', models.CharField(max_length=150, null=True)),
                ('currency_type', models.CharField(max_length=150, null=True)),
                ('pic', models.CharField(max_length=150, null=True)),
                ('disch_date', models.DateTimeField(null=True)),
                ('client_name', models.CharField(max_length=250, null=True)),
                ('invoice_amount', models.CharField(max_length=100, null=True)),
                ('received_date', models.CharField(max_length=50, null=True)),
                ('invoice_no', models.CharField(max_length=150, null=True)),
                ('invoice_date', models.DateTimeField(null=True)),
                ('disch_port', models.CharField(max_length=150, null=True)),
                ('price_type', models.CharField(max_length=150, null=True)),
                ('paid', models.CharField(max_length=150, null=True)),
                ('client_id', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='copy_data_boss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_name', models.CharField(max_length=150, null=True)),
                ('invoice_no', models.CharField(max_length=150, null=True)),
                ('received_date', models.DateField(null=True)),
                ('amount', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='cost_per_route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.FloatField(null=True)),
                ('route', models.CharField(max_length=50, null=True)),
                ('client_id', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='currency_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('currency', models.TextField(max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='delete_vessel_details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_date', models.DateField(null=True)),
                ('delete_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('ship_name', models.CharField(max_length=100, null=True)),
                ('voy_no', models.CharField(max_length=100, null=True)),
                ('invoice_no', models.CharField(max_length=100, null=True)),
                ('proj_name', models.CharField(max_length=50, null=True)),
                ('currency_type', models.CharField(max_length=50, null=True)),
                ('price', models.FloatField(null=True)),
                ('remarks', models.CharField(max_length=100, null=True)),
                ('client_id', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='generate_dsr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ship_name', models.CharField(max_length=50, null=True)),
                ('voyage_no', models.CharField(max_length=50, null=True)),
                ('vm_name', models.CharField(max_length=50, null=True)),
                ('voyage_id', models.CharField(max_length=150, null=True)),
                ('discharge_port', models.CharField(max_length=50, null=True)),
                ('discharge_eta', models.DateField(null=True)),
                ('client_name', models.CharField(max_length=150, null=True)),
                ('proj_name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='generate_for_vessel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ship_name', models.CharField(max_length=50, null=True)),
                ('voyage_no', models.CharField(max_length=50, null=True)),
                ('currency_type', models.CharField(max_length=50, null=True)),
                ('discharge_port', models.CharField(max_length=50, null=True)),
                ('client_id', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='generate_invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_no', models.CharField(max_length=350, null=True)),
                ('currency_type', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='inbox_invoice_details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_date', models.DateField(null=True)),
                ('vessel_name', models.CharField(max_length=100, null=True)),
                ('voy_no', models.CharField(max_length=100, null=True)),
                ('invoice_amount', models.FloatField(null=True)),
                ('invoice_no', models.CharField(max_length=100, null=True)),
                ('pdf_path', models.CharField(max_length=150, null=True)),
                ('mail', models.CharField(max_length=200, null=True)),
                ('mail_cc', models.CharField(max_length=200, null=True)),
                ('mail_from', models.CharField(max_length=200, null=True)),
                ('sent_mail_date', models.DateField(null=True)),
                ('client', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_no', models.CharField(max_length=100, null=True)),
                ('invoice_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('invoice_amount', models.FloatField(null=True)),
                ('received_date', models.DateField(null=True)),
                ('vm_name', models.CharField(max_length=200, null=True)),
                ('cancel_invoice', models.IntegerField(default=0, null=True)),
                ('ship_name', models.CharField(max_length=200, null=True)),
                ('voyage_no', models.CharField(max_length=200, null=True)),
                ('proj_name', models.CharField(max_length=100, null=True)),
                ('client_address', models.TextField(max_length=2000, null=True)),
                ('payment_status', models.CharField(max_length=100, null=True)),
                ('mail_to', models.CharField(max_length=200, null=True)),
                ('mail_cc', models.CharField(max_length=200, null=True)),
                ('mail_from', models.CharField(max_length=200, null=True)),
                ('disch_date', models.DateTimeField(null=True)),
                ('disch_port', models.CharField(max_length=200, null=True)),
                ('inr', models.CharField(max_length=200, null=True)),
                ('usd', models.CharField(max_length=200, null=True)),
                ('month', models.CharField(max_length=100, null=True)),
                ('counter', models.IntegerField(default=0, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
                ('remark', models.CharField(max_length=200, null=True)),
                ('vessel_type', models.CharField(max_length=200, null=True)),
                ('deadwt', models.CharField(max_length=200, null=True)),
                ('qty', models.FloatField(default=1, null=True)),
                ('price', models.FloatField(null=True)),
                ('rate', models.FloatField(null=True)),
                ('bank_charges', models.FloatField(null=True)),
                ('received_inr', models.FloatField(null=True)),
                ('tds', models.FloatField(null=True)),
                ('rece_amount', models.FloatField(null=True)),
                ('month_name', models.CharField(max_length=100, null=True)),
                ('price_type', models.CharField(max_length=100, null=True)),
                ('account_type', models.CharField(max_length=200, null=True)),
                ('total_amount', models.FloatField(null=True)),
                ('usd_amount', models.FloatField(null=True)),
                ('last_port', models.CharField(max_length=50, null=True)),
                ('last_noon_date', models.CharField(max_length=50, null=True)),
                ('client_flag', models.CharField(max_length=200, null=True)),
                ('bank_name', models.TextField(max_length=200, null=True)),
                ('client', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='json_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_date', models.DateField(null=True)),
                ('file_name', models.CharField(max_length=100, null=True)),
                ('client_id', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='mail_invoice_details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_no', models.CharField(max_length=100, null=True)),
                ('proj_name', models.CharField(max_length=50, null=True)),
                ('currency_type', models.CharField(max_length=100, null=True)),
                ('client', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='master_inw_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txn_date', models.DateField(null=True)),
                ('amount', models.FloatField(null=True)),
                ('rate', models.FloatField(null=True)),
                ('currency', models.CharField(max_length=150, null=True)),
                ('proj_name', models.CharField(max_length=150, null=True)),
                ('inward_no', models.CharField(max_length=150, null=True)),
                ('entry_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('remarks', models.TextField(max_length=2000, null=True)),
                ('image_date', models.DateField(null=True)),
                ('image_file', models.FileField(null=True, upload_to=it.models.get_images_path)),
                ('file_name', models.CharField(max_length=150, null=True)),
                ('flag', models.CharField(max_length=100, null=True)),
                ('client_id', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='merge_billing_day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ship_name', models.CharField(max_length=150, null=True)),
                ('no_of_day', models.IntegerField(default=0, null=True)),
                ('client_name', models.CharField(max_length=150, null=True)),
                ('account_tab', models.CharField(max_length=200, null=True)),
                ('port_name', models.CharField(max_length=150, null=True)),
                ('noon_date', models.CharField(max_length=150, null=True)),
                ('api_ship', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='merge_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.TextField(max_length=2000, null=True)),
                ('ship_name', models.TextField(max_length=2000, null=True)),
                ('voyage_no', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='new_users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change_password', models.CharField(max_length=150, null=True)),
                ('changed_pwd_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='pool_master',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pool', models.CharField(max_length=200, null=True)),
                ('address', models.TextField(max_length=2000, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('email_cc', models.CharField(max_length=200, null=True)),
                ('vm_name', models.CharField(max_length=200, null=True)),
                ('client', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='price_type_details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price_type', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='remittance_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remittance_date', models.DateField(null=True)),
                ('inward_amount', models.FloatField(null=True)),
                ('client_name', models.CharField(max_length=150, null=True)),
                ('certificate_no', models.CharField(max_length=150, null=True)),
                ('currency', models.CharField(max_length=150, null=True)),
                ('rate', models.FloatField(null=True)),
                ('bank_charges', models.FloatField(null=True)),
                ('status', models.CharField(max_length=150, null=True)),
                ('invoice_amount', models.FloatField(null=True)),
                ('inr_amount', models.FloatField(null=True)),
                ('net_amount_ref', models.FloatField(null=True)),
                ('total_amount', models.FloatField(null=True)),
                ('services1', models.CharField(max_length=150, null=True)),
                ('invoice_no1', models.CharField(max_length=100, null=True)),
                ('amount1', models.FloatField(default=0)),
                ('services2', models.CharField(max_length=150, null=True)),
                ('invoice_no2', models.CharField(max_length=100, null=True)),
                ('amount2', models.FloatField(default=0)),
                ('services3', models.CharField(max_length=150, null=True)),
                ('invoice_no3', models.CharField(max_length=100, null=True)),
                ('amount3', models.FloatField(default=0)),
                ('services4', models.CharField(max_length=150, null=True)),
                ('invoice_no4', models.CharField(max_length=100, null=True)),
                ('amount4', models.FloatField(default=0)),
                ('services5', models.CharField(max_length=150, null=True)),
                ('invoice_no5', models.CharField(max_length=100, null=True)),
                ('amount5', models.FloatField(default=0)),
                ('services6', models.CharField(max_length=150, null=True)),
                ('invoice_no6', models.CharField(max_length=100, null=True)),
                ('amount6', models.FloatField(default=0)),
                ('services7', models.CharField(max_length=150, null=True)),
                ('invoice_no7', models.CharField(max_length=100, null=True)),
                ('amount7', models.FloatField(default=0)),
                ('services8', models.CharField(max_length=150, null=True)),
                ('invoice_no8', models.CharField(max_length=100, null=True)),
                ('amount8', models.FloatField(default=0)),
                ('services9', models.CharField(max_length=150, null=True)),
                ('invoice_no9', models.CharField(max_length=100, null=True)),
                ('amount9', models.FloatField(default=0)),
                ('services10', models.CharField(max_length=150, null=True)),
                ('invoice_no10', models.CharField(max_length=100, null=True)),
                ('amount10', models.FloatField(default=0)),
                ('services11', models.CharField(max_length=150, null=True)),
                ('invoice_no11', models.CharField(max_length=100, null=True)),
                ('amount11', models.FloatField(default=0)),
                ('services12', models.CharField(max_length=150, null=True)),
                ('invoice_no12', models.CharField(max_length=100, null=True)),
                ('amount12', models.FloatField(default=0)),
                ('services13', models.CharField(max_length=150, null=True)),
                ('invoice_no13', models.CharField(max_length=100, null=True)),
                ('amount13', models.FloatField(default=0)),
                ('services14', models.CharField(max_length=150, null=True)),
                ('invoice_no14', models.CharField(max_length=100, null=True)),
                ('amount14', models.FloatField(default=0)),
                ('services15', models.CharField(max_length=150, null=True)),
                ('invoice_no15', models.CharField(max_length=100, null=True)),
                ('amount15', models.FloatField(default=0)),
                ('entry_date', models.DateField(null=True)),
                ('reference_no', models.CharField(max_length=150, null=True)),
                ('remarks', models.CharField(max_length=450, null=True)),
                ('approved', models.CharField(max_length=450, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='remittance_data_inr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remittance_date', models.DateField(null=True)),
                ('amount', models.FloatField(null=True)),
                ('proj_name', models.CharField(max_length=150, null=True)),
                ('reference_no', models.CharField(max_length=150, null=True)),
                ('entry_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('remarks', models.TextField(max_length=2000, null=True)),
                ('client_name', models.CharField(max_length=200, null=True)),
                ('bank_charges', models.FloatField(null=True)),
                ('tax', models.FloatField(null=True)),
                ('services1', models.CharField(max_length=150, null=True)),
                ('invoice_no1', models.CharField(max_length=100, null=True)),
                ('amount1', models.FloatField(default=0)),
                ('services2', models.CharField(max_length=150, null=True)),
                ('invoice_no2', models.CharField(max_length=100, null=True)),
                ('amount2', models.FloatField(default=0)),
                ('services3', models.CharField(max_length=150, null=True)),
                ('invoice_no3', models.CharField(max_length=100, null=True)),
                ('amount3', models.FloatField(default=0)),
                ('services4', models.CharField(max_length=150, null=True)),
                ('invoice_no4', models.CharField(max_length=100, null=True)),
                ('amount4', models.FloatField(default=0)),
                ('services5', models.CharField(max_length=150, null=True)),
                ('invoice_no5', models.CharField(max_length=100, null=True)),
                ('amount5', models.FloatField(default=0)),
                ('services6', models.CharField(max_length=150, null=True)),
                ('invoice_no6', models.CharField(max_length=100, null=True)),
                ('amount6', models.FloatField(default=0)),
                ('services7', models.CharField(max_length=150, null=True)),
                ('invoice_no7', models.CharField(max_length=100, null=True)),
                ('amount7', models.FloatField(default=0)),
                ('services8', models.CharField(max_length=150, null=True)),
                ('invoice_no8', models.CharField(max_length=100, null=True)),
                ('amount8', models.FloatField(default=0)),
                ('services9', models.CharField(max_length=150, null=True)),
                ('invoice_no9', models.CharField(max_length=100, null=True)),
                ('amount9', models.FloatField(default=0)),
                ('services10', models.CharField(max_length=150, null=True)),
                ('invoice_no10', models.CharField(max_length=100, null=True)),
                ('amount10', models.FloatField(default=0)),
                ('services11', models.CharField(max_length=150, null=True)),
                ('invoice_no11', models.CharField(max_length=100, null=True)),
                ('amount11', models.FloatField(default=0)),
                ('services12', models.CharField(max_length=150, null=True)),
                ('invoice_no12', models.CharField(max_length=100, null=True)),
                ('amount12', models.FloatField(default=0)),
                ('services13', models.CharField(max_length=150, null=True)),
                ('invoice_no13', models.CharField(max_length=100, null=True)),
                ('amount13', models.FloatField(default=0)),
                ('services14', models.CharField(max_length=150, null=True)),
                ('invoice_no14', models.CharField(max_length=100, null=True)),
                ('amount14', models.FloatField(default=0)),
                ('services15', models.CharField(max_length=150, null=True)),
                ('invoice_no15', models.CharField(max_length=100, null=True)),
                ('amount15', models.FloatField(default=0)),
                ('igst_1', models.FloatField(default=0)),
                ('tax_amt_1', models.FloatField(default=0)),
                ('final_1', models.FloatField(default=0)),
                ('igst_2', models.FloatField(default=0)),
                ('tax_amt_2', models.FloatField(default=0)),
                ('final_2', models.FloatField(default=0)),
                ('igst_3', models.FloatField(default=0)),
                ('tax_amt_3', models.FloatField(default=0)),
                ('final_3', models.FloatField(default=0)),
                ('igst_4', models.FloatField(default=0)),
                ('tax_amt_4', models.FloatField(default=0)),
                ('final_4', models.FloatField(default=0)),
                ('igst_5', models.FloatField(default=0)),
                ('tax_amt_5', models.FloatField(default=0)),
                ('final_5', models.FloatField(default=0)),
                ('igst_6', models.FloatField(default=0)),
                ('tax_amt_6', models.FloatField(default=0)),
                ('final_6', models.FloatField(default=0)),
                ('igst_7', models.FloatField(default=0)),
                ('tax_amt_7', models.FloatField(default=0)),
                ('final_7', models.FloatField(default=0)),
                ('igst_8', models.FloatField(default=0)),
                ('tax_amt_8', models.FloatField(default=0)),
                ('final_8', models.FloatField(default=0)),
                ('igst_9', models.FloatField(default=0)),
                ('tax_amt_9', models.FloatField(default=0)),
                ('final_9', models.FloatField(default=0)),
                ('igst_10', models.FloatField(default=0)),
                ('tax_amt_10', models.FloatField(default=0)),
                ('final_10', models.FloatField(default=0)),
                ('client_id', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ship_name', models.CharField(max_length=200, null=True)),
                ('address', models.TextField(max_length=2000, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('email_cc', models.CharField(max_length=200, null=True)),
                ('vm_name', models.CharField(max_length=200, null=True)),
                ('vessel_type', models.CharField(max_length=200, null=True)),
                ('pool_name', models.CharField(max_length=200, null=True)),
                ('client', models.ForeignKey(to='it.Client', null=True)),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='it.pool_master', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.CharField(max_length=150, null=True)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='vessel_billing_day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ship_name', models.CharField(max_length=150, null=True)),
                ('no_of_day', models.CharField(max_length=150, null=True)),
                ('client_id', models.CharField(max_length=150, null=True)),
                ('first_port', models.CharField(max_length=150, null=True)),
                ('last_port', models.CharField(max_length=150, null=True)),
                ('client_name', models.CharField(max_length=150, null=True)),
                ('ship_id', models.IntegerField(default=0, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_Date', models.DateField(null=True)),
                ('voyage_id', models.CharField(max_length=150, null=True)),
                ('account_tab', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='vessel_combined_invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_no', models.CharField(max_length=100, null=True)),
                ('voyage_no', models.CharField(max_length=200, null=True)),
                ('ship_name', models.CharField(max_length=200, null=True)),
                ('proj_name', models.CharField(max_length=100, null=True)),
                ('today', models.DateTimeField(null=True)),
                ('voyage_id', models.IntegerField(default=0, null=True)),
                ('vm_name', models.CharField(max_length=200, null=True)),
                ('month', models.CharField(max_length=200, null=True)),
                ('vessel_type', models.CharField(max_length=200, null=True)),
                ('qty', models.IntegerField(default=1, null=True)),
                ('last_port', models.CharField(max_length=50, null=True)),
                ('last_noon_date', models.CharField(max_length=50, null=True)),
                ('address', models.TextField(max_length=2000, null=True)),
                ('price', models.CharField(max_length=200, null=True)),
                ('client', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='vessel_selected_invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ship_name', models.CharField(max_length=200, null=True)),
                ('voyage_no', models.CharField(max_length=200, null=True)),
                ('proj_name', models.CharField(max_length=100, null=True)),
                ('today', models.DateTimeField(null=True)),
                ('voyage_cancel', models.IntegerField(default=0, null=True)),
                ('disch_date', models.DateTimeField(null=True)),
                ('disch_port', models.CharField(max_length=200, null=True)),
                ('vm_name', models.CharField(max_length=200, null=True)),
                ('invoice_no', models.CharField(max_length=100, null=True)),
                ('month', models.CharField(max_length=200, null=True)),
                ('vessel_type', models.CharField(max_length=200, null=True)),
                ('qty', models.IntegerField(default=1, null=True)),
                ('account_type', models.CharField(max_length=200, null=True)),
                ('address', models.TextField(max_length=2000, null=True)),
                ('client', models.ForeignKey(to='it.Client', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='bank_name',
            name='client_id',
            field=models.ForeignKey(to='it.Client', null=True),
        ),
    ]
