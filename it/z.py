from it import views
from it import models

#####################################################
def VoyageEntry(data):
	
	for t in data:
		try:
			print 
			#invoice_details 				= models.invoice.objects.filter(invoice_no=t['invoice_no'],usd='USD',proj_name='CHM',client_id=t['client_id']).first()
			#invoice_details.invoice_amount  = x['invoice_amount']
			# invoice_details.save()

			#print '---------',str(t['receiv_date']),'----',t['invoice_no'],'---',t['invoice_amount']
		except:
			print


		# 	invoice_details 				= models.invoice.objects.filter(invoice_no=x['invoice_no'],usd='USD',proj_name='CHM').first()
		# 	invoice_details.client_id		= x['client_id']	
		# 	invoice_details.ship_name  		= x['ship_name']
		# 	invoice_details.invoice_no 		= x['invoice_no']
		# 	invoice_details.vm_name    		= x['pic']
		# 	invoice_details.disch_port  	= x['disch_port']		
		# 	invoice_details.disch_date  	= (x['disch_date']) 
		# try:
		# 	invoice_details.received_date  	= str(x['receiv_date'])		
		# except:
		# 	invoice_details.received_date  	= None

		# try:
		# 	invoice_details.invoice_amount  = x['invoice_amount']
		# except:
		# 	invoice_details.invoice_amount  = None
		# # 	invoice_details.cancel_invoice  = x['cancel_invoice']
		# # 	invoice_details.vessel_type  	= x['vessel_type']
		# # 	invoice_details.voyage_no  		= x['voyage_no']
		# try:
		# 	invoice_details.payment_status  = x['payment_status']
		# except:
		# 	invoice_details.payment_status  = None
		# # 	invoice_details.proj_name 	    = 'CHM'			
		# invoice_details.month  			= str(x['invoice_date'][0:10])		
		# invoice_details.counter         = 0		
		# #	invoice_details.usd 			= 'USD'
		# # 	invoice_details.inr 			= None
		# # 	invoice_details.invoice_date    = str(x['invoice_date'])			
		# invoice_details.qty 			= 1
		# invoice_details.price 			= x['price']
		# invoice_details.rate 			= 1				
		# invoice_details.save()
		# print '=============UPDATED...1',x['invoice_no']
			
		# except:	
		# 	pass		
		# 	remove_splash_invoice_no 		= x['invoice_no'].replace('/', '_')
		# 	extension_in_html 		 		= remove_splash_invoice_no+'_'+x['client_name']+".html"
		# 	extension_in_pdf  		 		= remove_splash_invoice_no+'_'+x['client_name']+".pdf"
		# 	invoice_details.client_id 		= x['client_id']	
		# 	invoice_details.ship_name  		= x['ship_name']
		# 	invoice_details.invoice_no 		= x['invoice_no']
		# 	invoice_details.vm_name    		= x['pic']
		# 	invoice_details.disch_port  	= x['disch_port']		
		# 	invoice_details.disch_date  	= (x['disch_date'])
		# 	invoice_details.received_date  	= str(x['invoice_date'][0:10])
			
		# 	invoice_details.invoice_amount  = x['invoice_amount']
		# 	invoice_details.cancel_invoice  = x['cancel_invoice']
		# 	invoice_details.vessel_type  	= x['vessel_type']
		# 	invoice_details.voyage_no  		= x['voyage_no']
		# 	invoice_details.payment_status  = x['payment_status']
		# 	invoice_details.proj_name 	    = 'CHM'
		# 	invoice_details.client_address  = x['cl_address']
		# 	invoice_details.month  			= str(x['invoice_date'][0:10])
		# 	invoice_details.url 			= "/static/pdf/"+x['client_name']+"/"+extension_in_pdf
		# 	invoice_details.counter         = 0		
		# 	invoice_details.usd 			= 'USD'
		# 	invoice_details.inr 			= None
		# 	invoice_details.invoice_date    = str(x['invoice_date'])
		# 	invoice_details.qty 			= 1
		# 	invoice_details.price 			= x['price']
		# 	invoice_details.rate 			= 1			
		# 	invoice_details.save()				
		# 	print '=============UPDATED--2',x['invoice_no']


invoice_data = []
data_details = models.copy_data.objects.all()
for x in data_details:	
	client_det 	= models.Client.objects.filter(client_name=x.client_name,currency_type='USD',proj_name='CHM').first()
	pool_det   	= models.pool_master.objects.filter(client_id=client_det).first()	
	
		
	if x.paid=='':
		rece_date  = None
	else:
		rece_date  = x.received_date

	if x.received_date!='1970-01-01':
		rec = x.received_date
	else:
		rec = None

	if x.paid=='paid':
		statusx = 'Paid'
	else:
		statusx = None


	try:
		db 					= models.invoice.objects.filter(invoice_no=x.invoice_no,usd='USD',proj_name='CHM',client_id=x.client_id).first()
		db.received_date    = rec
		db.payment_status   = statusx
		db.save()
		print '----Updating...'
	except:
		print '----Not Updaing...'




	invoice_data.append({
	 	'client_id' 		: x.client_id,	  	
	  	'invoice_no' 		: x.invoice_no,
	  	'pic'        		: x.pic,
		'disch_port' 		: x.disch_port,
	  	'disch_date' 		: str(x.disch_date),
	 	'ship_name' 		: x.ship_name,
	 	'receiv_date' 		: str(rec),
	  	'invoice_date' 		: str(x.invoice_date),
	  	'invoice_amount' 	: x.invoice_amount,
	  	'usd' 				: 'USD',
	  	'cancel_invoice' 	: 0,			
	  	'vessel_type'    	: x.client_name,
	  	'qty' 			 	: 1,
	  	'price'			 	: x.invoice_amount,
	 	'rate' 			 	: 1,
	  	'price_type'     	: x.price_type,
	  	'voyage_no' 		: x.voyage_no,
	  	'client_name'		: x.client_name,
	  	'payment_status'    : statusx
	})

	
VoyageEntry(invoice_data)
#from it import z