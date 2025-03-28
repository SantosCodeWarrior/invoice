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
from it.forms import DocumentForm

from PIL import Image

def payment_advice(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'admin':
		login_user  	= request.user
		client_array 	= []		
		qry 			= "SELECT client_name,proj_name,currency_type,id FROM invoice.it_client where status='1' group by client_name,proj_name,currency_type;"
		cursor 			= connection.cursor()
		cursor.execute(qry)
		client_details 	= cursor.fetchall()
		for f in client_details:			
			client_array.append({
				'cl_id'	  : f[3],
				'client'  : str(f[0])+' - '+str(f[1]),
				'cl_name' : f[0],
				})

		all_data = models.master_inw_data.objects.filter(flag=None).order_by('-id')
		view_arr = []
		currency_list = []
		for c in all_data:
			CHK = models.master_inw_data.objects.filter(inward_no=c.inward_no,flag=None).first()
			if CHK.image_file!='':
				show_icon = ''
			else:
				show_icon = 'none'
			try:
				cl_name = c.client_id.client_name
			except:
				cl_name = ''

			try:
				cl_id = c.client_id.id
			except:
				cl_id = ''
			#print '-------',c.txn_date
			view_arr.append({
				'id' 		: c.id,
				'cal_date'	: str(c.txn_date),
				'txn_date' 	: c.txn_date,
				'rate'		: c.rate,
				'amount'	: c.amount,
				'show_icon' : show_icon,
				'currency'	: c.currency,
				'proj_name'	: c.proj_name,
				'inward_no' : c.inward_no,
				'client' 	: cl_name,
				'remarks'	: c.remarks,				
				'view_link' : '/static/Advice_images/'+str(c.file_name),
				'client_id' : cl_id,
	 			})

		currency_details = models.currency_data.objects.all().order_by('currency')
		for x in currency_details:
			currency_list.append({
				'id' 			: x.id,
				'currency_name' : x.currency
			})
		

		context={
			'view_arr' 		: view_arr,
			'login_user'   	: login_user,
			'client_array' 	: client_array,
			'currency_list' : currency_list,
		}
		
		return render_to_response("invoice_display/payment_advice.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')

def submit_advice(request):
	n_rate 				= json.loads(request.GET['n_rate'])
	n_date 			 	= json.loads(request.GET['n_date'])
	n_amount 		 	= json.loads(request.GET['n_amount'])
	n_remarks 	 		= json.loads(request.GET['n_remarks'])
	n_inwardno 		 	= json.loads(request.GET['n_inwardno'])
	n_client_name 	 	= json.loads(request.GET['n_client_name'])
	n_currency_type  	= json.loads(request.GET['n_currency_type'])

	cl_split 			= n_client_name.split('-')
	get_client_name 	= cl_split[0]
	get_proj_name 		= cl_split[1]

	get_client_id 		= models.Client.objects.filter(client_name=get_client_name,currency_type=n_currency_type,status=1).first()
	
	chk = models.master_inw_data.objects.filter(inward_no=n_inwardno).count()
	
	if chk!=0:
		return HttpResponse(json.dumps('alert'))
		#db = models.master_inw_data.objects.filter(inward_no=n_inwardno,client_id_id=get_client_id).first()
	else:
		db = models.master_inw_data()

	
	db.txn_date 	= n_date
	db.amount   	= n_amount
	db.currency 	= n_currency_type
	db.remarks 		= n_remarks
	db.inward_no 	= n_inwardno
	db.proj_name 	= get_proj_name
	db.client_id	= get_client_id
	db.rate 		= n_rate
	db.flag 		= None
	db.save()

	m_chk  			= models.remittance_data.objects.filter(certificate_no=n_inwardno).count()
	#print '--------',
	if m_chk!=0:
		print '-'
		#return HttpResponse(json.dumps('alert'))
	else:
		m_submit	= models.remittance_data()

	m_submit.rate 				= n_rate	
	m_submit.remarks 			= n_remarks
	m_submit.currency 			= n_currency_type
	m_submit.client_name 		= get_client_name
	m_submit.total_amount 		= n_amount
	m_submit.inward_amount 		= n_amount
	m_submit.certificate_no 	= n_inwardno
	m_submit.net_amount_ref 	= n_amount
	m_submit.remittance_date 	= n_date
	m_submit.entry_date 		= datetime.now().date()
	m_submit.save()


	return HttpResponse(json.dumps('done'))

def delete_advice(request):
	get_id = json.loads(request.GET['get_id'])
	models.master_inw_data.objects.filter(id=get_id).delete()
	return HttpResponse(json.dumps('done'))

def edit_advice(request):
	n_date 			= json.loads(request.GET['x_date'])
	n_amount		= json.loads(request.GET['x_amount'])
	n_inwardno 		= json.loads(request.GET['x_inwardno'])
	n_client_name   = json.loads(request.GET['x_client_name'])
	n_client_id   	= json.loads(request.GET['x_client_name'])
	n_currency_type = json.loads(request.GET['x_currency_type'])
	n_remarks		= json.loads(request.GET['x_remarks'])
	n_idx			= json.loads(request.GET['x_idx'])
	x_rate			= json.loads(request.GET['x_rate'])
	#print '----------',n_currency_type
	
	get_client_id 	= models.Client.objects.filter(id=n_client_id,currency_type=n_currency_type,status=1).first()
	
	Udb 			= models.master_inw_data.objects.filter(id=n_idx).first()
	Udb.txn_date 	= n_date
	Udb.amount 		= n_amount
	Udb.currency 	= n_currency_type
	Udb.remarks 	= n_remarks
	Udb.inward_no 	= n_inwardno
	#Udb.proj_name 	= get_client_id.proj_name
	Udb.client_id_id = int(n_client_id)
	Udb.id 			= n_idx
	Udb.rate 		= x_rate
	Udb.save()


	m_chk  			= models.remittance_data.objects.filter(certificate_no=n_inwardno).count()
	
	if m_chk!=0:
		m_update	= models.remittance_data.objects.filter(certificate_no=n_inwardno).first()
	else:
		m_update	= models.remittance_data()

	i=0
	invce = ''

	for c in n_remarks.split('\n'):		
		invce = models.invoice.objects.filter(invoice_no=c).first()
		#= str(m_update)+'.invoice_no1'+str(i+1) = invce.invoice_no
		#v = vv
		#print '=====',v
		#m_update.invoice_no+str(i) = invce.invoice_no
		#m_update.services+str(i)   = invce.client.proj_name		
		i+=1
		
	
	m_update.rate 				= x_rate	
	m_update.remarks 			= n_remarks
	m_update.currency 			= n_currency_type
	m_update.client_id 			= n_client_id #n_client_name
	m_update.total_amount 		= n_amount
	m_update.inward_amount 		= n_amount
	m_update.certificate_no 	= n_inwardno
	m_update.net_amount_ref 	= n_amount
	m_update.remittance_date 	= n_date
	m_update.entry_date 		= datetime.now().date()
	m_update.save()
	#print '------------',datetime.now().date()

	
	return HttpResponse(json.dumps('done'))

def get_currency_type(request):
	get_proj_name	= json.loads(request.GET['get_proj_name'])
	get_client_name = json.loads(request.GET['get_client_name'])
	currency_dets 	= models.Client.objects.filter(client_name=get_client_name,status=1).first()
	if currency_dets.proj_name=='BOSS':
		gcurrecny_type = currency_dets.currency_type
		try:
			get_tax_details = currency_dets.tax
		except:
			get_tax_details = None
	if currency_dets.proj_name=='CHM':

		gcurrecny_type = currency_dets.currency_type
		try:
			get_tax_details = currency_dets.tax
		except:
			get_tax_details = None
	

	context={
	'get_tax_details' : get_tax_details,
	'gcurrecny_type'  : gcurrecny_type
	}

	return HttpResponse(json.dumps(context))

def get_uploading_file_name(request):
	get_ids		= json.loads(request.GET['get_id'])
	get_image 	= models.master_inw_data.objects.filter(id=get_ids,flag=None).first()
	shw_png 	= get_image.image_file	
	show_png    = '/static/Advice_images/'+str(get_image.file_name)
	
	filepath 	= '/var/www/html/invoice/it/static/Advice_images/'+str(get_image.file_name)
	img 		= Image.open(filepath)	
	width 		= img.width
	height 		= img.height
	

	context={
		'w' 		: str(width+70)+'px',
		'h' 		: str(height+8)+'%',
		'show_png' 	: show_png,
	} 
	
	
	return HttpResponse(json.dumps(context))

