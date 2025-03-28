from django.db import models
import os
from django.core.files import File
from django.utils.timezone import datetime
from django.contrib.auth.models import User
from django.conf import settings
import uuid

class Client(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	client_name 	= models.CharField(max_length = 200, null = True)
	proj_name 		= models.CharField(max_length=50,null=True)
	currency_type 	= models.CharField(max_length=50,null=True)
	duration_type 	= models.CharField(max_length=50,null=True)
	price 			= models.FloatField(null=True)
	price_type 		= models.CharField(max_length=100,null=True)
	rate 		    = models.FloatField(null=True)
	tin_number 		= models.CharField(max_length=100,null=True)
	vm_name     	= models.CharField(max_length=200,null=True)
	status      	= models.IntegerField(null = True,default=0)
	change_dollar   = models.IntegerField(null = True,default=0)
	tax 		    = models.FloatField(null=True)
	day_calculate	= models.CharField(max_length=100,null=True)


class boss_client(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	client_name 	= models.CharField(max_length = 200, null = True)
	proj_name 		= models.CharField(max_length=50,null=True)
	currency_type 	= models.CharField(max_length=50,null=True)
	duration_type 	= models.CharField(max_length=50,null=True)
	price 			= models.FloatField(null=True)
	price_type 		= models.CharField(max_length=100,null=True)
	rate 		    = models.FloatField(null=True)
	tin_number 		= models.CharField(max_length=100,null=True)
	vm_name     	= models.CharField(max_length=200,null=True)
	status      	= models.IntegerField(null = True,default=0)
	change_dollar   = models.IntegerField(null = True,default=0)
	actives      	= models.IntegerField(null = True,default=0)
	curr_date   	= models.DateField(null = True)
	tax 		    = models.FloatField(null=True)


class pool_master(models.Model): ## account tab
	def __unicode__(self):
		return '%s' (self.id)
	pool 	 = models.CharField(max_length=200,null=True)
	client 	 = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)
	address  = models.TextField(max_length=2900, null=True)
	email 	 = models.CharField(max_length=200,null=True)
	email_cc = models.CharField(max_length=200,null=True)
	vm_name  = models.CharField(max_length=200,null=True)


class Ship(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	ship_name 	= models.CharField(max_length  = 200, null = True)	
	client 	 	= models.ForeignKey(Client,null=True,on_delete=models.CASCADE)
	address  	= models.TextField(max_length=2000, null=True)
	email 		= models.CharField(max_length=200,null=True)
	email_cc	= models.CharField(max_length=200,null=True)	
	vm_name     = models.CharField(max_length=200,null=True)
	vessel_type	= models.CharField(max_length = 200, null = True)
	pool_name	= models.CharField(max_length = 200, null = True)
	pool 		= models.ForeignKey(pool_master, null=True ,on_delete=models.PROTECT)

class invoice(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	invoice_no  	= models.CharField(max_length=100,null=True)
	invoice_date  	= models.DateTimeField(default=datetime.now,blank=True)
	invoice_amount  = models.FloatField(null=True)
	received_date  	= models.DateField( null = True)
	vm_name     	= models.CharField(max_length=200,null=True)
	cancel_invoice 	= models.IntegerField(null = True,default=0)
	ship_name 		= models.CharField(max_length  = 2000, null = True)
	voyage_no 		= models.CharField(max_length = 200, null = True)
	proj_name  		= models.CharField(max_length=100,null=True)
	client_address	= models.TextField(max_length=2000, null=True)
	payment_status 	= models.CharField(max_length=100,null=True)##paid or unpaid	
	mail_to 		= models.CharField(max_length=200,null=True)
	mail_cc 		= models.CharField(max_length=200,null=True)
	mail_from 		= models.CharField(max_length=200,null=True)
	client 	 		= models.ForeignKey(Client,null=True,on_delete=models.CASCADE)
	disch_date      = models.DateTimeField(null = True)
	disch_port      = models.CharField(max_length = 200, null = True)
	inr  			= models.CharField(max_length = 200, null = True)
	usd  			= models.CharField(max_length = 200, null = True)
	month 		 	= models.CharField(max_length=100,null=True)##paid or unpaid
	counter			= models.IntegerField(null = True,default=0)
	url      		= models.CharField(max_length=200,null=True)
	remark 		 	= models.CharField(max_length = 2000, null = True)
	vessel_type	 	= models.CharField(max_length = 200, null = True)
	deadwt	 		= models.CharField(max_length = 200, null = True)
	qty 			= models.FloatField(null=True)
	price	 		= models.FloatField(null=True)
	rate	 		= models.FloatField(null=True)
	bank_charges	= models.FloatField(null=True)
	received_inr	= models.FloatField(null=True)
	tds	   			= models.FloatField(null=True)
	rece_amount		= models.FloatField(null=True)
	month_name     	= models.CharField(max_length=100,null=True)
	price_type 		= models.CharField(max_length=100,null=True)
	account_type	= models.CharField(max_length = 200, null = True)
	total_amount	= models.FloatField(null=True)
	usd_amount		= models.FloatField(null=True)
	last_port		= models.CharField(max_length=50,null=True)
	last_noon_date	= models.CharField(max_length=50,null=True)		
	client_flag		= models.CharField(max_length = 200, null = True)
	bank_name 		= models.TextField(max_length=200, null=True)
	heading 		= models.TextField(max_length=800, null=True)
	load_date       = models.DateTimeField(null = True)
	load_port       = models.CharField(max_length = 200, null = True)
	nomination_date	= models.DateField(null = True)
	nature_type 	= models.CharField(max_length = 200, null = True)
	entity_name  	= models.CharField(max_length = 200, null = True)
	voyage_id 		= models.CharField(max_length  = 2000, null = True)
	approved 		= models.CharField(max_length  = 2000, null = True)
	reference_no	= models.CharField(max_length = 200, null = True)

class Users(models.Model):
	user 			= models.OneToOneField(User, null = True)	
	user_type 		= models.CharField(max_length = 150, null = True)
	email			= models.CharField(max_length = 500, null = True)


class vessel_selected_invoice(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	ship_name 		= models.CharField(max_length  = 200, null = True)
	voyage_no 		= models.CharField(max_length = 200, null = True)
	proj_name  		= models.CharField(max_length=100,null=True)	
	today       	= models.DateTimeField(null = True)
	voyage_cancel 	= models.IntegerField(null = True,default=0)
	disch_date      = models.DateTimeField(null = True)
	disch_port      = models.CharField(max_length = 200, null = True)
	vm_name     	= models.CharField(max_length=200,null=True)
	client 	 		= models.ForeignKey(Client,null=True,on_delete=models.CASCADE)	
	invoice_no  	= models.CharField(max_length=100,null=True)
	month 		    = models.CharField(max_length=200,null=True)
	vessel_type	 	= models.CharField(max_length = 200, null = True)	
	qty 			= models.IntegerField(null = True,default=1)	
	account_type	= models.CharField(max_length = 200, null = True)
	address  		= models.TextField(max_length=2000, null=True)
	nomination_date	= models.DateField(null = True)
	book_names 		= models.CharField(max_length = 200, null = True)

class BlueWater(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	client_name 	= models.CharField(max_length = 200, null = True)	
	tin_number 		= models.CharField(max_length=100,null=True)
	proj_name  		= models.CharField(max_length=100,null=True)

class vessel_combined_invoice(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	invoice_no  	= models.CharField(max_length=100,null=True)
	voyage_no 		= models.CharField(max_length = 200, null = True)
	ship_name 		= models.CharField(max_length  = 200, null = True)	
	proj_name  		= models.CharField(max_length=100,null=True)	
	today       	= models.DateTimeField(null = True)	
	voyage_id   	= models.IntegerField(null = True,default=0)
	vm_name 		= models.CharField(max_length=200,null=True)
	client 	 		= models.ForeignKey(Client,null=True,on_delete=models.CASCADE)	
	month 		    = models.CharField(max_length=200,null=True)
	vessel_type	 	= models.CharField(max_length = 200, null = True)	
	qty 			= models.IntegerField(null = True,default=1)
	last_port		= models.CharField(max_length=50,null=True)
	last_noon_date	= models.CharField(max_length=50,null=True)	
	address  		= models.TextField(max_length=2000, null=True)
	price	 		= models.CharField(max_length = 200, null = True)

class mail_invoice_details(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	invoice_no  	= models.CharField(max_length=100,null=True)	
	client 	 		= models.ForeignKey(Client,null=True,on_delete=models.CASCADE)	
	proj_name 		= models.CharField(max_length=50,null=True)
	currency_type	= models.CharField(max_length=100,null=True)

class inbox_invoice_details(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	invoice_date	= models.DateField(null = True)
	vessel_name     = models.CharField(max_length=100,null=True)
	voy_no 			= models.CharField(max_length=100,null=True)
	client 	 		= models.ForeignKey(Client,null=True,on_delete=models.CASCADE)	
	invoice_amount  = models.FloatField(null=True)
	invoice_no  	= models.CharField(max_length=100,null=True)
	pdf_path 		= models.CharField(max_length=150,null=True)	
	mail 			= models.CharField(max_length=200,null=True)
	mail_cc 		= models.CharField(max_length=200,null=True)
	mail_from 		= models.CharField(max_length=200,null=True)
	sent_mail_date  = models.DateField(null = True)

class new_users(models.Model):
	user 			 = models.ForeignKey(User,null=True)
	change_password  = models.CharField(max_length = 150, null = True)	
	changed_pwd_date = models.DateTimeField(auto_now_add=True)


class delete_vessel_details(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	invoice_date   = models.DateField(null = True)
	delete_date    = models.DateTimeField(default=datetime.now,blank=True)	
	ship_name 	   = models.CharField(max_length=100,null=True)
	voy_no 		   = models.CharField(max_length=100,null=True)
	invoice_no     = models.CharField(max_length=100,null=True)	
	client_id 	   = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)	
	proj_name 	   = models.CharField(max_length=50,null=True)
	currency_type  = models.CharField(max_length=50,null=True)	
	price 		   = models.FloatField(null=True)
	remarks        = models.CharField(max_length=100,null=True)


class price_type_details(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	price_type     = models.CharField(max_length=50,null=True)

class cost_per_route(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	cost  			= models.FloatField(null=True)
	route 			= models.CharField(max_length=50,null=True)	
	client_id 	    = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)	

class generate_invoice(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	invoice_no 		= models.CharField(max_length=350,null=True)	
	currency_type 	= models.CharField(max_length=50,null=True)	

	
class generate_for_vessel(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	ship_name		= models.CharField(max_length=50,null=True)	
	voyage_no		= models.CharField(max_length=50,null=True)
	client_id 	    = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)
	currency_type 	= models.CharField(max_length=50,null=True)
	discharge_port	= models.CharField(max_length=50,null=True)	

class copy_data(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	ship_name		= models.CharField(max_length=150,null=True)	
	voyage_no		= models.CharField(max_length=150,null=True)
	client_id 	    = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)
	currency_type 	= models.CharField(max_length=150,null=True)	
	pic				= models.CharField(max_length=150,null=True)	
	disch_date		= models.DateTimeField(null = True)
	client_name		= models.CharField(max_length=250,null=True)	
	invoice_amount 	= models.CharField(max_length=100,null=True)
	received_date	= models.CharField(max_length=50,null=True)
	invoice_no		= models.CharField(max_length=150,null=True)	
	invoice_date 	= models.DateTimeField(null = True)
	disch_port		= models.CharField(max_length=150,null=True)	
	price_type		= models.CharField(max_length=150,null=True)
	paid 			= models.CharField(max_length=150,null=True)

def get_file_path(instance, filename):
	try:
		os.remove('/var/www/html/invoice/it/static/excel/'+str(filename))
	except:
	 	pass
	return os.path.join('/var/www/html/invoice/it/static/excel/'+str(filename))

# class uploader(models.Model):
# 	def __unicode__(self):
# 		return '%s' % (self.id)	
# 	invoice_excel	= models.FileField(upload_to=get_file_path,null=True)	
# 	upload_date 	= models.DateField( null = True)
# 	file_name		= models.CharField(max_length=150,null=True)	

class copy_data_boss(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	client_name		= models.CharField(max_length=150,null=True)	
	invoice_no		= models.CharField(max_length=150,null=True)	
	received_date 	= models.DateField(null = True)
	amount 			= models.CharField(max_length=100,null=True)

class json_data(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	upload_date 	= models.DateField(null = True)
	file_name       = models.CharField(max_length=100,null=True)
	client_id 	    = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)
	

class api_client_data(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	ship_id		= models.CharField(max_length=150,null=True)	
	account_tab	= models.CharField(max_length=150,null=True)	
	client_id 	= models.CharField(max_length=150,null=True)	
	ship_name 	= models.CharField(max_length=100,null=True)
	address  	= models.TextField(max_length=2000, null=True)
	curr_date   = models.DateField(default=datetime.now,blank=True)	
	

class vessel_billing_day(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	ship_name	= models.CharField(max_length=150,null=True)	
	no_of_day	= models.CharField(max_length=150,null=True)	
	client_id 	= models.CharField(max_length=150,null=True)
	first_port	= models.CharField(max_length=150,null=True)
	last_port	= models.CharField(max_length=150,null=True)
	client_name	= models.CharField(max_length=150,null=True)
	ship_id	   	= models.IntegerField(null = True,default=0)
	start_date 	= models.DateField(null = True)
	end_Date 	= models.DateField(null = True)
	voyage_id	= models.CharField(max_length=150,null=True)
	account_tab = models.CharField(max_length = 200, null = True)
	status 		= models.CharField(max_length=50,null=True)



class merge_billing_day(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	ship_name	= models.CharField(max_length=150,null=True)	
	no_of_day	= models.IntegerField(null = True,default=0)	
	client_name	= models.CharField(max_length=150,null=True)
	account_tab = models.CharField(max_length = 200, null = True)
	port_name	= models.CharField(max_length=150,null=True)	
	noon_date	= models.CharField(max_length=150,null=True)
	api_ship	= models.CharField(max_length=150,null=True)		

class generate_dsr(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	ship_name		= models.CharField(max_length=50,null=True)	
	voyage_no		= models.CharField(max_length=50,null=True)
	vm_name			= models.CharField(max_length=50,null=True)	
	voyage_id		= models.CharField(max_length=150,null=True)
	discharge_port	= models.CharField(max_length=50,null=True)	
	discharge_eta 	= models.DateField(null = True)
	client_name		= models.CharField(max_length=150,null=True)
	proj_name 	    = models.CharField(max_length=50,null=True)






# class image_uploader(models.Model):
# 	def __unicode__(self):
# 		return '%s' % (self.id)
# 	image_file		= models.FileField(upload_to=get_images_path,null=True)
# 	image_date 		= models.DateField( null = True)
# 	file_name		= models.CharField(max_length=150,null=True)
# 	invoice_no		= models.CharField(max_length=150,null=True)
# 	proj_name		= models.CharField(max_length=150,null=True)

class bank_statement(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	txn_date 		= models.DateField(null = True)
	descs 			= models.TextField(blank = True)
	amount_inr 		= models.FloatField(null=True)
	d_c 			= models.CharField(max_length=20,null=True)
	amount_balance	= models.FloatField(null=True)
	bank_name 		= models.CharField(max_length=850,null=True)
	referencez		= models.CharField(max_length=150,null=True)
	reference_no 	= models.CharField(max_length=150,null=True)
	# rate 			= models.CharField(max_length=150,null=True)

class bank_statement_inr(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	txn_date 		= models.DateField(null = True)
	descs 			= models.TextField(blank = True)
	amount_inr 		= models.FloatField(null=True)
	d_c 			= models.CharField(max_length=20,null=True)
	amount_balance	= models.FloatField(null=True)
	bank_name 		= models.CharField(max_length=850,null=True)
	referencez		= models.CharField(max_length=150,null=True)
	reference_no 	= models.CharField(max_length=150,null=True)
	#rate 			= models.CharField(max_length=150,null=True)

class bank_name(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	bank_name 		= models.TextField(max_length=2000, null=True)
	client_id 	    = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)	
	# currency 		= models.CharField(max_length=150,null=True)
	# proj_name 		= models.CharField(max_length=150,null=True)
	flag_bank 		= models.CharField(max_length=150,null=True)
	bank_address1	= models.CharField(max_length=1150,null=True)
	swift_code1		= models.CharField(max_length=1150,null=True)
	account_name1	= models.CharField(max_length=1150,null=True)
	account_no1		= models.CharField(max_length=1150,null=True)
	contact_no1		= models.CharField(max_length=1150,null=True)
	bank_address2	= models.CharField(max_length=1150,null=True)
	swift_code2		= models.CharField(max_length=1150,null=True)
	account_name2	= models.CharField(max_length=1150,null=True)
	account_no2		= models.CharField(max_length=1150,null=True)
	contact_no2		= models.CharField(max_length=1150,null=True)

def get_images_path(instance, filename):	
	#print '----->>>',instance,'--->>-',filename
	try:
		os.remove('/var/www/html/invoice/it/static/Advice_images/'+str(filename))
	except:
	   	pass

	return os.path.join('/var/www/html/invoice/it/static/Advice_images/'+str(filename))

class master_inw_data(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	txn_date		= models.DateField(null = True)
	amount 	    	= models.FloatField(null=True)
	rate 	    	= models.FloatField(null=True)
	currency 		= models.CharField(max_length=150,null=True)
	proj_name 		= models.CharField(max_length=150,null=True)
	inward_no 		= models.CharField(max_length=150,null=True)
	entry_date 		= models.DateTimeField(default=datetime.now,blank=True)
	remarks			= models.TextField(max_length=2000, null=True)
	client_id 	    = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)	
	image_date 		= models.DateField( null = True)
	image_file		= models.FileField(upload_to=get_images_path,null=True)	
	file_name		= models.CharField(max_length=150,null=True)
	flag 			= models.CharField(max_length=100,null=True)


class remittance_data(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	value_date		= models.DateField(null = True)
	remittance_date	= models.DateField(null = True)
	inward_amount 	= models.FloatField(null=True)
	client_name 	= models.CharField(max_length=150,null=True)
	certificate_no 	= models.CharField(max_length=150,null=True)
	currency 		= models.CharField(max_length=150,null=True)	
	rate 		    = models.FloatField(null=True)
	market_rate     = models.FloatField(null=True)
	bank_charges 	= models.FloatField(null=True)	
	status 			= models.CharField(max_length=150,null=True)
	invoice_amount 	= models.FloatField(null=True)	
	inr_amount 		= models.FloatField(null=True)	
	net_amount_ref	= models.FloatField(null=True)	
	total_amount	= models.FloatField(null=True)	
	tds_deducted 	= models.FloatField(null=True)	

	services1 		= models.CharField(max_length=150,null=True)	
	invoice_no1  	= models.CharField(max_length=100,null=True)
	amount1			= models.FloatField(default=0)	

	services2 		= models.CharField(max_length=150,null=True)	
	invoice_no2  	= models.CharField(max_length=100,null=True)
	amount2			= models.FloatField(default=0)	

	services3 		= models.CharField(max_length=150,null=True)	
	invoice_no3  	= models.CharField(max_length=100,null=True)
	amount3			= models.FloatField(default=0)	

	services4 		= models.CharField(max_length=150,null=True)	
	invoice_no4  	= models.CharField(max_length=100,null=True)
	amount4			= models.FloatField(default=0)	

	services5 		= models.CharField(max_length=150,null=True)	
	invoice_no5  	= models.CharField(max_length=100,null=True)
	amount5			= models.FloatField(default=0)	

	services6 		= models.CharField(max_length=150,null=True)	
	invoice_no6  	= models.CharField(max_length=100,null=True)
	amount6			= models.FloatField(default=0)	

	services7 		= models.CharField(max_length=150,null=True)	
	invoice_no7  	= models.CharField(max_length=100,null=True)
	amount7			= models.FloatField(default=0)	

	services8 		= models.CharField(max_length=150,null=True)	
	invoice_no8  	= models.CharField(max_length=100,null=True)
	amount8			= models.FloatField(default=0)	

	services9 		= models.CharField(max_length=150,null=True)	
	invoice_no9  	= models.CharField(max_length=100,null=True)
	amount9			= models.FloatField(default=0)	

	services10 		= models.CharField(max_length=150,null=True)	
	invoice_no10  	= models.CharField(max_length=100,null=True)
	amount10		= models.FloatField(default=0)

	services11 		= models.CharField(max_length=150,null=True)	
	invoice_no11  	= models.CharField(max_length=100,null=True)
	amount11		= models.FloatField(default=0)

	services12 		= models.CharField(max_length=150,null=True)	
	invoice_no12  	= models.CharField(max_length=100,null=True)
	amount12		= models.FloatField(default=0)	

	services13 		= models.CharField(max_length=150,null=True)	
	invoice_no13  	= models.CharField(max_length=100,null=True)
	amount13		= models.FloatField(default=0)	

	services14 		= models.CharField(max_length=150,null=True)	
	invoice_no14  	= models.CharField(max_length=100,null=True)
	amount14		= models.FloatField(default=0)	

	services15 		= models.CharField(max_length=150,null=True)	
	invoice_no15  	= models.CharField(max_length=100,null=True)
	amount15		= models.FloatField(default=0)	

	services16 		= models.CharField(max_length=150,null=True)	
	invoice_no16  	= models.CharField(max_length=100,null=True)
	amount16		= models.FloatField(default=0)	

	services17 		= models.CharField(max_length=150,null=True)	
	invoice_no17  	= models.CharField(max_length=100,null=True)
	amount17		= models.FloatField(default=0)	

	services18 		= models.CharField(max_length=150,null=True)	
	invoice_no18  	= models.CharField(max_length=100,null=True)
	amount18		= models.FloatField(default=0)	

	services19 		= models.CharField(max_length=150,null=True)	
	invoice_no19  	= models.CharField(max_length=100,null=True)
	amount19		= models.FloatField(default=0)	

	services20 		= models.CharField(max_length=150,null=True)	
	invoice_no20	= models.CharField(max_length=100,null=True)
	amount20		= models.FloatField(default=0)	

	services21 		= models.CharField(max_length=150,null=True)	
	invoice_no21	= models.CharField(max_length=100,null=True)
	amount21		= models.FloatField(default=0)	

	services22 		= models.CharField(max_length=150,null=True)	
	invoice_no22	= models.CharField(max_length=100,null=True)
	amount22		= models.FloatField(default=0)	

	services23 		= models.CharField(max_length=150,null=True)	
	invoice_no23	= models.CharField(max_length=100,null=True)
	amount23		= models.FloatField(default=0)	

	services24 		= models.CharField(max_length=150,null=True)	
	invoice_no24	= models.CharField(max_length=100,null=True)
	amount24		= models.FloatField(default=0)	

	services25 		= models.CharField(max_length=150,null=True)	
	invoice_no25	= models.CharField(max_length=100,null=True)
	amount25		= models.FloatField(default=0)	

	services26 		= models.CharField(max_length=150,null=True)	
	invoice_no26	= models.CharField(max_length=100,null=True)
	amount26		= models.FloatField(default=0)	
	
	services27 		= models.CharField(max_length=150,null=True)	
	invoice_no27	= models.CharField(max_length=100,null=True)
	amount27		= models.FloatField(default=0)	
	
	services28 		= models.CharField(max_length=150,null=True)	
	invoice_no28	= models.CharField(max_length=100,null=True)
	amount28		= models.FloatField(default=0)	
	
	services29 		= models.CharField(max_length=150,null=True)	
	invoice_no29	= models.CharField(max_length=100,null=True)
	amount29		= models.FloatField(default=0)	

	services30 		= models.CharField(max_length=150,null=True)	
	invoice_no30	= models.CharField(max_length=100,null=True)
	amount30		= models.FloatField(default=0)	
	

	entry_date		= models.DateField(null = True)
	reference_no 	= models.CharField(max_length=150,null=True)
	remarks 		= models.CharField(max_length=450,null=True)
	approved 		= models.CharField(max_length=450,null=True)	
	approved_date 	= models.DateField(null = True)

class chm_client(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)
	client_name 	= models.CharField(max_length = 200, null = True)
	proj_name 		= models.CharField(max_length=50,null=True)
	currency_type 	= models.CharField(max_length=50,null=True)
	duration_type 	= models.CharField(max_length=50,null=True)
	price 			= models.FloatField(null=True)
	price_type 		= models.CharField(max_length=100,null=True)
	rate 		    = models.FloatField(null=True)
	tin_number 		= models.CharField(max_length=100,null=True)
	vm_name     	= models.CharField(max_length=200,null=True)
	status      	= models.IntegerField(null = True,default=0)
	change_dollar   = models.IntegerField(null = True,default=0)

class currency_data(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	currency 		= models.TextField(max_length=2000, null=True)	


class merge_data(models.Model): ## account tab
	def __unicode__(self):
		return '%s' (self.id)	
	client 	 	= models.TextField(max_length=2000, null=True)
	ship_name  	= models.TextField(max_length=2000, null=True)
	voyage_no 	= models.CharField(max_length=200,null=True)


class remittance_data_inr(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	remittance_date		= models.DateField(null = True)
	reference_no 		= models.CharField(max_length=150,null=True)	
	amount_received		= models.FloatField(null=True)	
	status				= models.TextField(max_length=200, null=True)
	total_remitt		= models.FloatField(null=True)
	charges_any			= models.FloatField(null=True)
	remitt_amount		= models.FloatField(null=True)

	invoice_no1			= models.TextField(max_length=200, null=True)
	client_name1 		= models.CharField(max_length = 700, null = True)
	principle1			= models.FloatField(null=True)
	igst1				= models.TextField(max_length=200, null=True)
	igst_value1			= models.FloatField(null=True)
	tds1				= models.FloatField(null=True)
	tds_amount1 	    = models.FloatField(null=True)
	tds_igst1 			= models.FloatField(null=True)
	tds_igst_amt1   	= models.FloatField(null=True)
	principle_tds_ded1 	= models.FloatField(null=True)
	remitt1 			= models.TextField(max_length=200, null=True)

	remitt_amount2		= models.FloatField(null=True)
	invoice_no2			= models.TextField(max_length=200, null=True)
	client_name2 		= models.CharField(max_length = 700, null = True)
	principle2			= models.FloatField(null=True)
	igst2				= models.TextField(max_length=200, null=True)
	igst_value2			= models.FloatField(null=True)
	tds2				= models.FloatField(null=True)
	tds_amount2 	    = models.FloatField(null=True)
	tds_igst2 			= models.FloatField(null=True)
	tds_igst_amt2   	= models.FloatField(null=True)
	principle_tds_ded2 	= models.FloatField(null=True)
	remitt2 			= models.TextField(max_length=200, null=True)

	remitt_amount3		= models.FloatField(null=True)
	invoice_no3			= models.TextField(max_length=200, null=True)
	client_name3 		= models.CharField(max_length = 700, null = True)
	principle3			= models.FloatField(null=True)
	igst3				= models.TextField(max_length=200, null=True)
	igst_value3			= models.FloatField(null=True)
	tds3				= models.FloatField(null=True)
	tds_amount3 	    = models.FloatField(null=True)
	tds_igst3 			= models.FloatField(null=True)
	tds_igst_amt3   	= models.FloatField(null=True)
	principle_tds_ded3 	= models.FloatField(null=True)
	remitt3 			= models.TextField(max_length=200, null=True)

	remitt_amount4		= models.FloatField(null=True)
	invoice_no4			= models.TextField(max_length=200, null=True)
	client_name4 		= models.CharField(max_length = 700, null = True)
	principle4			= models.FloatField(null=True)
	igst4				= models.TextField(max_length=200, null=True)
	igst_value4			= models.FloatField(null=True)
	tds4				= models.FloatField(null=True)
	tds_amount4 	    = models.FloatField(null=True)
	tds_igst4 			= models.FloatField(null=True)
	tds_igst_amt4   	= models.FloatField(null=True)
	principle_tds_ded4 	= models.FloatField(null=True)
	remitt4 			= models.TextField(max_length=200, null=True)

	remitt_amount5		= models.FloatField(null=True)
	invoice_no5			= models.TextField(max_length=200, null=True)
	client_name5 		= models.CharField(max_length = 700, null = True)
	principle5			= models.FloatField(null=True)
	igst5				= models.TextField(max_length=200, null=True)
	igst_value5			= models.FloatField(null=True)
	tds5				= models.FloatField(null=True)
	tds_amount5 	    = models.FloatField(null=True)
	tds_igst5 			= models.FloatField(null=True)
	tds_igst_amt5   	= models.FloatField(null=True)
	principle_tds_ded5 	= models.FloatField(null=True)
	remitt5 			= models.TextField(max_length=200, null=True)

	remitt_amount6		= models.FloatField(null=True)
	invoice_no6			= models.TextField(max_length=200, null=True)
	client_name6 		= models.CharField(max_length = 700, null = True)
	principle6			= models.FloatField(null=True)
	igst6				= models.TextField(max_length=200, null=True)
	igst_value6			= models.FloatField(null=True)
	tds6				= models.FloatField(null=True)
	tds_amount6 	    = models.FloatField(null=True)
	tds_igst6 			= models.FloatField(null=True)
	tds_igst_amt6   	= models.FloatField(null=True)
	principle_tds_ded6 	= models.FloatField(null=True)
	remitt6 			= models.TextField(max_length=200, null=True)

	remitt_amount7		= models.FloatField(null=True)
	invoice_no7			= models.TextField(max_length=200, null=True)
	client_name7 		= models.CharField(max_length = 700, null = True)
	principle7			= models.FloatField(null=True)
	igst7				= models.TextField(max_length=200, null=True)
	igst_value7			= models.FloatField(null=True)
	tds7				= models.FloatField(null=True)
	tds_amount7 	    = models.FloatField(null=True)
	tds_igst7 			= models.FloatField(null=True)
	tds_igst_amt7   	= models.FloatField(null=True)
	principle_tds_ded7 	= models.FloatField(null=True)
	remitt7 			= models.TextField(max_length=200, null=True)

	remitt_amount8		= models.FloatField(null=True)
	invoice_no8			= models.TextField(max_length=200, null=True)
	client_name8 		= models.CharField(max_length = 700, null = True)
	principle8			= models.FloatField(null=True)
	igst8				= models.TextField(max_length=200, null=True)
	igst_value8			= models.FloatField(null=True)
	tds8				= models.FloatField(null=True)
	tds_amount8 	    = models.FloatField(null=True)
	tds_igst8 			= models.FloatField(null=True)
	tds_igst_amt8   	= models.FloatField(null=True)
	principle_tds_ded8 	= models.FloatField(null=True)
	remitt8 			= models.TextField(max_length=200, null=True)

	remitt_amount9		= models.FloatField(null=True)
	invoice_no9			= models.TextField(max_length=200, null=True)
	client_name9 		= models.CharField(max_length = 700, null = True)
	principle9			= models.FloatField(null=True)
	igst9				= models.TextField(max_length=200, null=True)
	igst_value9			= models.FloatField(null=True)
	tds9				= models.FloatField(null=True)
	tds_amount9 	    = models.FloatField(null=True)
	tds_igst9 			= models.FloatField(null=True)
	tds_igst_amt9   	= models.FloatField(null=True)
	principle_tds_ded9 	= models.FloatField(null=True)
	remitt9 			= models.TextField(max_length=200, null=True)

	remitt_amount10		= models.FloatField(null=True)
	invoice_no10		= models.TextField(max_length=200, null=True)
	client_name10 		= models.CharField(max_length = 700, null = True)
	principle10			= models.FloatField(null=True)
	igst10				= models.TextField(max_length=200, null=True)
	igst_value10		= models.FloatField(null=True)
	tds10				= models.FloatField(null=True)
	tds_amount10 	    = models.FloatField(null=True)
	tds_igst10 			= models.FloatField(null=True)
	tds_igst_amt10   	= models.FloatField(null=True)
	principle_tds_ded10 = models.FloatField(null=True)
	remitt10 			= models.TextField(max_length=200, null=True)
	remarks				= models.TextField(max_length=1200, null=True)
	entry_date 			= models.DateTimeField(default=datetime.now,blank=True)

	
	

class financial_invoice_no(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	fin_invoice_no 	= models.CharField(max_length=100,null=True)
	entry_date 		= models.DateField(default=datetime.now,blank=True)
	

class conversion_rate(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	rate_date		= models.DateField(null = True)
	rate_price 	    = models.FloatField(null=True)	
	rate_open 		= models.FloatField(null=True)	
	rate_high 		= models.FloatField(null=True)	
	entry_date 		= models.DateTimeField(default=datetime.now,blank=True)
	rate_low		= models.FloatField(null=True)
	rate_avg 	    = models.FloatField(null=True)
	remarks 		= models.CharField(max_length = 200, null = True)


class log_sessions(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	date				= models.DateTimeField(default=datetime.now,blank=True)
	url_name			= models.CharField(max_length=200,null=True)
	user_name			= models.CharField(max_length=200,null=True)
	invoice_no  		= models.CharField(max_length=500,null=True)
	invoice_generate 	= models.CharField(max_length=500,null=True)
	approved 			= models.CharField(max_length=500,null=True)
	status 				= models.CharField(max_length=500,null=True)

class login_log(models.Model):
	def __unicode__(self):
		return self.id
	user_id 			= models.ForeignKey(User,null=True)
	ip_adress			= models.CharField(max_length = 200, null = True)
	country				= models.CharField(max_length=200, null=True)
	state				= models.CharField(max_length=200,null=True)
	city				= models.CharField(max_length=200,null=True)
	e_date				= models.DateTimeField(auto_now_add=True)

class otp_verification(models.Model):
	def __unicode__(self):
		return '%s' % (self.id)	
	otps 				= models.TextField(max_length=100, null=True)
	current_date		= models.CharField(max_length=200, null=True)
	user_name			= models.CharField(max_length=200,null=True)