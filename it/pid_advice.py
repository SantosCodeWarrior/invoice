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

def pid_advice(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'admin':
		login_user  	= request.user
		client_array 	= []		
		qry 			= "SELECT client_name,proj_name,currency_type FROM invoice.it_client where status='1' group by client_name,proj_name,currency_type;"
		cursor 			= connection.cursor()
		cursor.execute(qry)
		client_details 	= cursor.fetchall()
		for f in client_details:			
			client_array.append({
				'client'  : str(f[0])+'-'+str(f[1])+'-'+str(f[2]),
				'cl_name' : f[0],
				})

		all_data = models.master_inw_data.objects.filter(flag='PID').order_by('id')
		view_arr = []
		for c in all_data:
			CHK = models.master_inw_data.objects.filter(inward_no=c.inward_no,flag='PID').first()
			if CHK.image_file!='':
				show_icon = ''
			else:
				show_icon = 'none'
			#print '------',str(c.txn_date),'---',c.txn_date
			view_arr.append({
				'id' 		: c.id,
				'cal_date'	: str(c.txn_date),
				'txn_date' 	: c.txn_date,
				'amount'	: c.amount,
				'show_icon' : show_icon,
				'currency'	: c.currency,
				'proj_name'	: c.proj_name,
				'inward_no' : c.inward_no,
				'client' 	: c.client_id.client_name,
				'remarks'	: c.remarks,
				'rate'		: c.rate,				
				'view_link' : '/static/Advice_images/'+str(c.file_name)
	 			})
		

		context={
			'view_arr' 		: view_arr,
			'login_user'   	: login_user,
			'client_array' 	: client_array,
		}
		
		return render_to_response("invoice_display/pid_advice.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')

def pid_submit_advice(request):
	n_date 			 	= json.loads(request.GET['n_date'])
	n_amount 		 	= json.loads(request.GET['n_amount'])
	n_inwardno 		 	= json.loads(request.GET['n_inwardno'])
	n_client_name 	 	= json.loads(request.GET['n_client_name'])
	n_currency_type  	= json.loads(request.GET['n_currency_type'])
	n_remarks 	 		= json.loads(request.GET['n_remarks'])
	n_rate 	 			= json.loads(request.GET['n_rate'])
	cl_split 			= n_client_name.split('-')
	get_client_name 	= cl_split[0]
	get_proj_name 		= cl_split[1]
	get_client_id 		= models.Client.objects.filter(client_name=get_client_name,currency_type=n_currency_type,status=1).first()
	#print '-----',get_client_name,'---',n_currency_type
	chk = models.master_inw_data.objects.filter(inward_no=n_inwardno,client_id_id=get_client_id).count()
	
	if chk!=0:
		db = models.master_inw_data.objects.filter(inward_no=n_inwardno,client_id_id=get_client_id).first()
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
	db.flag 		= 'PID'
	db.save()

	return HttpResponse(json.dumps('done'))

def pid_delete_advice(request):
	get_id = json.loads(request.GET['get_id'])
	models.master_inw_data.objects.filter(id=get_id).delete()
	return HttpResponse(json.dumps('done'))

def pid_edit_advice(request):
	n_date 			= json.loads(request.GET['x_date'])
	n_amount		= json.loads(request.GET['x_amount'])
	n_inwardno 		= json.loads(request.GET['x_inwardno'])
	n_client_name   = json.loads(request.GET['x_client_name'])
	n_currency_type = json.loads(request.GET['x_currency_type'])
	n_remarks		= json.loads(request.GET['x_remarks'])
	n_idx			= json.loads(request.GET['x_idx'])
	x_rate			= json.loads(request.GET['x_rate'])
	
	#print '-----',n_client_name,'----',n_currency_type
	
	get_client_id 	= models.Client.objects.filter(client_name=n_client_name,currency_type=n_currency_type,status=1).first()
	Udb 			= models.master_inw_data.objects.filter(id=n_idx).first()
	Udb.txn_date 	= n_date
	Udb.amount 		= n_amount
	Udb.currency 	= n_currency_type
	Udb.remarks 	= n_remarks
	Udb.inward_no 	= n_inwardno
	try:
		Udb.proj_name 	= get_client_id.proj_name
	except:
		return HttpResponse(json.dumps('error'))

	Udb.client_id 	= get_client_id
	Udb.id 			= n_idx
	Udb.rate 		= x_rate
	Udb.save()

	
	return HttpResponse(json.dumps('done'))

def pid_get_currncy_type(request):
	get_proj_name	= json.loads(request.GET['get_proj_name'])
	get_client_name = json.loads(request.GET['get_client_name'])
	currency_dets 	= models.Client.objects.filter(client_name=get_client_name,status=1).first()
	if currency_dets.proj_name=='BOSS':
		gcurrecny_type = currency_dets.currency_type
	if currency_dets.proj_name=='CHM':
		gcurrecny_type = currency_dets.currency_type

	return HttpResponse(json.dumps(gcurrecny_type))


def get_upload_file_name(request):
	get_ids		= json.loads(request.GET['get_id'])
	get_image 	= models.master_inw_data.objects.filter(id=get_ids).first()
	shw_png 	= get_image.image_file	
	show_png    = '/static/Advice_images/'+str(get_image.file_name)
	print '----',shw_png
	

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


def get_client_currency_handler(request):
	client_name 		= request.GET['client_name']
	x_proj_name 		= request.GET['proj_name']
	split_proj_nm 		= x_proj_name.split('-')
	proj_name 			= split_proj_nm[1].strip()
	get_client 			= models.Client.objects.filter(client_name=client_name,proj_name=proj_name).first()
	get_currency_type 	= get_client.currency_type

	return HttpResponse(json.dumps(get_currency_type))