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


def boss_tracker(request):
	if request.user.is_authenticated():			
		login_user = request.user	
		context={
		'login_user' :  login_user
		}		
		return render_to_response("invoice_display/boss_tracker.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')
	
	
@csrf_exempt
def filter_boss_invoice_tracker(request):	
	import calendar
	login_user = request.user	
	try:
		invoice_list    = []
		filter1         = ''	
		start_date 	   	= json.loads(request.POST['start_date'])
		end_date 	   	= json.loads(request.POST['end_date'])
		start_date_for  = datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y-%m-%d')
		end_date_for    = datetime.strptime(end_date,"%m/%d/%Y").strftime('%Y-%m-%d')
		unpaid_list    	= json.loads(request.POST['pad_unpaid_list'])
		

		if unpaid_list=='Paid':			
			filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,proj_name='BOSS',usd='USD',payment_status='Paid')
		elif unpaid_list=='unpaid':
			filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,proj_name='BOSS',usd='USD',payment_status=None)
		elif unpaid_list=='cancel':
			filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,proj_name='BOSS',usd='USD',payment_status='Cancel')
		else:		
			filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,proj_name='BOSS',usd='USD')	
		invoice_array = []	
		invoice_details  = models.invoice.objects.filter(filter1).order_by('-invoice_no')
		for xx in invoice_details:
			if xx.invoice_no not in invoice_array:
				invoice_array.append(xx.invoice_no)
		c = 0
		t=0
		for i in invoice_array:		
			#print '------------',i
			x  = models.invoice.objects.filter(invoice_no=i).first()	
			
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

			try:
				if x.client.client_name!='Shell':
					if x.voyage_no=='':
						vessel_type = x.vessel_type
					else:
						vessel_type = x.client.client_name		
						#total_amountprint '--------------',vessel_type, x.ship_name
				else:
					vessel_type = x.vessel_type
			except:
				vessel_type = ''

			

			if x.month:
				split_month = (x.month).split('-')
				yearx  		= split_month[0]
				monthx 		= split_month[1]
				last_month 	= calendar.monthrange(int(yearx),int(monthx))[1]
				month_name 	= calendar.month_abbr[int(monthx)]
				period_name = '01 '+str(month_name)+' to '+str(last_month)+' '+str(month_name)+' '+str(yearx)
			else:
				period_name = ''


			get_counter = models.invoice.objects.filter(invoice_no=i).aggregate(Count('qty'))
			ct_vessel   = get_counter['qty__count']
			
			if x.payment_status=='Paid':
				show_button = 'none'
			else:
				show_button = ''

			img_logo    = '/static/img/pdf.png'

			if x.remark:
				comment = x.remark
			else:
				comment = ''			


			if x.client.client_name=='Oldendorff' or x.client.client_name=='MM Solution' or x.client.client_name=='ALADIN EXPRESS (ALX) DMCC' or x.client.client_name=='Cliff Shipping' or x.client.client_name=='LIGHTHOUSE NAVIGATION PTE LTD' or x.client.client_name=='MSEA Amber LLC':
				amt = round(x.usd_amount,0)				

			else:
				if ct_vessel==1:
					amt = x.price*x.qty
				else:
					x_prices = models.invoice.objects.filter(invoice_no=i).aggregate(Sum('price'))
					amt 	 = x_prices['price__sum']#x.price*x.qty*ct_vessel
					#print '---->>>>>', x_prices['price__sum']

			try:
				cl_name = x.client.client_name
			except:
				cl_name = ''
			#print '---',amt,'---',x.client.client_name
			
			invoice_list.append({
				'id' 			: x.id,
				'invoice_no'   	: x.invoice_no, 
				'invoice_date' 	: str(x.invoice_date.strftime('%d-%b-%y')),#str(x.invoice_date.strftime('%d/%b/%Y')),
				'vessel_name'  	: x.ship_name,
				'voyage_no'    	: 0,#x.voyage_no,
				'vm_name' 	   	: x.vm_name,
				'client_name'  	: cl_name, #x.client.client_name,
				'invoice_amt'  	: x.invoice_amount,
				'rece_date'		: str(rece_date),
				'color_fit'     : color_fit,
				'proj_name'     : x.proj_name,
				'client_id'     : x.client_id,
				'show_button'   : show_button,
				'pool_types'    : vessel_type,
				'url_pdf'		: x.url,
				'img_logo'    	: img_logo,
				'period_name'   : period_name,
				'voy_no'		: 0, #x.voyage_no,
				'total_amount'	: amt, #x.total_amount,
				'remark'		: comment,
				'show_file'     : show_file,
				})
		max_date = end_date_for.strftime('%d/%m/%Y')
		min_date = '01/01/2013'
		context={
			'invoice_list' : invoice_list,
			'max_date'     : str(max_date),	
			'min_date'	   : str(min_date),	
			'login_user'   : login_user
		}
		return HttpResponse(json.dumps(context))
	except:
		#print '------',	x.invoice_no		
		unpaid_list 	= 0		
		context={
			'invoice_list'	: invoice_list,
			'max_date'     	: '',
			'min_date'		: '',
			'login_user'    : 0,
		}
	 	return HttpResponse(json.dumps(context))
	 
def delete_invoice_for_usd(request):
	getID 				= request.GET['getID']
	invoice_details 	= models.invoice.objects.filter(id=getID).first()
	del_invoice_details = models.invoice.objects.filter(invoice_no=invoice_details.invoice_no,proj_name=invoice_details.proj_name).delete()
		
	context={
		'msg'			 : 'done',
		'del_invoice_no' : invoice_details.invoice_no,
	}

	return HttpResponse(json.dumps(context))

	
def invoice_paid_track_usd(request):
	try:
		nox 				= json.loads(request.GET['nox'])
		gen_invoice_no 		= json.loads(request.GET['generated_invoice_no'])
		get_invoice_no 		= gen_invoice_no[0]
		get_no 				= nox[0]
		gt 					= models.invoice.objects.filter(invoice_no=get_invoice_no).first()
		gt.received_date 	= datetime.now().date()
		gt.payment_status 	= 'Paid'
		tot_paid 			= (gt.rate*gt.price*gt.qty)
		gt.invoice_amount 	= tot_paid
		gt.save()	
		ht 					= models.remittance_data.objects.filter(id=get_no).first()
		ht.approved 		= 'yes'
		ht.save()
		print '----------',get_invoice_no,'---',ht
	except:
		pass
	

	return HttpResponse(json.dumps('done'))