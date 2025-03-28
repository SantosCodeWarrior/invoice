from it import views
from it import models

#####################################################
def cl(cl_id=88):	
	check_invoice = models.invoice.objects.filter(client_id=cl_id,proj_name='BOSS',usd='USD')
	for c in check_invoice:
		c.client_id = 64
		#c.save()
		print '------',c.client_id,'----',c.invoice_no,'-----Updating..'


