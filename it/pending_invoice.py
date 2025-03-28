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
import pprint


@csrf_exempt
def selected_pending_invoice_no(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'gmadam':
		clientID   = json.loads(request.GET['clientID'])
		proj_name  = json.loads(request.GET['proj_name'])
		ship_array = []
		vessel_arr = []
		vessel_det = []
		s_no 	   = 1		
		
		invoice_details = models.invoice.objects.filter(client_id=clientID,proj_name=proj_name,payment_status=None)
		for sh in invoice_details:
			if sh.invoice_no not in vessel_arr:
				vessel_arr.append(sh.invoice_no)
			
		for h in vessel_arr:
			# update_invoice  = models.invoice.objects.filter(invoice_no=h,client_id=clientID,proj_name=proj_name).first()
			# invoice_ct      = models.invoice.objects.filter(invoice_no=h,client_id=clientID,proj_name=proj_name).count()			
			# sum_qty         = models.invoice.objects.filter(invoice_no=h,client_id=clientID,proj_name=proj_name).aggregate(Sum('qty'))
			# if invoice_ct>1:
			#  	total_amount = update_invoice.price*update_invoice.rate*sum_qty['qty__sum']
			# else:
			#  	total_amount = update_invoice.price*update_invoice.rate

			

			in_det = models.invoice.objects.filter(client_id=clientID,proj_name=proj_name,invoice_no=h,payment_status=None).first()
			if in_det.vessel_type=='VLCC' and in_det.proj_name=='BOSS':
				ship_name = 'VLCC Fleet'
			elif in_det.vessel_type=='LR1' and in_det.proj_name=='BOSS':
				ship_name = 'LR1 Fleet'	
			elif in_det.vessel_type=='LR2' and in_det.proj_name=='BOSS':
				ship_name = 'LR2 Fleet'	
			elif in_det.vessel_type=='VLGC' and in_det.proj_name=='BOSS':
				ship_name = 'VLGC Fleet'
			elif in_det.vessel_type=='Tsakos' and in_det.proj_name=='BOSS':
				ship_name = 'Tsakos Fleet'
			else:
				ship_name = in_det.ship_name
			vessel_det.append({
				'ship_name'   : ship_name,
				'invoice_no'  : h,
				'voyage_no'   : in_det.voyage_no,	
				'client_name' : in_det.client.client_name,
				's_no'		  : s_no,
				'invoice_amt' : (in_det.price*in_det.rate),
				'vess_invoice': str(ship_name)+','+str(in_det.invoice_no),
				})
			s_no+=1

		context={
		'ship_array'   : vessel_det,		
		}
	
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')


@csrf_exempt
def generate_of_pending_invoice(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'gmadam':
		try:
			show_button     = ''
			msg             = ''
			checkbutton     = ''
			caption         = ''
			button          = ''
			total_amount    = ''
			invoice_list    = json.loads(request.POST['invoice_list'])
			rec_date 	    = request.POST['rec_date']
			invoice_cancel  = request.POST['invoice_cancel']
			invoice_amount  = request.POST['invoice_amount']
			remark 			= request.POST['payment_status']		
			checkbutton		= request.POST['submit_id']
			received_inr    = request.POST['e_received_inr']
			bank_charges    = request.POST['e_bank_charges']
			invoice_tds 	= request.POST['e_tds']
			e_proj_name 	= request.POST['e_proj_namex']
			e_id 			= request.POST['e_id']	
			client_id 		= request.POST['client_id']

			try:
				for_invoice_date  = datetime.strptime(rec_date, "%m/%d/%Y").strftime('%Y-%m-%d')
			except:
				for_invoice_date  = rec_date

			for x in invoice_list:
				update_invoice  			  = models.invoice.objects.filter(invoice_no=x,client_id=client_id,proj_name=e_proj_name).first()			
				update_invoice.received_inr   = received_inr
				update_invoice.bank_charges   = bank_charges
				update_invoice.payment_status = remark
				invoice_ct = models.invoice.objects.filter(invoice_no=x,client_id=client_id,proj_name=e_proj_name).count()			
				sum_qty = models.invoice.objects.filter(invoice_no=x,client_id=client_id,proj_name=e_proj_name).aggregate(Sum('qty'))	
				
				if invoice_ct>1:
				 	total_amount = update_invoice.price*update_invoice.rate*sum_qty['qty__sum']
				else:
				 	total_amount = update_invoice.price*update_invoice.rate

				if invoice_tds:
					update_invoice.tds = float(invoice_tds)
				else:
					tds = 0.0

				update_invoice.received_date  = datetime.now().date()		
				if invoice_cancel=='1':			
					update_invoice.cancel_invoice = '1'
					update_invoice.payment_status = None
					update_invoice.received_date  = None
					update_invoice.invoice_amount = None
					msg    = 'cancel'
					button = 'Submit'

				if invoice_cancel=='0':
					update_invoice.cancel_invoice = '0'
					update_invoice.payment_status = 'Paid'
					update_invoice.received_date  = for_invoice_date
					update_invoice.invoice_amount = invoice_amount
					msg    = 'ok'
					button = 'Unpaid'
					
				get_client_id 	= models.Client.objects.filter(id=request.POST['client_id']).first()
				if get_client_id.currency_type=='USD':
					update_invoice.usd = 'USD'
				else:
					update_invoice.inr = 'INR'
				
				check = models.invoice.objects.filter(invoice_no=x).count()
				if check>0:
					show_button= 'none'
				else:
					show_button = ''

				if checkbutton=="Unpaid":				
					update_invoice.cancel_invoice = 0
					update_invoice.payment_status = None
					update_invoice.received_date  = None
					update_invoice.invoice_amount = None				
					msg = 'unpaid'			
				update_invoice.save()


				
		except:
			pass

		context={
		'show_button' : show_button,
		'msg'     	  : msg,	
		'checkbutton' : checkbutton,	
		'caption'     : button,
		'total_amount': total_amount,
		}

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')



def get_invoice_calc(request):
	try:
		get_invoice_no = json.loads(request.GET['get_invoice_no'])
		client_id      = json.loads(request.GET['client_id'])
		e_proj_name    = json.loads(request.GET['e_proj_name'])
		arr_details    = []	
		for x in get_invoice_no:		
			if x not in arr_details:			
				arr_details.append(x)

		sums=0
		for j in arr_details:		
			update_invoice  = models.invoice.objects.filter(invoice_no=j,client_id=client_id,proj_name=e_proj_name).first()			
			invoice_ct 		= models.invoice.objects.filter(invoice_no=j,client_id=client_id,proj_name=e_proj_name).count()			
			sum_qty   	    = models.invoice.objects.filter(invoice_no=j,client_id=client_id,proj_name=e_proj_name).aggregate(Sum('qty'))		
			if invoice_ct>1:
			 	total_amount = update_invoice.price*update_invoice.rate*sum_qty['qty__sum']
			 	sums+=total_amount
			else:
			 	total_amount = update_invoice.price*update_invoice.rate
			 	sums+=total_amount			 	

		context={
		'total_amount' : sums
		}
	except:
		context={
		'total_amount' : 0
		}
		

	return HttpResponse(json.dumps(context))