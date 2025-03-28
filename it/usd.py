from it import views
from it import models

#####################################################
def usd(data):
	for i in data:
		update_invoice = models.invoice.objects.filter(invoice_no=i['invoice_no'],client_id=i['client_id'],proj_name='BOSS',usd='USD').first()
		try:
			if i['rece_date']=='1970-01-01':
				recx_date 	= None
				paid 		= None
			else:
				recx_date 	= i['rece_date']
				paid 		= i['status']
			update_invoice.received_date  = str(recx_date)
			update_invoice.payment_status = paid
			update_invoice.save()
			print '________Updating...'
		except:
			pass



data_details = models.copy_data_boss.objects.all()
invoice_data = []
for x in data_details:	
	client_details = models.Client.objects.filter(client_name=x.client_name,proj_name='BOSS',currency_type='USD').first()
	try:
		clID = client_details.id
	except:
		clID = ''

	# if x.received_date=='1970-01-01':
	# 	rec_date = None
	# else:
	# 	rec_date = str(x.received_date)

	if x.received_date=='1970-01-01':
		payment 	= None
		rece_date 	= None
	else:
		payment 	= 'Paid'
		rece_date 	= str(x.received_date)

	invoice_data.append({
	  	'client_id'  : clID,
	  	'invoice_no' : x.invoice_no,
	  	'rece_date'  : rece_date,	  	
	  	'status'     : payment,
	  
	})
	
usd(invoice_data)
		
	



