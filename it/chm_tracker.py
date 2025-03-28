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
import time
def chm_tracker(request):
	#if request.user.is_authenticated():		
	login_user = request.user			
	context={
	'login_user' :  login_user
	}
	return render_to_response("invoice_display/chm_tracker.html",context)
	#if user.is_anonymous():
	#	return HttpResponseRedirect('/it/user_login')
#else:
	return HttpResponseRedirect('/it/user_login')
	
	
@csrf_exempt
def filter_chm_invoice_tracker(request):
	login_user = request.user	
	try:
		invoice_list  	= []
		filter1       	= ''	
		start_date 		= json.loads(request.POST['start_date'])
		end_date 		= json.loads(request.POST['end_date'])
		start_date_for  = datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y-%m-%d')
		end_date_for    = datetime.strptime(end_date,"%m/%d/%Y").strftime('%Y-%m-%d')
		unpaid_list    	= json.loads(request.POST['pad_unpaid_list'])
		try:
			start_date_for = json.loads(request.POST['curr_invodate'])[0]
		except:
			start_date_for =  datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y-%m-%d')

		#print '--------',start_date_for,'----',end_date_for
		

		if unpaid_list=='Paid':			
			filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,proj_name='CHM',usd='USD',payment_status='Paid')
		elif unpaid_list=='unpaid':
			filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,proj_name='CHM',usd='USD',payment_status=None)
		elif unpaid_list=='cancel':
			filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,proj_name='CHM',usd='USD',payment_status='Cancel')
		else:		
			filter1  = Q(invoice_date__gte=start_date_for,invoice_date__lte=end_date_for,proj_name='CHM',usd='USD')	
		#start_time = time.time()	
		invoice_details  = models.invoice.objects.filter(filter1).order_by('-invoice_no')		
		#print start_time-time.time()
		invoice_array = []
		for xx in invoice_details:
			if xx.invoice_no not in invoice_array:
				invoice_array.append(xx.invoice_no)

		#for x in invoice_details:
		for i in invoice_array:	
			x  = models.invoice.objects.filter(invoice_no=i).first()			
			if x.received_date:
				rece_date = str(x.received_date.strftime('%d/%b/%Y'))				
			else:
				rece_date = ''

			#print '------',x.received_date
				
			
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


			if x.client.client_name=='Navig8' or x.client.client_name=='Shell' or x.client.client_name=='Shell NWE' or x.client.client_name=='Ultranav' or x.client.client_name=='Litasco':
				vessel_type = x.account_type #x.vessel_type
			else:
				vessel_type = ""

			if x.payment_status=='Paid':
				show_button = 'none'
			else:
				show_button = ''

			img_logo    = '/static/img/pdf.png'
			
			if x.client.client_name=='Stena Bulk Veg Oil' or x.client.client_name=='Ultranav' or x.client.client_name=='Phillips 66' or x.client.client_name=='stena bulk':
			#if x.price_type!=None:				
				selected_price_type = str(x.client.client_name)+' ('+str(x.price_type)+')',
			else:
				selected_price_type = ''

			#print '----->>>>>>>>>>>>>>.',x.id
			
			
			if x.remark:
				comment = x.remark
			else:
				comment = ''

			try:
				disch_port = x.disch_port
			except:
				disch_port = ''

			try:
				disch_date = str(x.disch_date.strftime('%d-%b-%Y'))
			except:
				disch_date = ''

			if x.invoice_amount==None:				
				if x.client.client_name=='Litasco_Dubai':
					amt_price  = round(x.price*x.rate,0)
				else:
					amt_price  = x.price
			else:
				amt_price = x.invoice_amount

			ctx  = models.invoice.objects.filter(invoice_no=x.invoice_no).count()			
			if ctx>1:
				shp_name 	= ''
				voy_nos  	= ''
				disch_date 	= ''
				disch_port 	= ''
			else:
				shp_name 	= x.ship_name
				voy_nos  	= x.voyage_no
				disch_date 	= str(x.disch_date.strftime('%d-%b-%Y'))
				disch_port 	= x.disch_port


			try:
				voyID = x.voyage_id
			except:
				voyID = ''


			

			invoice_list.append({
				'id' 			: x.id,
				'invoice_no'   	: x.invoice_no, 
				'invoice_date' 	: str(x.invoice_date.strftime('%d-%b-%y')),#str(x.invoice_date.strftime('%d/%b/%Y')),
				'vessel_name'  	: shp_name, #x.ship_name,
				'voyage_no'    	: voy_nos, #x.voyage_no,
				'vm_name' 	   	: x.vm_name,
				'disch_port'   	: disch_port,
				'disch_date'   	: disch_date,
				'client_name'  	: x.client.client_name,
				'invoice_amt'  	: amt_price,
				'rec_date'		: rece_date,
				'color_fit'     : color_fit,
				'pool_name'     : vessel_type,
				'proj_name'     : x.proj_name,
				'client_id'     : x.client_id,
				'show_button'   : show_button,
				'pool_types'    : x.vessel_type,
				'url_pdf'		: x.url,
				'img_logo'    	: img_logo,
				'price_type'    : selected_price_type,
				'remark'		: comment,
				'show_file'     : show_file,
				'voyID'			: voyID,
				})

		max_date = end_date_for.strftime('%d/%m/%Y')
		min_date = '04/01/2019'
		context={
			'invoice_list' : invoice_list,
			'max_date'     : str(max_date),	
			'min_date'	   : str(min_date),	
			'login_user'   : login_user
		}		
		return HttpResponse(json.dumps(context))
	except:		
		#print '===========',datetime.strptime(start_date,"%m/%d/%Y"),'=======',datetime.strptime(end_date,"%m/%d/%Y")
		unpaid_list 	= 0
		start_date_for  = datetime.strptime(start_date,"%m/%d/%Y")
		end_date_for    = datetime.strptime(end_date,"%m/%d/%Y")
		context={
			'invoice_list' 	: invoice_list,
			'max_date'     	: str(start_date_for),
			'min_date'		: str(end_date_for),
				
		}
		return HttpResponse(json.dumps(context))
	

def delete_invoice_for(request):
	getID 				= request.GET['getID']
	invoice_details 	= models.invoice.objects.filter(id=getID).first()
	del_invoice_details = models.invoice.objects.filter(id=getID).delete()
	print '---------',getID
	context={
		'del_invoice_no' : invoice_details.invoice_no,
		'msg'			 : 'done'
	}
	

	return HttpResponse(json.dumps(context))


def invoice_paid_track(request):
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
		#print '----------',get_no,'---',ht
	except:
		pass
	

	return HttpResponse(json.dumps('done'))

def get_pdf_viewer(request):
	invoice_n 		= request.GET['inv']	
	url_link  		= models.invoice.objects.filter(invoice_no=invoice_n).first()	
	url 			= url_link.url
	# pt_invs 		= invoice_n.split('/')
	# invo1 			= pt_invs[0]
	# invo2 			= pt_invs[1]
	# merge_invoice 	= str(invo1)+'_'+str(invo2)
	# cl_name 		= url_link.client.client_name
	# fleet_name 		= url_link.account_type
	# if url_link.proj_name=='BOSS':
	# 	url = "/static/pdf/BIM/"+str(cl_name)+"/Online/"+str(merge_invoice)+"_"+str(cl_name)+".pdf"
	# if url_link.proj_name=='CHM':
	# 	url = "/static/pdf/HIM/"+str(cl_name)+"/Online/"+str(merge_invoice)+"_"+str(cl_name)+".pdf"

	print '--------',url
	

	return HttpResponse(json.dumps(url))