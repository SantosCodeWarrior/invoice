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
from it import default_template as dt

import smbclient 
import os 
from shutil import copyfile    
import shutil
from smb import smb_structs
from smb.SMBConnection import SMBConnection
from nmb.NetBIOS import NetBIOS
smb_structs.SUPPORT_SMB2 = True
import urllib
import tempfile
import urllib2
from smb.SMBHandler import SMBHandler
from it import oldendorff_template as otp
from datetime import datetime

def master_inv(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'admin':
		login_user  	 = request.user
		get_data 		 = models.details_inw_details.objects.all()		
		inv_arr 		 = []
		remittance_array = []
		single_invoice 	 = []
		for t in get_data:			
			client_name			= t.client			
			get_client_id 		= models.Client.objects.filter(client_name=client_name,proj_name=t.proj_name).first()			
			get_invoice_data 	= models.invoice.objects.filter(proj_name=t.proj_name,client_id=get_client_id).order_by('invoice_no')
			
			for c in get_invoice_data:
				if c.invoice_no not in single_invoice:
					single_invoice.append(c.invoice_no)

			remittance_array.append({
				'id'	  		: t.id,
				'rem_id'  		: t.inward_id,
				'invoice_no'  	: t.invoice_no,
				'bank_chrgs'  	: t.bank_chrgs,
				'client'		: t.client,
				'remarks'		: t.remarks,
				'sub_amount' 	: t.sub_amount
				})
		
		for i in single_invoice:			
			inv_arr.append({				
				'invoice_no' : i,
				})

		context={
			'login_user' 	: login_user,
			'remitt_array' 	: remittance_array,
			'inv_arr'		: sorted(inv_arr),
		}		
		return render_to_response("invoice_display/master_inv.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')

def get_client_details(request):
	proj_name  	 = request.GET['proj_name']	
	if proj_name=='CHM':
		status = '0'
	else:
		status = '1'

	client_list  = models.Client.objects.filter(proj_name=proj_name,status=status).order_by('client_name').exclude(id=15584)
	single_array = []
	cl_arr 		 = []

	for x in client_list:		
		if x.client_name not in single_array:
			single_array.append(x.client_name)
		
	for i in single_array:
		cl_arr.append({
			'client_name' :  i
		})

	context={		
		'cl_array' : cl_arr,
	}
	return HttpResponse(json.dumps(cl_arr))

def get_client_proj_details(request):
	proj_name  		= request.GET['proj_name']
	invoice_no 		= request.GET['invoice_no']
	
	in_arr 		 	= []		
	cl_arr 		 	= []	
	
	invoice_details = models.invoice.objects.filter(invoice_no=invoice_no)
	for i in invoice_details:		
		in_arr.append({
			'client_name'   : i.client.client_name,
			'cl_id'			: i.client.id
		})

	client_details = models.Client.objects.all()
	for i in client_details:		
		cl_arr.append({
			'client_name'   : i.client_name,
			'cl_id'			: i.id
		})

	context={		
		'cl_array' : cl_arr,
		'in_arr'   : in_arr,
	}	
	return HttpResponse(json.dumps(context))


@csrf_exempt
def submit_remittance_master(request):
	get_in_date 	= json.loads(request.POST['get_in_date'])	
	select_bank 	= request.POST['select_bank']
	proj_name 		= json.loads(request.POST['proj_name'])	
	party_name 		= request.POST['party_name']
	get_amount 		= request.POST['get_amount']
	get_remarks     = request.POST['get_remarks']
	invoice_no   	= json.loads(request.POST['invoice_nox'])
	bank_chrgs   	= json.loads(request.POST['bank_chrgs'])
	amount   		= json.loads(request.POST['amount'])
	client   		= json.loads(request.POST['client'])
	remarks   		= json.loads(request.POST['remarks'])
	rowCount 		= json.loads(request.POST['rowCount'])	
	get_currency 	= json.loads(request.POST['get_currency'])
	get_rate 		= json.loads(request.POST['get_rate'])
	tot_amounts 	= json.loads(request.POST['tot_amounts'])	
	
	try:
		BANKIDsx 	= json.loads(request.POST['BANKIDx'])[0]
	except:
		BANKIDsx    = None	
	
	if BANKIDsx!=None:
		msg = 'done'
		check  = models.master_inw_data.objects.filter(bank_date=get_in_date,bank_id=BANKIDsx).count()
		if check!=0:
			db = models.master_inw_data.objects.filter(bank_date=get_in_date,bank_id=BANKIDsx).first()
		else:
			db = models.master_inw_data()

		db.total_amount = tot_amounts
		db.bank_name    = select_bank
		db.party_name   = party_name	
		db.bank_date 	= get_in_date	
		db.bank_id 		= BANKIDsx
		db.currency 	= get_currency
		db.rate 		= get_rate	
		db.save()

		for c in range(0,rowCount):		
			check_inw 	= models.details_inw_details.objects.filter(inward_id=db,invoice_no=invoice_no[c],client=client[c]).count()
			
			if check_inw!=0:
				inw_db 	=  models.details_inw_details.objects.filter(inward_id=db,invoice_no=invoice_no[c],client=client[c]).first()			
			else:
				inw_db 	= models.details_inw_details()			

			inw_db.sub_amount 	= amount[c]
			inw_db.invoice_no 	= invoice_no[c]
			inw_db.bank_chrgs 	= bank_chrgs[c]
			inw_db.remarks 		= remarks[c]
			inw_db.client 		= client[c]
			inw_db.inward   	= db
			inw_db.proj_name 	= proj_name[c]
			inw_db.bank_id 		= BANKIDsx
			inw_db.currency 	= get_currency
			inw_db.rate 		= get_rate		
		 	inw_db.save()
		else:
			msg = ''

		# Approval will be done from Madam
		
		# get_update_invoice 					= models.invoice.objects.filter(invoice_no=invoice_no[c],client_id=get_client_id.id,proj_name=proj_name).first()
		# get_update_invoice.received_date 		= get_in_date
		# get_update_invoice.payment_status 	= 'Paid'
		# get_update_invoice.save()


	return HttpResponse(json.dumps('done'))


def get_remittance_master(request):
	get_invoice_no  = request.GET['get_invoice_no']
	get_amount_data	= models.invoice.objects.filter(invoice_no=get_invoice_no)
	arr_list 		= []
	for c in get_amount_data:		
		amt 		= c.total_amount
		if amt:
			amt = amt
		else:
			amt = c.price
		client_name = c.client.client_name
		arr_list.append({
			'amount'		: amt,
			'client_name' 	: client_name,
			})

	context={
	'arr_list' : arr_list
	}
	return HttpResponse(json.dumps(context))


def view_remittance(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'admin':
		login_user  = request.user
		all_master 	= models.master_inw_data.objects.all()
		m_array    	= []
		for c in all_master:
			m_array.append({
				'id' 			: c.id,
				'bank_name' 	: c.bank_name,				
				'party_name' 	: c.party_name,
				'total_amount' 	: c.total_amount,
				'credit_date'   : c.bank_date,				
				'get_bank_id' 	: c.bank_id,
				'tt_currency' 	: c.currency,
				})

		context={
			'login_user' : login_user,	
			'm_array'  	 : m_array,		
		}	

		return render_to_response("invoice_display/view_remittance.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')


def get_remittance_id(request):
	remid 		= json.loads(request.GET['remid'])[0]	
	all_master 	= models.master_inw_data.objects.filter(id=remid)
	m_array    	= []	
	
	for c in all_master:		
		m_array.append({
			'id' 			: c.id,
			'bank_name' 	: c.bank_name,			
			'party_name' 	: c.party_name,
			'total_amount' 	: c.total_amount,
			'credit_date'   : str(c.bank_date),		
			'tot_currency'	: c.currency,
			'get_rate'		: c.rate,			
			})

	all_data    = []
	all_details = models.details_inw_details.objects.filter(inward_id=remid)
	total_data  = models.details_inw_details.objects.filter(inward_id=remid).count()

	for e in all_details:
		all_data.append({
			'sub_amount' : e.sub_amount,
			'invoice_no' : e.invoice_no,
			'bank_chrgs' : e.bank_chrgs,
			'proj_name'  : e.proj_name,
			'remarks'  	 : e.remarks,
			'client'  	 : e.client,
			'inward_id'  : remid,
			'e_id' 		 : e.id,			
			})

	context={
		'all_data' : all_data,
		'm_array'  : m_array,
		'tot_data' : total_data,
	}
	return HttpResponse(json.dumps(context))
		

def del_details(request):
	get_id 	= json.loads(request.GET['get_id'])
	models.details_inw_details.objects.filter(id=get_id).delete()
	print 'Deleting...',get_id


	return HttpResponse(json.dumps('done'))

def update_remittance_master(request):
	get_rem_id 		= json.loads(request.GET['rem_ids'])[0]	
	invoice_nox 	= json.loads(request.GET['invoice_nox'])
	bank_chrgs 		= json.loads(request.GET['bank_chrgs'])
	amount 			= json.loads(request.GET['amount'])
	client 			= json.loads(request.GET['client'])
	remarks 		= json.loads(request.GET['remarks'])
	rowCount 		= json.loads(request.GET['rowCount'])
	get_id 			= json.loads(request.GET['get_id'])
	get_rate 		= json.loads(request.GET['get_rate'])
	get_currency	= json.loads(request.GET['get_curr'])
	proj_name 		= json.loads(request.GET['proj_name'])
	ar_proj_c 		= json.loads(request.GET['ar_proj_c'])
	
	for c in range(0,rowCount):
		updt_master 	= models.master_inw_data.objects.filter(id=get_rem_id).first()
		check_details 	= models.details_inw_details.objects.filter(inward_id=updt_master,id=get_id[c]).count()
		if check_details!=0:
			up_db = models.details_inw_details.objects.filter(inward_id=updt_master,id=get_id[c]).first()
		else:
			up_db = models.details_inw_details()	

		up_db.sub_amount 	= amount[c]
		up_db.invoice_no 	= invoice_nox[c]
		up_db.bank_chrgs 	= bank_chrgs[c]
		up_db.remarks 		= remarks[c]
		up_db.client 		= client[c]
		up_db.inward   		= updt_master			
		up_db.currency 		= get_currency
		up_db.rate 			= get_rate
		if ar_proj_c[c]!=None:
			up_db.proj_name = ar_proj_c[c]
		else:
			up_db.proj_name = up_db.proj_name
	 	up_db.save()

	updt_master.currency 	= get_currency
	updt_master.rate 		= get_rate
	updt_master.save()

	return HttpResponse(json.dumps('done'))