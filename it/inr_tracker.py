from django.shortcuts import render
from django.shortcuts import render,render_to_response
from it import models
from django.http import HttpResponse
import json
from django.db.models import Count
from datetime import date,timedelta,datetime
from collections import Counter
import numpy as np
import decimal
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os
import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import requests
from num2words import num2words

#####################################################
import smtplib
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os,sys
from os import path
import re
import sys, ast
import subprocess
from subprocess import Popen, PIPE
import pprint
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import requests
import re
from bs4 import BeautifulSoup
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import pdfkit
import webbrowser
from django.db.models import Max
from django.db.models import Min
from shutil import copyfile
import shutil
from django.db.models import Sum
from time import strptime
from calendar import monthrange
from django.db import connection

from it import apj_template as apj
from it import clearlake_template as ct
from it import shell_template as sh
from it import vessel_template as vt
from django.db.models import Q


def inr_tracker(request):
	if request.user.is_authenticated():			
		login_user = request.user	
		context={
		'login_user' :  login_user
		}
		return render_to_response("invoice_display/inr_tracker.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')
	
	
@csrf_exempt
def filter_inr_tracker(request):
	login_user = request.user		
	import calendar

	#try:
	invoice_list    = []
	filter1         = ''	
	start_date 	   	= json.loads(request.POST['start_date'])
	end_date 	   	= json.loads(request.POST['end_date'])
	start_date_for  = datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y-%m-%d')
	end_date_for    = datetime.strptime(end_date,"%m/%d/%Y").strftime('%Y-%m-%d')
	unpaid_list    	= json.loads(request.POST['pad_unpaid_list'])
	project_list    = json.loads(request.POST['project_list'])

	
	if unpaid_list=='Paid' and project_list=='all':		
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',payment_status='Paid')
	elif unpaid_list=='unpaid' and project_list=='all':
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',payment_status=None)
	elif unpaid_list=='cancel' and project_list=='all':
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',payment_status='Cancel')		
	
	elif unpaid_list=='cancel' and project_list=='BOSS':
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',payment_status='Cancel',proj_name='BOSS')	
	elif unpaid_list=='Paid' and project_list=='BOSS':		
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',payment_status='Paid',proj_name='BOSS')
	elif unpaid_list=='unpaid' and project_list=='BOSS':
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',payment_status=None,proj_name='BOSS')
	
	elif unpaid_list=='cancel' and project_list=='CHM':
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',payment_status='Cancel',proj_name='CHM')	
	elif unpaid_list=='Paid' and project_list=='CHM':		
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',payment_status='Paid',proj_name='CHM')
	elif unpaid_list=='unpaid' and project_list=='CHM':
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',payment_status=None,proj_name='CHM')
	
	elif unpaid_list=='all' and project_list=='CHM':
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',proj_name='CHM')
	elif unpaid_list=='all' and project_list=='BOSS':
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR',proj_name='BOSS')

	else:		
		filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,inr='INR')	
	
	invoice_array   = []	
	invoice_details = models.invoice.objects.filter(filter1).order_by('-invoice_no')
	
	for xx in invoice_details:
		if xx.invoice_no not in invoice_array:
			invoice_array.append(xx.invoice_no)
	
	for i in invoice_array:
		tot_invoice	= models.invoice.objects.filter(invoice_no=i).aggregate(Sum('total_amount'))	
		x  = models.invoice.objects.filter(invoice_no=i,inr='INR').first()	
		
		if x.received_date:
			rece_date = str(x.received_date.strftime('%d/%b/%Y'))
			#color_fit = 'green'
		else:
			rece_date = ''
			#color_fit = ''


		if x.payment_status!='Cancel' and x.payment_status=='Paid' and x.received_date!=None:
			color_fit = 'green'
			show_file = 'none'
		elif x.payment_status=='Cancel' and x.payment_status!='Paid' and x.received_date==None:
			color_fit = 'red'
			show_file = 'none'
		elif x.payment_status!='Cancel' and x.payment_status=='' and x.received_date==None:
			color_fit = 'black'
			show_file = ''
		else:
			color_fit = ''
			show_file = ''

		
		if x.client_id!=125:
			if x.voyage_no=='' or x.voyage_no=="0":
				vessel_type = x.vessel_type
				voyage_no   = ''
			else:
				#vessel_type = x.ship_name
				if x.client.client_name=='Poompuhar Shipping Corporation Limited':
					voyage_no   = ''
					vessel_type = 'Poompuhar'
				# else:
				# 	voyage_no   = x.voyage_no
				# 	vessel_type = x.ship_name

				elif x.client.client_name=='TANGEDCO':
					voyage_no   = ''
					vessel_type = 'TANGEDCO'
				else:
					voyage_no   = x.voyage_no
					vessel_type = x.ship_name
		else:
			name = 'Poompuhar Shipping Corporation Limited'
			vessel_type = name[:9]
			voyage_no   = ''
	
		
		if x.month:
			split_month = (x.month).split('-')
			yearx  		= split_month[0][2:]
			monthx 		= split_month[1]				
			period_name = str(monthx)+'/'+str(yearx)				
		else:
			period_name = ''
		
		if x.payment_status=='Paid':
			show_button = 'none'
		else:
			show_button = ''

		img_logo    = '/static/img/pdf.png'

		if x.remark:
			comment = x.remark
		else:
			comment = ''

		#print '------',x.invoice_no
		if x.rate!=1:				
			if x.client.client_name=='Poompuhar Shipping Corporation Limited' or x.client.client_name=='TANGEDCO':					
				inr_rate = ''
			else:
				inr_rate = round(x.rate,1)
		else:
			inr_rate = ''

		if x.usd_amount:
			if x.client.client_name=='Poompuhar Shipping Corporation Limited' or x.client.client_name=='TANGEDCO':				
				usd_amt = ''
				
			else:
				usd_amt = x.usd_amount					
		else:
			usd_amt = x.price

		sm 		= models.invoice.objects.filter(invoice_no=i).aggregate(Sum('price'))	

		if x.total_amount:				
			tds  	= round((tot_invoice['total_amount__sum'])*10/100,1)#round(sm['price__sum']*10/100)#round(x.total_amount*10/100)
			igst 	= round(tot_invoice['total_amount__sum']*18/100) #round(x.total_amount*18/100) 
			#print '----',(tot_invoice['total_amount__sum']),'----',x.invoice_no
			net_inr = round((x.total_amount*x.rate*18)/100,1)#round((sm['price__sum']+igst)-tds)#round((x.total_amount+igst)-tds)				
			
			
			if x.client.client_name=='Poompuhar Shipping Corporation Limited' or x.client.client_name=='TANGEDCO': 
				tds  	= round((sm['price__sum'])*10/100,1)
				igst    = round(sm['price__sum']*18/100)
				net_inr = round(sm['price__sum']+igst)
				sub_inr = round(sm['price__sum']+igst)-(tds+(sm['price__sum'])*2/100)
				#inr+(cgst+sgst)-tds
				#print '=======INR',sm['price__sum']*18/100,'----',x.total_amount*x.rate,'---',tds
				#print '=======TDS',tds
			 	# print '=======IGST',round((sm['price__sum']+tds))
				#print '=======((INR+TDS+IGST)-(TDS+(2*INR/100)))'
			else:
				sub_inr = ''#round(igst+(x.price*x.rate),1)
				net_inr = round(((tot_invoice['total_amount__sum'])+igst)-tds,1)							
				igst    = round(tot_invoice['total_amount__sum']*18/100)					
				
		else:
			
			try:
				tds  	= round(tot_invoice['total_amount__sum']*10/100)#round(x.price*x.rate*10/100)
				igst 	= round(tot_invoice['total_amount__sum']*18/100)
				net_inr	= round((tot_invoice['total_amount__sum']+igst)-tds)#-(tds+(2*tot_invoice['total_amount__sum']*x.rate/100)))
				sub_inr = ''
			except:
				tds = 0
				igst = 0
				net_inr = 0
				sub_inr = ''



		if x.invoice_amount!=None:
			if x.client.client_name=='Poompuhar Shipping Corporation Limited' or x.client.client_name=='TANGEDCO':
				price_amt 	= x.total_amount
		
			else:
				price_amt = round(sm['price__sum'],1)#x.invoice_amount				
		else:
			if x.client.client_name=='Poompuhar Shipping Corporation Limited' or x.client.client_name=='TANGEDCO':									
				price_amt = round(sm['price__sum'],1)
				#price_amt = x.total_amount
			else:
				try:
					price_amt = tot_invoice['total_amount__sum'] #round(x.price*x.rate,1)
				except:
					price_amt = ''

		#((INR+TDS+IGST)-(TDS+(2*INR/100)))
		
		
		invoice_list.append({
			'id' 			: x.id,
			'invoice_no'   	: x.invoice_no, 
			'invoice_date' 	: str(x.invoice_date.strftime('%d-%b-%y')),#str(x.invoice_date.strftime('%d/%b/%Y')),
			'vessel_name'  	: vessel_type,
			'voyage_no'    	: voyage_no,
			'vm_name' 	   	: x.vm_name,			
			'client_name'  	: x.client.client_name,
			'invoice_amt'  	: x.invoice_amount,
			'rece_date'		: str(rece_date),
			'color_fit'     : color_fit,
			'proj_name'     : x.proj_name,
			'client_id'     : x.client_id,
			'show_button'   : show_button,
			'pool_types'    : x.vessel_type,#vessel_type,
			'url_pdf'		: x.url,
			'img_logo'    	: img_logo,
			'period_name'   : period_name,
			'voy_no'		: x.voyage_no,
			'total_amount'	: price_amt,#x.total_amount,
			'remark'		: comment,
			'show_file'     : show_file,
			'inr_rate'  	: inr_rate,
			'usd_amt' 		: usd_amt,
			'tds' 			: tds,
			'igst' 			: igst,
			'net_inr' 		: net_inr,
			'sub_inr' 		: sub_inr,				
			})

	try:
		max_date = end_date_for.strftime('%d/%m/%Y')
	except:
		max_date = '03/01/2021'

	#min_date = '04/01/2019'


	min_invoice_date = models.invoice.objects.filter(inr='INR').first()
	min_date 		 = min_invoice_date.invoice_date.strftime('%m/%d/%Y')
	
	context={
		'invoice_list' : invoice_list,
		'max_date'     : str(max_date),	
		'min_date'	   : str(min_date),	
		'login_user'   : str(login_user)
	}
	return HttpResponse(json.dumps(context))
	# except:
				
	# 	unpaid_list 	= 0		
	# 	context={
	# 		'invoice_list'	: invoice_list,
	# 		'max_date'     	: '',
	# 		'min_date'		: '',
	# 		'login_user'    : 0,
	# 	}
	# 	return HttpResponse(json.dumps(context))
	 
def delete_invoice_for_inr(request):
	getID 				= request.GET['getID']
	invoice_details 	= models.invoice.objects.filter(id=getID).first()
	del_invoice_details = models.invoice.objects.filter(invoice_no=invoice_details.invoice_no,proj_name=invoice_details.proj_name).delete()
		
	context={
		'msg'			 : 'done',
		'del_invoice_no' : invoice_details.invoice_no,
	}

	return HttpResponse(json.dumps(context))