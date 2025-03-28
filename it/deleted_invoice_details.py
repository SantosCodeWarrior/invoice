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

@csrf_exempt
def del_invoice_log(request):
	if request.user.is_authenticated():
		# deleted_log = models.delete_vessel_details.objects.all()
		del_log       = []
		# for e in deleted_log:
		# 	del_invoice_date = e.delete_date.strftime("%d-%b-%Y")
		# 	gen_invoice_date = e.invoice_date.strftime("%d-%b-%Y")
		# 	cl_details = models.Client.objects.filter(proj_name=e.proj_name,currency_type = e.currency_type,id=e.client_id_id).first()
		# 	del_log.append({
		# 		'invoice_date' : str(gen_invoice_date),
		# 		'deleted_date' : str(del_invoice_date),
		# 		'invoice_no'   : e.invoice_no,
		# 		'ship_name'    : e.ship_name,
		# 		'proj_name'    : e.proj_name,
		# 		'currency'	   : e.currency_type,
		# 		'client_name'  : cl_details.client_name,
		# 		'remarks'      : e.remarks
		# 		})
		max_invoice_date = models.invoice.objects.filter(client_id=64).aggregate(Max('invoice_date'))
		get_max_date 	 = (max_invoice_date['invoice_date__max'])		
		qry    			 = "SELECT vessel_type,count(vessel_type),invoice_date,invoice_no,month,sum(price*rate),price,month,qty from it_invoice where client_id='64' and invoice_date='"+str(get_max_date)+"' and cancel_invoice=0 group by vessel_type order by invoice_no;"
		cursor 			 = connection.cursor()
		cursor.execute(qry)
		invoice_details  = cursor.fetchall()
		#print qry
		for v in invoice_details:
			qry1    	 = "SELECT sum(price*rate) from it_invoice where client_id='64' and invoice_date='"+str(get_max_date)+"' and cancel_invoice=0";
			#print qry1
			cursor 		 = connection.cursor()
			cursor.execute(qry1)
			f_details 	 = cursor.fetchone()
			f_amount 	 = f_details[0]
			
			split_month  = v[7].split('-')
			get_year 	 = split_month[0]
			month_names  = str(v[2].strftime("%b"))
			del_log.append({
				'account_name' : v[0],
				'no_of_vessel' : v[1],
				'invoice_date' : str(v[2].strftime("%d-%m-%Y")),
				'invoice_no'   : v[3],	
				'month_name'   : 'Summary ('+str(month_names)+' '+str(get_year)+') Shell',
				'amount'	   : v[5],
				'price'	  	   : v[6],
				'qty'		   : v[8],				
			})
		
		
		context={
		  'del_log' 	: del_log,	
		  'tot_amt'		: f_amount	  
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')


@csrf_exempt
def total_deleted_chm_usd(request):
	if request.user.is_authenticated():
		del_invoice_details  = models.delete_vessel_details.objects.filter(currency_type='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31')
		del_details 		 = []
		for x in del_invoice_details:
			cl_details 		 = models.Client.objects.filter(proj_name=x.proj_name,currency_type = x.currency_type,id=x.client_id_id).first()
			del_invoice_date = x.delete_date.strftime("%d-%b-%Y")
			gen_invoice_date = x.invoice_date.strftime("%d-%b-%Y")
			del_details.append({
				'invoice_no'  : x.invoice_no,
				'vessel_name' : x.ship_name,
				'delete_date' : str(del_invoice_date),
				'gen_datex'   : str(gen_invoice_date),
				'proj_name'   : x.proj_name,
				'client_name' : cl_details.client_name,	
				'price' 	  : x.price,
				'status' 	  : 'DELETED'
				})	
		context={
		'del_details' : del_details
		}	

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')


@csrf_exempt
def total_deleted_inr(request):
	if request.user.is_authenticated():
		del_invoice_details  = models.delete_vessel_details.objects.filter(currency_type='INR',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31')
		del_details 		 = []
		for x in del_invoice_details:
			cl_details 		 = models.Client.objects.filter(proj_name=x.proj_name,currency_type = x.currency_type,id=x.client_id_id).first()
			del_invoice_date = x.delete_date.strftime("%d-%b-%Y")
			gen_invoice_date = x.invoice_date.strftime("%d-%b-%Y")
			del_details.append({
				'invoice_nox'  : x.invoice_no,
				'vessel_namex' : x.ship_name,
				'delete_datex' : str(del_invoice_date),
				'gen_datexx'   : str(gen_invoice_date),
				'proj_namex'   : x.proj_name,
				'client_namex' : cl_details.client_name,	
				'pricex' 	   : x.price,
				'statusx' 	   : 'DELETED'
				})	
		context={
		'del_details' : del_details
		}	

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def entry_for_price_type(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'gmadam':
		e_price_type 	= request.GET['e_price_type']
		check_type 		= models.price_type_details.objects.filter(price_type=e_price_type).count()		
		if check_type==1:
			price_entry = models.price_type_details.objects.filter(price_type=e_price_type).first()
			msg = 'no'
		else:
			price_entry = models.price_type_details()
			msg = 'done'
		price_entry.price_type 	= e_price_type
		price_entry.save()
		return HttpResponse(json.dumps(msg))
	else:
		return HttpResponseRedirect('/it/user_login')


def folder_list(request):
	import os
	path   		= "/var/www/html/invoice/it/static/pdf/"
	e_name    	= request.GET['e_name']
	proj_name 	= request.GET['proj_name']

	if proj_name=='BOSS':
		tag_name = 'BIM'		
	else:
		tag_name = 'HIM'


	files  = []		
	for r, d, f in os.walk(path):
		for file in f:					
			if '.pdf' in file:
				files.append(os.path.join(r, file))		
			if '.xlsx' in file:
				files.append(os.path.join(r, file))			
					
	folder_details  = []
	ax   = []	
	num  = ''
	arr  = []
	remove_space = ''
	for f in files:
		ss = f.split('pdf/')
		aa = ss[1:]
		x  = aa[0].split('/')

		if e_name==x[0]:
			ax = x[1]
			
			if x[0].isspace()==False:
				remove_space = x[0]				
				pdf_name   	 = ('%20').join(str(remove_space).split())
				space_name   = pdf_name
				number       = str(x[1].rsplit('_', 1)[0])+'_'
				url 	     = '/static/pdf/'+str(tag_name)+'/'+str(pdf_name)+'/Online/'+str(number)+str(pdf_name)+".pdf"
				icon         = '/static/img/pdf.png'
				
				if x[1].endswith('.xlsx')==True:
					number 	   = str(x[1].rsplit('_', 1)[0])+'_'		
					num    	   = str(x[1].rsplit('_', 1)[0])							
					url 	   = '/static/pdf/'+str(pdf_name)+'/Online/'+str(x[1])				
					icon 	   = '/static/img/excel.png'
					space_name = pdf_name
				else:
					pdf_name   = pdf_name
					url        = '/static/pdf/'+str(tag_name)+'/'+str(pdf_name)+'/Online/'+str(number)+str(pdf_name)+".pdf"	
					icon       = '/static/img/pdf.png'
					space_name = pdf_name
			else:				
				pdf_name    = pdf_name
				url 	    =  '/static/pdf/'+str(tag_name)+'/'+str(x[0])+'/Online/'+str(number)+str(pdf_name)+".pdf"	
				icon 	 	= '/static/img/pdf.png'
				space_name  = pdf_name	
			
			
			if x[0]!='Poompuhar Shipping Corporation Limited':				
			 	urlx = '/static/pdf/'+str(tag_name)+'/'+str(x[0])+'/Online/'+str(number)+str(x[0])+".pdf"			 	
			else:
			 	urlx = '/static/pdf/'+str(tag_name)+'/Poompuhar Shipping Corporation Limited'+'/Online/poompuhar_template_'+str(num)+".xlsx"			
			
			invoice_details = models.invoice.objects.filter(url=urlx,cancel_invoice=0).first()
			
			if invoice_details:			
				if invoice_details.proj_name==proj_name:
					invoice_date    = invoice_details.invoice_date.strftime("%d-%b-%Y")
					currency_type   = invoice_details.client.currency_type
					proj_name 		= invoice_details.proj_name	
					invoice_no      = invoice_details.invoice_no
					folder_details.append({		
						'folder_name'  : x[0],
						'pdf_link'     : ax,
						'folder_icon'  : '/static/img/folder.png/',
						'pdf_icon'     : icon,#'/static/img/pdf.png',
						'open_link'    : f,
						'file_name'    : ax,
						'url'		   : url,
						'invoice_date' : str(invoice_date),
						'currency_type': currency_type,
						'proj_name'    : proj_name,
						'invoice_no'   : invoice_no,					
					})

		context= {
		'folder_details' : sorted(folder_details)
		}

	return HttpResponse(json.dumps(context))



def folder_listx_for_boss(request):	
	path   = "/var/www/html/invoice/it/static/pdf/"
	e_name    = request.GET['e_name']
	proj_name = request.GET['proj_name']

	if proj_name=='BOSS':
		tag_name = 'BIM'		
	else:
		tag_name = 'HIM'

	print '------------',	tag_name	
	
	files  = []		
	for r, d, f in os.walk(path):
		for file in f:					
			if '.pdf' in file:
				files.append(os.path.join(r, file))		
			if '.xlsx' in file:
				files.append(os.path.join(r, file))			
					
	folder_list_boss  = []
	ax   = []	
	num  = ''
	arr  = []
	remove_space = ''
	for f in files:
		ss = f.split('pdf/')
		aa = ss[1:]
		x  = aa[0].split('/')
		if e_name==x[0]:
			ax = x[1]
			if x[0].isspace()==False:
				remove_space = x[0]
				pdf_name   	 = ('%20').join(str(remove_space).split())
				space_name   = pdf_name
				number       = str(x[1].rsplit('_', 1)[0])+'_'
				url 	     = '/static/pdf/'+str(tag_name)+'/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"
				icon         = '/static/img/pdf.png'				
			else:
				pdf_name    = pdf_name
				url 	    =  '/static/pdf/'+str(tag_name)+'/'+str(x[0])+'/'+str(number)+str(pdf_name)+".pdf"	
				icon 	 	= '/static/img/pdf.png'
				space_name  = pdf_name
				print '========',url

			# if x[1].endswith('.xlsx')==True:
			# 		number 	   = str(x[1].rsplit('_', 1)[0])+'_'		
			# 		num    	   = str(x[1].rsplit('_', 1)[0])							
			# 		url 	   = '/static/pdf/'+str(pdf_name)+'/'+str(x[1])				
			# 		icon 	   = '/static/img/excel.png'
			# 		space_name = pdf_name
			# else:
			# 	pdf_name   = pdf_name
			# 	url        = '/static/pdf/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"	
			# 	icon       = '/static/img/pdf.png'
			# 	space_name = pdf_name
			
			
			if x[0]!='Poompuhar Shipping Corporation Limited':				
			 	urlx = '/static/pdf/'+str(tag_name)+'/'+str(x[0])+'/'+str(number)+str(x[0])+".pdf"			 	
			else:
			 	urlx = '/static/pdf/'+str(tag_name)+'/Poompuhar Shipping Corporation Limited'+'/poompuhar_template_'+str(num)+".xlsx"			
			
			invoice_details = models.invoice.objects.filter(url=urlx,cancel_invoice=0).first()			
			if invoice_details:			
				if invoice_details.proj_name==proj_name:
					invoice_date    = invoice_details.invoice_date.strftime("%d-%b-%Y")
					currency_type   = invoice_details.client.currency_type
					proj_name 		= invoice_details.proj_name	
					invoice_no      = invoice_details.invoice_no
					folder_list_boss.append({		
						'folder_name'  : x[0],
						'pdf_link'     : ax,
						'folder_icon'  : '/static/img/folder.png/',
						'pdf_icon'     : icon,#'/static/img/pdf.png',
						'open_link'    : f,
						'file_name'    : ax,
						'url'		   : url,
						'invoice_date' : str(invoice_date),
						'currency_type': currency_type,
						'proj_name'    : proj_name,
						'invoice_no'   : invoice_no,					
					})

	context= {
	'folder_list_boss' : sorted(folder_list_boss)
	}

	print '========',folder_list_boss
	return HttpResponse(json.dumps(context))


# def folder_listx_for_boss(request):
	
# 	path   = "/var/www/html/invoice/it/static/pdf/"
# 	e_name = request.GET['e_name']
# 	proj_name  = request.GET['proj_name']	
# 	files  = []		
# 	for r, d, f in os.walk(path):
# 		for file in f:			
# 			if '.pdf' in file:
# 				files.append(os.path.join(r, file))
					
# 	folder_list_boss  = []
# 	ax = []	
# 	for f in files:		
# 		ss = f.split('pdf/')
# 		aa = ss[1:]
# 		x = aa[0].split('/')
# 		if e_name==x[0]:
# 			ax = x[1]
			
# 			if ax == "Stena Weco":
# 				space_name = 'Stena%20Weco'	
# 			else:
# 				space_name = ax

# 			aaaaa = x[1].rsplit('_', 1)[1]

# 			yt = aaaaa.replace('.pdf','')
# 			if yt=="Stena Weco":
# 				pdf_name = 'Stena%20Weco'
# 				number = str(x[1].rsplit('_', 1)[0])+'_'			
# 				url = '/static/pdf/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"	
# 			elif yt=='Diamond S Shipping':
# 				pdf_name = 'Diamond%20S%20Shipping'
# 				number = str(x[1].rsplit('_', 1)[0])+'_'			
# 				url = '/static/pdf/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"	
# 			elif yt=='stena bulk':
# 				pdf_name = 'stena%20bulk'
# 				number = str(x[1].rsplit('_', 1)[0])+'_'			
# 				url = '/static/pdf/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"	
# 			elif yt=='Shell NWE':
# 				pdf_name = 'Shell%20NWE'
# 				number = str(x[1].rsplit('_', 1)[0])+'_'			
# 				url = '/static/pdf/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"	
# 			elif yt=='Essar Oil':
# 				pdf_name = 'Essar%20Oil'
# 				number = str(x[1].rsplit('_', 1)[0])+'_'			
# 				url = '/static/pdf/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"	
# 			elif yt=='Navig8 Chemical':
# 				pdf_name = 'Navig8%20Chemical'
# 				number = str(x[1].rsplit('_', 1)[0])+'_'			
# 				url = '/static/pdf/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"	
# 			elif yt=='Koch Shipping':
# 				pdf_name = 'Koch%20Shipping'
# 				number = str(x[1].rsplit('_', 1)[0])+'_'			
# 				url = '/static/pdf/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"
# 			# elif yt=='Shell':
# 			# 	pdf_name = 'Shell'
# 			# 	number = str(x[1].rsplit('_', 1)[0])+'_'			
# 			# 	url = '/static/pdf/'+str(pdf_name)+'/'+str(number)+str(pdf_name)+".pdf"
			

# 			else:
# 				pdf_name = yt
# 				url = '/static/pdf/'+str(x[0])+'/'+str(space_name)
			
# 			if x[0]=="Stena Weco":
# 				name_only = 'Stena%20Weco'
# 			else:
# 				name_only = x[0]



# 			urlx = '/static/pdf/'+str(x[0])+'/'+str(ax)			
			
# 			invoice_details = models.invoice.objects.filter(url=urlx,cancel_invoice=0).first()
# 			if invoice_details:
# 				if invoice_details.proj_name==proj_name:
# 					invoice_date    = invoice_details.invoice_date.strftime("%d-%b-%Y")
# 					currency_type   = invoice_details.client.currency_type
# 					proj_name 		= invoice_details.proj_name	
# 					invoice_no      = invoice_details.invoice_no
				
# 					folder_list_boss.append({		
# 						'folder_name'  : x[0],
# 						'pdf_link'     : ax,
# 						'folder_icon'  : '/static/img/folder.png/',
# 						'pdf_icon'     : '/static/img/pdf.png',
# 						'open_link'    : f,
# 						'file_name'    : ax,
# 						'url'		   : url,
# 						'invoice_date' : str(invoice_date),
# 						'currency_type': currency_type,
# 						'proj_name'    : proj_name,
# 						'invoice_no'   : invoice_no,					
# 					})

# 		context= {
# 		'folder_list_boss' : sorted(folder_list_boss)
# 		}
# 	return HttpResponse(json.dumps(context))