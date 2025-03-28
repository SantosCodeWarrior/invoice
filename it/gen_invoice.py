def get_create_pdf(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,proj_name,merge,editable,currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5):
	from calendar import monthrange
	import calendar
	split_address6 = ''
	array = []
	if proj_name=='BOSS' and currency=='INR' or (proj_name=='CHM' and currency=='INR'):
		tot_amount     = total_amount
		taxable_amt    = taxable_amount
		net_tax_amount = net_taxable_amount
	if proj_name=='BOSS' and currency=='USD' or (proj_name=='CHM' and currency=='USD'):
		tot_amount     = total_amount
		net_tax_amount = tot_amount


	if proj_name=='BOSS':
		tag_name = 'BIM'
		img_tag  = 'boss.png'
	elif proj_name=='CHM':
		tag_name = 'HIM'
		img_tag  = 'chm.png'	
	
	dir      = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/'	
	if not os.path.exists(dir):
		os.makedirs(dir)
	srcfile      = '/var/www/html/invoice/it/static/pdf/1.png'
	dstroot      = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/1.png'		
	copyfile(srcfile, dstroot)
	srcfile1     = '/var/www/html/invoice/it/static/pdf/rings.png'
	dstroot1     = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/rings.png'	
	copyfile(srcfile1, dstroot1)
	srcfile2     = '/var/www/html/invoice/it/static/pdf/'+str(img_tag)
	dstroot2     = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag	
	copyfile(srcfile2, dstroot2)
	srcfile3     = '/var/www/html/invoice/it/static/pdf/'+str(img_tag)
	dstroot3     = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag	
	copyfile(srcfile3, dstroot3)
	
	
	if proj_name=='BOSS':
		if editable=='edit':
			vessel_details  = models.invoice.objects.filter(proj_name='BOSS',invoice_no=invoice_no)
		else:
			vessel_details  = models.vessel_combined_invoice.objects.filter(proj_name='BOSS')
	elif proj_name=='CHM':
		if editable=='edit':
			vessel_details  = models.invoice.objects.filter(proj_name='CHM',invoice_no=invoice_no)
		else:
			check_vessel    = models.vessel_selected_invoice.objects.all().count()
			vessel_details  = models.vessel_selected_invoice.objects.filter(proj_name='CHM')

	voy = {}
	amt = 0
	vnt = 0

	for x in vessel_details:
		remove_splash_invoice_no = x.invoice_no.replace('/', '_')
		extension_in_html 		 = remove_splash_invoice_no+'_'+client_name+".html"
		extension_in_pdf  		 = remove_splash_invoice_no+'_'+client_name+".pdf"
		client_details 	  		 = models.Client.objects.filter(client_name=client_name).first()
		inr_usd 				 = client_details.currency_type
		try:
			for_invoice_dates    = x.invoice_date.strftime('%d-%b-%Y')
		except:
			for_invoice_dates    = x.today.strftime('%d-%b-%Y')

		
		Html_file = open("/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_html),"w")
		#print '--------',"/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_html
		# Html_file.write('<center>');
		#Html_file = open("/home/munish/Documents/Finance/Finance/Current/Finance/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_html,"w")
		Html_file.write('<center>');
		# Html_file.write('<table style="width: 898px;" border="0" cellspacing="0" cellpadding="0">');
		Html_file.write('<table style="height:1200px;width:100%; position: ; top: 0; bottom: 0; left: 0; right: 0;border-collapse: collapse;">');
		Html_file.write('<tbody>');
		Html_file.write('<style>');
		Html_file.write('td{');
		Html_file.write('font-family:Arial, Helvetica, sans-serif;');
		Html_file.write('font-size:14px;');
		Html_file.write('padding:3px;');
		Html_file.write('}');
		Html_file.write('.hd{');
		Html_file.write('font-weight:bold;');
		Html_file.write('}');
		Html_file.write('.style1 {');
		Html_file.write('color: #000000;');
		Html_file.write('font-weight: bold;');
		Html_file.write('}');
		Html_file.write('.style2 {');
		Html_file.write('color: #000000;');
		Html_file.write('font-weight: bold;');
		Html_file.write('}');
		Html_file.write('.style3 {');
		Html_file.write('color: black;');
		Html_file.write('font-weight: bold;');
		Html_file.write('}');
		Html_file.write('</style>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-top: none; border-left: none; border-right: none; width:432;"><img src="1.png"  width="280px";/></td>');
		if proj_name=='BOSS':
			logo = 'boss.png'
		elif proj_name=='CHM':
			logo = 'chm.png'
		Html_file.write('<td style="border-top: none; border-left: none; border-right: none; width: 266px;"><img style="float: right;" src="'+str(logo)+'" width="95" /></td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="padding: 10px; border-top: 6px double #000000; border-left: 6px double #000000; border-right: 6px double #000000; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="1" width="100%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		customer = "Customer"+"'s"
		Html_file.write('<td style="background: #CCCCCC;" colspan="2"><span class="hd">'+customer+' name &amp; address:</span></td>');
		Html_file.write('<td rowspan="5" width="2%">&nbsp;</td>');
		Html_file.write('<td style="background: #CCCCCC;" width="22%"><span class="hd">Invoice No.</span>:</td>');
		Html_file.write('<td style="background: #CCCCCC;" width="29%">'+x.invoice_no+'</td>');  # 21%
		Html_file.write('</tr>');
		Html_file.write('<tr style="border:0px">');

		#print '________',split_address1
		if editable!='edit':
			# Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top"><strong>'+str(header)+'</strong><br />'+str(address)+'</td>');
			Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top"><strong>'+str(split_address1)+'</strong><br>'+split_address2+'<br>'+split_address3+'<br>'+split_address4+'<br>'+split_address5+'<br>'+split_address6+'</td>');
		else:
			# if client_name=='Petredec':
			# 	Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top" style="height:auto;border:0px"><b>'+str(x.ship_name)+'</b><br><b>'+'"'+str(x.ship_name)+'"'+'&nbsp;'+str(split_address1)+'</b><br>'+split_address2+'<br>'+split_address3+'<br>'+split_address4+'<br>'+split_address5+'<br>'+split_address6+'</td>');
			# else:
			Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top"><strong>'+str(split_address1)+'</strong><br>'+split_address2+'<br>'+split_address3+'<br>'+split_address4+'<br>'+split_address5+'<br>'+split_address6+'</td>');

		Html_file.write('<td>Date:</td>');
		# Html_file.write('<td><strong>'+str(format_invoice_date)+'</strong></td>');
		Html_file.write('<td><strong>'+str(for_invoice_dates)+'</strong></td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td>Our Ref.:</td>');
		Html_file.write('<td><strong>'+x.invoice_no+'</strong></td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');

		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and  currency=='INR':
			Html_file.write('<td width="21%">Customer GSTIN</td>');
			if editable!='edit':
				Html_file.write('<td width="28%">'+str(customer_no)+'</td>');
			else:
				Html_file.write('<td width="28%">'+str(customer_no)+'</td>');

			Html_file.write('<td>Blue Water GSTIN:</td>');
			Html_file.write('<td><strong>05AACCB9907G2ZQ</strong></td>');
			Html_file.write('</tr>');

		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and  currency=='USD':
			print ''
		elif proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and  currency=='INR':
			Html_file.write('<td width="21%">Customer GSTIN</td>');
			if editable!='edit':
				Html_file.write('<td width="28%">'+str(customer_no)+'</td>');
			else:
				Html_file.write('<td width="28%">'+str(customer_no)+'</td>');
			Html_file.write('<td>Blue Water GSTIN:</td>');
			Html_file.write('<td><strong>05AACCB9907G2ZQ</strong></td>');
			Html_file.write('</tr>');

		# elif proj_name=='BOSS' and inr_usd=='USD':
		# 	Html_file.write('<td width="21%"><span class="style2">Customer GSTIN</span></td>');
		# 	if editable!='edit':
		# 		Html_file.write('<td width="28%">'+str(customer_no)+'</td>');
		# 	else:
		# 		Html_file.write('<td width="28%">'+str(customer_no)+'</td>');
		# 	Html_file.write('<td><span class="style1">Blue Water GSTIN:</span></td>');
		# 	Html_file.write('<td>05AACCB9907G2ZQ</td>');
		# 	Html_file.write('</tr>');

		Html_file.write('<tr>');
		Html_file.write('<td class="hd">Person Incharge:</td>');
		try:
			Html_file.write('<td><strong>'+str(x.vm_name)+'</strong></td>');
		except:
			Html_file.write('<td><strong></strong></td>');
		if proj_name=='CHM' and currency=='INR' and client_name=='Reliance' and client_name=='Apeejay':
			#Html_file.write('<td class="hd">Disch Port,Disch Date</td>');
			Html_file.write('<td class="hd">Remarks</td>');
			if editable=='edit':
				ship_name  = x.ship_name
				voy_no     = x.voyage_no
				if merge=='1':
					#merge_ship = str(ship_name) +', '+str(voyage_no)
					disch_port 		= x.disch_port
					for_disch_date 	= x.disch_date.strftime('%d-%b-%Y')
				else:
					#merge_ship = str(ship_name) +', '+str(voy_no)
					disch_port 		= x.disch_port
					for_disch_date 	= x.disch_date.strftime('%d-%b-%Y')
				#Html_file.write('<td>'+str(merge_ship)+'</td>');
				#Html_file.write('<td>'+str(disch_port)+','+str(for_disch_date)+'</td>');
				Html_file.write('<td>'+str(ship_name)+',Voy No: ' +str(voy_no)+',Disch.Port: ' +str(disch_port)+'</td>');
			else:
				disch_port 		= x.disch_port
				for_disch_date 	= x.disch_date.strftime('%d-%b-%Y')
				#ship_name  = x.ship_name
				#voy_no     = x.voyage_no
				if merge=='1':
					#merge_ship = str(ship_name) +', '+str(voyage_no)
					merge_ship = str(disch_port)+','+str(for_disch_date)
				else:
					#merge_ship = str(ship_name) +', '+str(voy_no)
					merge_ship = str(disch_port)+','+str(for_disch_date)
				Html_file.write('<td>'+str(merge_ship)+'</td>');


		if proj_name=='BOSS' and currency=='INR' and client_name=='Reliance' or client_name=='Apeejay':			
			Html_file.write('<td class="hd">Invoice Period</td>');
			if editable=='edit':
				format_invoice_date = datetime.now().strftime("%d-%b-%Y")
				format_year 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%Y')
				format_month 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%b')
				int_month 			= datetime.strptime(x.month, "%Y-%m-%d").strftime('%m')
				get_month 			= monthrange(int(format_year),int(int_month))[1]
				remark = '01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
				Html_file.write('<td>'+str(remark)+'</td>');
			else:
				remark = '01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
				Html_file.write('<td>'+str(remark)+'</td>');
		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			ship_name  = x.ship_name
			voy_no     = x.voyage_no
			if merge=='1':
				merge_ship = str(ship_name) +', '+str(voyage_no)
			else:
				merge_ship = str(ship_name) +',Voy: '+str(voy_no)

			Html_file.write('<td class="hd">Your Ref.:</td>');
			if proj_name=='BOSS':
				if x.vessel_type!="0":					
					Html_file.write('<td>'+str(x.vessel_type)+' Fleet</td>');
				else:
					Html_file.write('<td>'+str(client_name)+' Fleet</td>');
			else:
				Html_file.write('<td>'+str(merge_ship)+'</td>');
		Html_file.write('</tr>');
		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
			print ''
		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			Html_file.write('<tr>');
			if proj_name=='BOSS':
				Html_file.write('<td class="hd"></td>');
				Html_file.write('<td>&nbsp;</td>');
				Html_file.write('<td>&nbsp;</td>');
			else:
				Html_file.write('<td class="hd">Agent Hub</td>');
				Html_file.write('<td>&nbsp;</td>');
				Html_file.write('<td>&nbsp;</td>');
			if proj_name=='BOSS':
				Html_file.write('<td class="hd">Invoice Period:</td>');
			else:
				Html_file.write('<td class="hd">Disch Port,Disch Date:</td>');


		if proj_name=='CHM' and currency=='USD':
			try:
				disch_port 		= x.disch_port
				for_disch_date 	= x.disch_date.strftime('%d-%b-%Y')
			except:
				disch_port      = ''
				for_disch_date  = ''
			Html_file.write('<td>'+str(disch_port)+','+str(for_disch_date)+'</td>');
		elif proj_name=='BOSS' and currency=='USD':
			format_invoice_date = datetime.now().strftime("%d-%b-%Y")
			format_year 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%Y')
			format_month 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%b')
			int_month 			= datetime.strptime(x.month, "%Y-%m-%d").strftime('%m')
			get_month 			= monthrange(int(format_year),int(int_month))[1]
	 		remarkx 			= '01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
			Html_file.write('<td>'+str(remarkx)+'</td>');



		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="padding: 10px; border-left: 6px double #000000; border-right: 6px double #000000; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="1" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" style="background: #CCCCCC;" colspan="2" align="center">Project Details</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" width="23%">Customer ID:</td>');
		service_type = ''
		span_type    = ''
		customerID   = ''

		if proj_name=='BOSS':
			if client_name=='Reliance':
				customerID   = 'RELIANCE/BW/BOSS  [Vendors/Business partner code : 3249511]'
				service_type = 'Other Professional, Technical And Business Services'
				span_type    = '[SAC Code: 998399]'
			elif client_name=='Shell':
				customerID   = str(client_name)+'/BW/'+str(proj_name)
				service_type = 'Marine Services'
				span_type    = ''
			elif client_name=='Apeejay':
				customerID   = str(client_name)+'/BW/'+str(proj_name)
				service_type = 'Other Professional, Technical And Business Services'
				span_type    = '[SAC Code: 998399]'
			else:
				customerID = str(client_name)+'/BW/'+str(proj_name)

		elif proj_name=='CHM':
			if client_name=='Reliance':
				customerID   = 'RELIANCE/BW/CHM [Vendors/Business partner code : 3249511]'
				service_type = 'Other Professional, Technical And Business Services '
				span_type  	 = '[SAC Code: 998399]'
			else:
				customerID   = str(client_name)+'/BW/'+str(proj_name)
				service_type = 'Other Professional, Technical And Business Services'
				span_type    = ''


		if proj_name=='BOSS' and currency=='INR':
				displayz = ''
				col 	 = '7'
		
		elif proj_name=='CHM' and currency=='INR':
			displayz = ''
			col 	 = '7'

		elif proj_name=='BOSS' and currency=='USD':			
			displayz = 'none'
			col 	 = '6'

		elif proj_name=='CHM' and currency=='USD':
			displayz = 'none'
			col 	 = '6'

		Html_file.write('<td width="77%">'+str(customerID)+'</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd">Service Name:</td>');
		if proj_name=='BOSS' and currency=='INR' or proj_name=='BOSS' and currency=='USD':
			Html_file.write('<td>Tech consultancy through BOSS</td>');
		elif  proj_name=='CHM' and currency=='INR' or proj_name=='CHM' and currency=='USD':
			Html_file.write('<td>Cargo Heating Management Services</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd">Service Type:</td>');
		Html_file.write('<td>'+str(service_type)+' <span class="style3">'+str(span_type)+'</span></td>');
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="padding: 10px; border-left: 6px double #000000; border-right: 6px double #000000; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="0" width="100%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		Html_file.write('<tr style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-bottom: 1px solid #000000;">');
		Html_file.write('<td style="background: #cccccc; border: 1px solid #000000; width: 94%;" colspan="'+str(col)+'">&nbsp;</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-bottom: 1px solid #000000; width: 7%;" align="center" valign="middle">S.No.</td>');
		Html_file.write('<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-bottom: 1px solid #000000; width: 36%;" align="center" valign="middle">Service Details</td>');
		Html_file.write('<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-bottom: 1px solid #000000; width: 10%;" align="center" valign="middle">Billing Days</td>');
		Html_file.write('<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-bottom: 1px solid #000000; width: 10%;" align="center" valign="middle">Rate</td>');
		Html_file.write('<td style="width: 20.3102%; border: 1px solid #000000;" align="center" valign="middle">Rate</td>');
		Html_file.write('<td width="14%" align="center" valign="middle" style="border-right: solid  #000000 1px;border-top: solid  #000000 0px; border-bottom: solid  #000000 1px;display:'+str(displayz)+';white-space:nowrap">USD to INR Conv. Rate</td>');
		
		if proj_name=='CHM' or proj_name=='BOSS':
			if client_name=='Reliance':
				display = ''
			else:
				display = ''

		Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000;border-right: 1px solid #000000; width: 10%;" align="center" valign="middle">Amount</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');

		#print '------------',client_name,'=======',proj_name

		if x.proj_name=='BOSS' and currency=='INR' or x.proj_name=='CHM' and currency=='INR':
			if editable=='edit':
				amount = x.price*x.rate*x.qty
				amt=amount				
			else:
				amount = (x.client.price*x.client.rate*x.qty)
				amt=amount
				


		elif x.proj_name=='BOSS' and currency=='USD' or x.proj_name=='CHM' and currency=='USD':
			if editable=='edit':
				client_price = x.price*x.qty
				amount 		 = client_price
				amt 		 = amount

			else:				
				try:
					client_del = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()				
					if client_del.client_name=='stena bulk':
						if check_vessel>=1 and check_vessel<=2:
							prices  = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='stena bulk').first()
							i_price = prices.price #_1600_____1-2'
						elif check_vessel>=3 and check_vessel<=5:
							prices  = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='stena bulk').first()
							i_price = prices.price # 1400 #______3-5'
						elif check_vessel>=6 and check_vessel<=8:
							prices  = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
							i_price = prices.price # 1200#_______6-8'
						elif check_vessel>=8:
							prices  = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
							i_price = prices.price  #1200
					elif client_del.client_name=='Stena Bulk Veg Oil':
						if check_vessel>=1 and check_vessel<=2:
							pricess = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
							i_price = pricess.price # 1700 #______1-2'
						elif check_vessel>=3 and check_vessel<=5:
							pricess = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
							i_price = pricess.price # 1500 # _____3-5'
						elif check_vessel>=6 and check_vessel<=8:
							pricess = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
							i_price = pricess.price # 1300# ______6-8'
						elif check_vessel>=8:
							pricess = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
							i_price = pricess.price  #1300

					elif client_del.client_name=='Ultranav':
						if check_vessel>=1 and check_vessel<=4:
							pricess 	 = models.Client.objects.filter(price_type='1-4',proj_name='CHM',client_name='Ultranav').first()
							i_price 	 = pricess.price # 1700 #______1-2'
							#price_typess = '1-4'
						elif check_vessel>=5 and check_vessel<=9:
							pricess 	 = models.Client.objects.filter(price_type='5-9',proj_name='CHM',client_name='Ultranav').first()
							i_price 	 = pricess.price # 1500 # _____3-5'
							#price_typess = '5-9'
						elif check_vessel>=10:
							pricess 	 = models.Client.objects.filter(price_type='ShortHaul',proj_name='CHM',client_name='Ultranav').first()
							i_price 	 = pricess.price # 1300# ______6-8'
							#price_typess = 'ShortHaul'

					elif client_del.client_name=='Litasco':			
						if check_vessel>=1 and check_vessel<=5:						
							pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco').first()
							i_price = pricess.price # 1700 #______1-2'
							#price_typess = '1-5'
						elif check_vessel>=6 and check_vessel<=10:
							pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco').first()
							i_price = pricess.price # 1500 # _____3-5'
							#price_typess = '6-10'
						elif check_vessel>=11:
							pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco').first()
							i_price = pricess.price # 1300# ______6-8'
							#price_typess = '11 and Up'
					else:
						i_price = x.client.price
						#print '=dfdfdsfdfdddddddddd'

					client_price = i_price*x.qty
					amount 		 = client_price
					amt 		 = amount
					#print '---------',amount
				except:
					price_list   = models.Client.objects.filter(proj_name='BOSS',id=112).first()
					client_price = price_list.price*x.qty
					amount 		 = client_price
					amt 		 = client_price
					


		# if client_name=='Shell' and proj_name=='BOSS' and currency=='USD':
		# 	amount = x.client.price
		# 	vnt+=0
		# 	amt = vnt
		# elif client_name!='Shell' and proj_name=='BOSS' and currency=='USD':
		# 	amount = (x.client.price)
		# 	amt=amount

		if proj_name=='BOSS':
			project = 'Tech consultancy through BOSS'
		elif proj_name=='CHM':
			project = 'Cargo Heating Management Services'

		if proj_name=='BOSS':			
			y = 1
			for j in calling_pdf:						
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 7%;"><center>'+str(y)+'</center></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 36%;white-space:nowrap">'+str(project)+'</td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 16.9275%;white-space:nowrap">'+j.ship_name+'</td>');
				if editable!='edit':
					Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 10%;"><center>'+str(j.qty)+'</center></td>');
					Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 17%;"><center>'+str(float(j.client.price))+'</center></td>');
					Html_file.write('<td style="border-left: solid #000000 1px;; border-bottom: solid #000000 1px;border-right: solid #000000 1px;display:'+str(displayz)+'"><center>'+str(float(j.client.rate))+'</center></td>');
					Html_file.write('<td style="border-left: solid #000000 1px;border-top: solid #000000 1px;border-right: solid #000000 1px;"><center>'+str(float(round(amount,2)))+'</center></td>');
				else:
					Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 10%;"><center>'+str(j.qty)+'</center></td>');
					Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 17%;"><center>'+str(float(j.price))+'</center></td>');
					Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: solid #000000 1px;display:'+str(displayz)+'"><center>'+str(float(j.rate))+'</center></td>');
					if displayz=='none':
						amtttt = (j.qty*j.price*1)
					else:
						amtttt = (j.qty*j.price*j.rate)

					Html_file.write('<td style="border-top: solid #000000 1px;border-left: solid #000000 1px;border-right: solid #000000 1px;border-bottom: solid #000000 1px;"><center>'+str(float(round(amtttt,2)))+'</center></td>');

				
				Html_file.write('</tr>');
				y+=1


			for c in range(1,6):
				Html_file.write('<tr>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 7%;white-space:nowrap">&nbsp;</td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 16.9275%;white-space:nowrap"></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 10%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-top: solid #000000 1px;border-left: solid #000000 1px;border-right: solid #000000 1px;border-bottom: solid #000000 1px"><center></center></td>');
				if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
					Html_file.write('<td style="border-top: solid #000000 1px;border-left: solid #000000 0px; border-right: solid #000000 1px;"><center></center></td>');
				else:
					print ''
				Html_file.write('</tr>');		


		amttt = 0

		if proj_name=='CHM':
			Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 7%;"><center><strong>1</strong></center></td>');
			Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 36%;white-space:nowrap;"><strong>'+str(project)+'</strong></td>');
			Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 16.9275%;white-space:nowrap;"><strong>'+x.ship_name+'</strong></td>');
			if editable!='edit':
				client_del = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()
				if client_del.client_name=='stena bulk':
					if check_vessel>=1 and check_vessel<=2:
						prices  = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='stena bulk').first()
						i_price = prices.price #_1600_____1-2'
					elif check_vessel>=3 and check_vessel<=5:
						prices  = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='stena bulk').first()
						i_price = prices.price # 1400 #______3-5'
					elif check_vessel>=6 and check_vessel<=8:
						prices  = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
						i_price = prices.price # 1200#_______6-8'
					elif check_vessel>=8:
						prices  = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
						i_price = prices.price  #1200
				elif client_del.client_name=='Stena Bulk Veg Oil':
					if check_vessel>=1 and check_vessel<=2:
						pricess = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
						i_price = pricess.price # 1700 #______1-2'
					elif check_vessel>=3 and check_vessel<=5:
						pricess = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
						i_price = pricess.price # 1500 # _____3-5'
					elif check_vessel>=6 and check_vessel<=8:
						pricess = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
						i_price = pricess.price # 1300# ______6-8'						
					elif check_vessel>=8:
						pricess = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
						i_price = pricess.price  #1300	

				elif client_del.client_name=='Ultranav':
					if check_vessel>=1 and check_vessel<=4:
						pricess 	 = models.Client.objects.filter(price_type='1-4',proj_name='CHM',client_name='Ultranav').first()
						i_price 	 = pricess.price # 1700 #______1-2'
						#price_typess = '1-4'
					elif check_vessel>=5 and check_vessel<=9:
						pricess 	 = models.Client.objects.filter(price_type='5-9',proj_name='CHM',client_name='Ultranav').first()
						i_price 	 = pricess.price # 1500 # _____3-5'
						#price_typess = '5-9'
					elif check_vessel>=10:
						pricess 	 = models.Client.objects.filter(price_type='ShortHaul',proj_name='CHM',client_name='Ultranav').first()
						i_price 	 = pricess.price # 1300# ______6-8'
						#price_typess = 'ShortHaul'

				elif client_del.client_name=='Litasco':
					if check_vessel>=1 and check_vessel<=5:						
						pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco').first()
						i_price = pricess.price # 1700 #______1-2'
						#price_typess = '1-5'
					elif check_vessel>=6 and check_vessel<=10:
						pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco').first()
						i_price = pricess.price # 1500 # _____3-5'
						#price_typess = '6-10'
					elif check_vessel>=11:
						pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco').first()
						i_price = pricess.price # 1300# ______6-8'
						#price_typess = '11 and Up'				
				else:
					i_price = x.client.price

				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 10%;"><center><strong>'+str(x.qty)+'</strong></center></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 17%;"><center><strong>'+str(float(i_price))+'</strong></center></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000;display:'+str(displayz)+'"><center><strong>'+str(float(x.client.rate))+'</strong></center></td>');
				Html_file.write('<td style="border-left: solid #000000 1px; border-top: solid #000000 1px; border-bottom: solid  #000000 1px; border-right: solid  #000000 1px;"><center><strong>'+str(float(round(amount,2)))+'</strong></center></td>');
				

				# Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 7%;"><center></center></td>');
				# Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 36%;white-space:nowrap"></td>');
				# Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 16.9275%;white-space:nowrap"></td>');
				# Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 10%;"><center></center></td>');
				# Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 17%;"><center></center></td>');
				# Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; width: 17%;"><center></center></td>');
				# Html_file.write('<td style="border-left: solid #000000 1px; border-top: solid #000000 1px; border-bottom: solid  #000000 1px; border-right: solid  #000000 1px;"><center></center></td>');


			else:
				Html_file.write('<td style="border-left: 1px solid #000000;border-bottom: 1px solid #000000; width: 10%;"><center><strong>'+str(x.qty)+'</strong></center></td>');
				Html_file.write('<td style="border-left: 1px solid #000000;border-bottom: 1px solid #000000; width: 17%;"><center><strong>'+str(float(x.price))+'</strong></center></td>');
				Html_file.write('<td style="border-left: solid #000000 1px;border-bottom: solid #000000 1px;border-right: solid #000000 1px;display:'+str(displayz)+'"><center><strong>'+str(float(x.rate))+'</strong></center></td>');
				if displayz=='none':
					amttt = (x.qty*x.price*1)
				else:
					amttt = (x.qty*x.price*x.rate)				
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000;border-right: 1px solid #000000;width: 17%;"><center><strong>'+str(float(round(amttt,2)))+'</strong></center></td>');

			Html_file.write('</tr>');


			for c in range(1,10):
				Html_file.write('<tr>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 7%;white-space:nowrap">&nbsp;</td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 16.9275%;white-space:nowrap"></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 10%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000;border-right: 1px solid #000000"><center></center></td>');
				if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
					Html_file.write('<td style="border-top: solid #000000 1px;border-left: solid #000000 0px; border-right: solid #000000 1px;"><center></center></td>');
				else:
					print ''
				Html_file.write('</tr>');


		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
			tax_amount = (total_amount*18)/100
			total_taxable_amount = (tax_amount+total_amount)
			round_off = round(total_taxable_amount,0)
			in_words = convert_money_to_text(round_off)
			#in_words  = num2words(round_off)			
			taxable   = 0
			tot_invoice = 0
			#print '______>>>>',	in_words


		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			tax_amount = x.client.price*x.qty
			if editable!='edit':
				tax_amount  = total_amount	 #amount			
			else:
				tax_amount  =  amttt

			#print '==============',tax_amount
			if tax_amount!=0:
				total_taxable_amount = tax_amount #amount
			else:
				total_taxable_amount = amount
			
			round_off 			 = round(total_amount,0)
			in_words 			 = convert_money_to_text(round_off)
			print '---------------',tax_amount
			#in_words  = num2words(round_off)


		elif proj_name=='BOSS' and currency=='USD':
				#tax_amount = x.client.price*x.qty
				tax_amount = total_amount
				total_taxable_amount = tax_amount
				round_off = round(total_taxable_amount,0)
				in_words = convert_money_to_text(round_off)

		# if proj_name=='BOSS' and currency=='USD':
		# 		total_taxable_amount = x.client.price
		# 		round_off = round(total_taxable_amount,0)
		# 		in_words  = num2words(round_off) +' only'
		#print '--------//',tax_amount
		if editable!='edit':
			if client_name=='Shell':
				due_date = x.today + timedelta(days=60)
			else:
				due_date = x.today + timedelta(days=30)
		else:
			if client_name=='Shell':
				due_date = x.invoice_date + timedelta(days=60)
			else:
				due_date = x.invoice_date + timedelta(days=30)

		#print '-----------',convert_money_to_text(total_amount),'----',total_amount


		due_date_format = due_date.strftime("%d-%b-%Y")
		if proj_name=='BOSS' and currency=='INR':
			a 			= 'style="width: 7%;"'
			b 			= 'style="width:36%;"'
			c 			= 'style="width:16.9275%"'
			d 			= 'style="width:10%;"'
			e 			= ''
			f 			= 'style="width:0.60423%;"'
			hide    	= ''
			colspan 	= 'colspan="2"'
			currency 	= 'INR'
			gst_label   = 'IGST Amount @18.0%'
			tot_invoice = 'Total Invoice Amount'
			taxable     = 'Taxable Amount (Rs.)'
		if proj_name=='CHM' and currency=='INR':
			a 			= 'style="width:7%;"'
			b 			= 'style="width:36%;"'
			c 			= 'style="width:16.9275%"'
			d 			= 'style="width:10%;"'
			e 			= 'style="display:''"'
			f 			= 'style="width:0.60423%;"'
			hide  		= ''
			colspan 	= 'colspan="2"'
			currency 	= 'INR'
			gst_label   = 'IGST Amount @18.0%'
			tot_invoice = 'Total Invoice Amount'
			taxable     = 'Taxable Amount (Rs.)'
		if proj_name=='BOSS' and currency=='USD':
			a 			= ''
			b 			= ''
			c 			= ''
			d 			= ''
			e 			= 'style="display:''"'
			f 			= ''
			hide 		= 'none'
			# colspan 	= 'colspan="2"'
			colspan 	= ''
			currency 	= 'USD'
			gst_label   = ''
			tot_invoice = ''
			taxable     = 'Total'


		if proj_name=='CHM' and currency=='USD':
			a 			= ''
			b 			= ''
			c 			= ''
			d 			= ''
			e 			= 'style="display:none"'
			f 			= ''
			hide 		= 'none'
			colspan 	= ''
			currency 	= 'USD'
			gst_label   = ''
			tot_invoice = ''
			taxable     = 'Total'

		Html_file.write('<tr style="text-align: right;">');
		Html_file.write('<td '+str(a)+'>&nbsp;</td>');
		Html_file.write('<td '+str(b)+'>&nbsp;</td>');
		#Html_file.write('<td '+str(c)+'>&nbsp;</td>');

		if proj_name=='BOSS' and currency=='INR':
			Html_file.write('<td '+str(c)+'>&nbsp;</td>');
		else:
			Html_file.write('<td '+str(c)+'>&nbsp;</td>');

		# if proj_name=='BOSS' and currency=='USD' and client_name=='Shell':
			# print ''
			# Html_file.write('<td '+str(c)+'>&nbsp;</td>');

			# if proj_name=='BOSS' and currency=='USD' and client_name!='Shell':
			# if proj_name=='BOSS' and currency=='USD':
			# 	Html_file.write('<td '+str(c)+'>&nbsp;</td>');

		if proj_name=='BOSS' and currency=='INR':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="2"><b>'+str(taxable)+'</b></td>');  # colspan="2" for CHM
		elif  proj_name=='CHM' and currency=='INR':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="2"><b>'+str(taxable)+'</b></td>');  # colspan="2" for CHM
		elif proj_name=='CHM' and currency=='USD':
			Html_file.write('<td '+str(d)+' colspan="2"><b>'+str(taxable)+'</b></td>');  # colspan="2" for CHM
			#print '=======================',taxable,'=====',amttt
			Html_file.write('<td '+str(e)+'></td>');
		elif proj_name=='BOSS' and currency=='USD':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' '+str(colspan)+'><b>'+str(taxable)+'</b></td>');  # colspan="2" for CHM

		if editable!='edit':
			Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000;border-right: 1px solid #000000;border-top:1px solid #000000"><center><strong>'+str(float(round(total_amount,2)))+'</strong></center></td>'); # amount
		else:
			#print '=========',total_amount
			Html_file.write('<td style="border-left: 1px solid #000000; border-bottom:1px solid #000000;border-right: 1px solid #000000;border-top:1px solid #000000"><center><strong>'+str(float(round(total_amount,2)))+'</strong></center></td>'); # amount
		Html_file.write('<td style="display:'+str(hide)+'">&nbsp;</td>');
		Html_file.write('</tr>');

		Html_file.write('<tr style="text-align: right;">');
		Html_file.write('<td '+str(a)+'>&nbsp;</td>');
		Html_file.write('<td '+str(b)+'>&nbsp;</td>');
		Html_file.write('<td '+str(c)+'>&nbsp;</td>');

		if proj_name=='BOSS' and currency=='INR':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="2">'+str(gst_label)+'</td>'); # CHM colspan="2"
		elif  proj_name=='CHM' and currency=='INR':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="2">'+str(gst_label)+'</td>'); # CHM colspan="2"
		elif proj_name=='CHM' and currency=='USD':
			Html_file.write('<td '+str(d)+' colspan="2"></td>');  # colspan="2" for CHM
			Html_file.write('<td '+str(e)+'></td>');
		elif proj_name=='BOSS' and currency=='USD':

			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="2">'+str(gst_label)+'</td>');  # colspan="2" for CHM

		if editable!='edit':
			#print '________',tax_amount
			Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; border-right: 1px solid #000000;display:'+str(hide)+'"><strong>'+str(float(round(tax_amount,2)))+'</strong></td>');
		else:
			Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; border-right: 1px solid #000000;display:'+str(hide)+'"><strong>'+str(float(round(taxable_amount,2)))+'</strong></td>');
		Html_file.write('<td style="display:'+str(hide)+'">&nbsp;</td>');
		Html_file.write('</tr>');

		Html_file.write('<tr style="text-align: right;">');
		Html_file.write('<td '+str(a)+'>&nbsp;</td>');
		Html_file.write('<td '+str(b)+'>&nbsp;</td>');
		Html_file.write('<td '+str(c)+'>&nbsp;</td>');
		if proj_name=='BOSS' and currency=='INR':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="2">'+str(tot_invoice)+'</td>'); # colspan="2" for CHM
		if proj_name=='CHM' and currency=='INR':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="2">'+str(tot_invoice)+'</td>'); # colspan="2" for CHM
		elif proj_name=='CHM' and currency=='USD':
			Html_file.write('<td '+str(d)+' colspan="2">'+str(tot_invoice)+'</td>'); # colspan="2" for CHM
			Html_file.write('<td '+str(e)+'></td>');
		elif proj_name=='BOSS' and currency=='USD':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="2">'+str(tot_invoice)+'</td>'); # colspan="2" for CHM

		if editable!='edit':
			Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; border-right: 1px solid #000000;display:'+str(hide)+'"><strong>'+str(float(round(total_taxable_amount,2)))+'</strong></td>');
		else:
			Html_file.write('<td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000; border-right: 1px solid #000000;display:'+str(hide)+'"><strong>'+str(float(round(net_taxable_amount,2)))+'</strong></td>');
		Html_file.write('<td style="display:'+str(hide)+'">&nbsp;</td>');
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');

		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: 6px double #000000; border-right: 6px double #000000; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="0" width="98%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		Html_file.write('<td style="; border-left: solid  #000000  1px; border-top: double #000000 1px;" width="86%">Total Invoice Amount Due (Rounded Off):</td>');
		if proj_name=='BOSS' and currency=='INR':
			if editable!='edit':
				Html_file.write('<td style="border-left: solid  #000000  1px; ; border-right: solid  #000000  1px; border-top: solid #000000 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(int(round(total_taxable_amount,0)))+'</strong></td>');
			else:
				Html_file.write('<td style="border-left: solid  #000000  1px; ; border-right: solid  #000000  1px; border-top: solid #000000 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(int(round(net_taxable_amount,0)))+'</strong></td>');
		elif proj_name=='BOSS' and currency=='USD':
			# if client_name=='Shell':
			# 	Html_file.write('<td style="border-left: solid  #000000  1px; ; border-right: solid  #000000  1px; border-top: solid #000000 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(vnt))+'</strong></td>');
			# else:
			Html_file.write('<td style="border-left: solid  #000000  1px; ; border-right: solid  #000000  1px; border-top: solid #000000 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(total_amount))+'</strong></td>');
		elif proj_name=='CHM' and currency=='INR':
			Html_file.write('<td style="border-left: solid  #000000  1px; ; border-right: solid  #000000  1px; border-top: solid #000000 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(int(round(total_taxable_amount,0)))+'</strong></td>');
		elif proj_name=='CHM' and currency=='USD':
			#if x.client.change_dollar!=1:
			Html_file.write('<td style="border-left: solid  #000000  1px; ; border-right: solid  #000000  1px; border-top: solid #000000 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(amount))+'</strong></td>');
			#elif x.client.change_dollar==1:
			#	Html_file.write('<td style="border-left: solid  #000000  1px; ; border-right: solid  #000000  1px; border-top: solid #000000 1px;" width="14%"><strong style="white-space:nowrap"> SGD '+str(float(amount))+'</strong></td>');
			#else:
			#	Html_file.write('<td style="border-left: solid  #000000  1px; ; border-right: solid  #000000  1px; border-top: solid #000000 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(amount))+'</strong></td>');

		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="background: #CCCCCC; border: solid  #000000  1px;" colspan="2"> <strong style="text-transform: capitalize;">'+str(in_words)+'</strong></td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: solid  #000000  1px; border-bottom: solid  #000000  1px;" align="right" valign="middle">Payment Due Date</td>');
		Html_file.write('<td style="border-left: solid  #000000  1px; border-right: solid  #000000  1px; border-bottom: solid  #000000  1px;"><strong>'+str(due_date_format)+'</strong></td>');
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: 6px double #000000; border-right: 6px double #000000; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="0" width="99%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		Html_file.write('<td>Terms of payment:</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td>By wire transfer to our account "<b>Blue Water Trade Winds Pvt Ltd</b>" with-</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td>');
		Html_file.write('<table border="0" width="50%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		#print '-----------------------------,,.,.,',client_name
		if client_name=='Stena Bulk Veg Oil':
			print '-------------->>',client_name
			if proj_name=='CHM' and currency=='INR' or proj_name=='CHM' and currency=='USD':
				Html_file.write('<tr>');
				Html_file.write('<td><b>HDFC Bank</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>56 Rajpur Road, Dehradun (UK), India</td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>SWIFT Code: <b>HDFCINBB</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Name: <b>Blue Water Trade Winds Pvt Ltd</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Number: <b>02252560001213</b></td>');
				Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Bank Tel. # +91-135 2744865 Fax : +91-135-2746089&nbsp</td>');
				# Html_file.write('</tr>');
		else:
			print '--------->>>>',client_name
			if proj_name=='CHM' and currency=='INR' or proj_name=='CHM' and currency=='USD':
				Html_file.write('<tr>');
				Html_file.write('<td><b>HDFC Bank</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>32, Arhat Bazar, Dehradun - 248001, Uttarakhand, INDIA</td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>SWIFT Code: <b>HDFCINBB</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Name: <b>Blue Water Trade Winds Pvt Ltd</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Number: <b>02252560001213</b></td>');
				Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Bank Tel. # +91-135 2744865 Fax : +91-135-2746089&nbsp</td>');
				# Html_file.write('</tr>');

		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: 6px double #000000; border-right: 6px double #000000; border-bottom: 6px double #000000; width: 698px;" colspan="2" align="center" valign="middle">');
		#if proj_name=='CHM' and client_name=='Reliance':
		#Html_file.write('<table border="0" width="100%" cellspacing="0" cellpadding="0" style="margin-top:-109px">');
		#elif proj_name=='BOSS' and client_name!='Reliance':
		Html_file.write('<table border="0" width="100%" cellspacing="0" cellpadding="0" style="margin-top:0px">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');

		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
			Html_file.write('<td style="border: solid #999999 1px;">Note: GST rates in this invoice is based on current applicable rate. In case of revision of GST rates and policy in the current financial year, arrears arising due to such revision will be settled at the end of current financial year.</td>');
		elif proj_name=='BOSS' and currency=='USD':
			Html_file.write('<td></td>');
		elif proj_name=='CHM' and currency=='USD':
			Html_file.write('<td></td>');

		# Html_file.write('<td></td>');
		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='USD':
			Html_file.write('<td align="center" width="52%"><img src="/var/www/html/invoice/it/static/pdf/stamp.png" style="margin-top: -224px;" width="170" height="170">');
		else:
			Html_file.write('<td align="center" width="52%">');
		Html_file.write('<p style="margin-top:-75px;">For Blue Water Trade Winds Pvt Ltd</p>');
		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
			Html_file.write('<p style="margin-top:-10px">K. Gupta</p>');
		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			Html_file.write('<pstyle="margin-top:-10px">K Gupta</p>');

		Html_file.write('<p style="margin-top:-10px">Authorized Signatory</p>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		# Html_file.write('<tr>');
		# Html_file.write('<td style="padding:6px;margin-bottom:0px" colspan="6" align="right"><img src="rings.png" width="95" height="36" style="margin-right:199px" /><br /><span style="font-family: Arial, Helvetica, sans-serif; font-size: 9pt;margin-right:155px">Visit us at : www.bwesglobal.com</span></td>');
		# Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</center>');
		#Html_file.write('</br>');
		Html_file.write('<div style="margin-top:10px"><center style="font-family: arial; font-size: 9pt;">Blue Water Trade Winds Pvt. Ltd.</center><center style="font-family: arial; font-size: 8pt;">4, Siddarth Enclave, GMS Road, Ballupur, Dehradun - 248001 Uttarkhand INDIA<br /> Tel:+91-135-2649301, 2649464 Corporate Email: info@bwesglobal.com Website:www.bwesglobal.com</center><div> <div style="padding:6px;margin-bottom:0px" colspan="6" align="right"><img src="rings.png" width="95" height="36" style="float:right;margin-bottom:50px;margin-top:-55px;;margin-right:-26px;margin-right:27px" /><br /><span style="font-family: Arial, Helvetica, sans-serif; font-size: 7pt;float:right;margin-top:-40px;margin-right:-119px;">Visit us at : www.bwesglobal.com</span></div>');
		Html_file.close()

		html  		= "/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_html)
		pdf 		= "/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_pdf)
		pdfkit.from_file([html],pdf)	
		#print '---------',html,'======',pdf
		# html  			= "/home/munish/Documents/Finance/Finance/Current/Finance/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_html
		# pdf 				= "/home/munish/Documents/Finance/Finance/Current/Finance/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_pdf
		# pdfkit.from_file([html],pdf)			
		path_save  		= models.invoice.objects.filter(invoice_no=x.invoice_no).first()		
		path_save.pdf_path = pdf		
		path_save.save()
		# srcfile4     		= pdf
		# split_invoice 	= srcfile4.split('/')
		# file_name 		= split_invoice[11]
		# dstroot4     		= 'Finance/Current/Finance/HIM/LITASCO(Original)/Online/'+file_name		
		# copyfile(srcfile4, dstroot4)		
		username   	= "BWTW059"
		password   	= "sandeep@123"
		clientname  = "OHMSERVER"
		servername  = "OHMSERVER"
		domain 	   	= 'WORKGROUP'
		ipaddress  	= "172.16.5.100"
		conn 	   	= SMBConnection(username,password,clientname,servername,domain,use_ntlm_v2=True, sign_options=2, is_direct_tcp=True)
		conn.connect(ipaddress,445)
		Shares 		= conn.listShares()	
		share_name  = Shares[5].name	
		print '---------',share_name 	
		
		if client_name=='Navig8 Chemical':
			path_name  = 'Finance/Current/Finance/HIM/Online/Navig8/Online/'			
		elif client_name =='Litasco':
			path_name  = 'Finance/Current/Finance/HIM/Online/Litasco/Online/'
		elif client_name =='Apeejay':
			path_name  = 'Finance/Current/Finance/BIM/Online/APJ/'
		
		else:			
			path_name  = 'Finance/Current/Finance/'+str(tag_name)+'/Online/'+str(client_name)+'/Online/'
		sharedfiles = conn.listPath(share_name,path_name)	

		with open("/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_pdf), 'rb') as file:	
			if client_name=='Litasco':		  		
			 	conn.storeFile('Finance',"Finance/Current/Finance/HIM/Online/Litasco/Online/"+extension_in_pdf, file)
			 	print '---....1'
			elif client_name=='Navig8 Chemical':
				conn.storeFile('Finance',"Finance/Current/Finance/HIM/Online/Navig8/Online/"+extension_in_pdf, file)
				print '---...2'	
			elif client_name=='Apeejay':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/APJ/Online/"+extension_in_pdf, file)
				print '---...3',file
			else:
				conn.storeFile('Finance',"Finance/Current/Finance/"+str(tag_name)+"/Online/"+str(client_name)+"/Online/"+extension_in_pdf, file)	 
				print '---...4',client_name
		conn.close()

		url_path   = "/static/pdf/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_pdf
		#url_path   = "/home/munish/Documents/Finance/Finance/Current/Finance/"+client_name+"/Online/"+extension_in_pdf
		url_details    = models.invoice.objects.filter(invoice_no=x.invoice_no,client_id=x.client.id)
		for x in url_details:
			x.url = url_path
			x.save()
	return array
