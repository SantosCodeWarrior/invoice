from it import views
from it import models

#####################################################
def VoyageEntry(data):
	
	for t in data:
		#print '-------',t['market_rates'],'----',t['rate_dates']
		try:
			db_remi	= models.remittance_data.objects.filter(remittance_date=t['rate_dates'])
			for e in db_remi:
				if e!=None:
					e.market_rate = t['market_rates']
				 	e.save()
		except:
			print


	

rate_details = models.conversion_rate.objects.all()
rate_array   = []
for c in rate_details:
	#print '--------',c.rate_avg
	rate_array.append({
	 	'rate_dates' 	: c.rate_date,
	 	'market_rates'  : c.rate_avg,
	})						

VoyageEntry(rate_array)
#from it import y