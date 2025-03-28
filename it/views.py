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
import requests
import pytz

def dashboard(request):	
	#print '----',models.Users.objects.filter(user = request.user)[0].user_type
	if request.user.is_authenticated():
		#print '---------Admin'
		return render_to_response("admin.html", {})
	elif request.user.is_authenticated():		
		return render_to_response("admin.html", {})
	elif request.user.is_authenticated():
		#print '-------Gamda'
		return render_to_response("base.html", {})

# def fetching_data_from_api(request):
# 	if request.user.is_authenticated():
# 		#api_url 	= "http://0.0.0.0:8000/hb/get_chm_data/"
# 		api_url 	 = "https://chm.bwesglobal.com/hb/get_chm_data/"
# 		api_method  = "GET"
# 		parameters  = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
# 		response    = requests.get(api_url, params=parameters,verify=False)
# 		return HttpResponse(response.content)
# 	else:
# 		return HttpResponseRedirect('/it/user_login')

def welcome(request):
	if request.user.is_authenticated():
		login_user 	= request.user
		
		
		context={		
			'login_user'   : login_user
		}
		return render_to_response("invoice_display/chm/welcome.html", context)
	else:
		return HttpResponseRedirect('/it/user_login')

def index(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'santosht':
		invoice_details = models.invoice.objects.filter(invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').order_by('invoice_no')
		invoice_array 			= []
		boss_appen 				= []
		boss_unpaid_appen 		= []
		boss_total_appen 		= []
		check_counter 			= []
		chm_total_paid 			= 0
		boss_total_paid 		= 0
		unpaid_chm_total_paid 	= 0
		unpaid_boss_total_paid 	= 0
		total_boss_paids 		= 0
		cancel_invoice_boss 	= 0
		cancel_invoice_chm 		= 0
		counter 				= 0
		chm_paid      			= []
		check_chm     			= []
		chm_cancelled 			= []
		chm_usd 				= []
		login_user 				= request.user
		for i in invoice_details:
			if i.invoice_no not in check_counter:
				if i.inr=='INR' and i.usd==None:
					check_counter.append(i.invoice_no)
			if i.invoice_no not in chm_usd:
				if i.inr==None and i.usd=='USD':
					chm_usd.append(i.invoice_no)

			client_details = models.Client.objects.filter(id=i.client_id,status=1).first()
			if i.payment_status=='Paid':
				if i.proj_name=='CHM':
					if i.invoice_no not in chm_paid:
						chm_paid.append(i.invoice_no)

				elif i.proj_name=='BOSS':
					if i.invoice_no not in boss_appen:
						boss_appen.append(i.invoice_no)

			elif i.payment_status==None:
				if i.proj_name=='CHM':
					if i.invoice_no not in check_chm:
						check_chm.append(i.invoice_no)
						#print '__',check_chm

				elif i.proj_name=='BOSS':
					if i.invoice_no not in boss_unpaid_appen:
						boss_unpaid_appen.append(i.invoice_no)

			elif i.payment_status=='Cancel':
				if i.proj_name=='CHM':
					if i.invoice_no not in chm_cancelled:
						chm_cancelled.append(i.invoice_no)

				elif i.proj_name=='BOSS':
					if i.invoice_no not in boss_total_appen:
						boss_total_appen.append(i.invoice_no)

			counter+=1



		ctc=0
		for we in check_chm:
			if we>1:
				ctc+=1
		unpaid_chm_total_paid = int(ctc)		

		ctp=0
		for w in chm_paid:
			ctp+=1

		chm_total_paid = ctp

		ct=0
		for p in boss_total_appen:
			if p>1:
				ct+=1
		total_invoice_of_boss = ct

		can=0
		for ssa in chm_cancelled:
			can+=1
		cancel_invoice_chm=can

		v=0
		for r in boss_unpaid_appen:
			if r>1:
				v+=1
		unpaid_boss_total_paid=v

		t=0
		for x in boss_appen:
			if x>1:
				t+=1
		boss_total_paid = t
		total_invoice_chm = 2

		z=0
		for s in check_counter:
			if s>1:
				z+=1
		total_inr = z

		xd = 0
		for sw in chm_usd:
			if sw>1:
				xd+=1
		total_usd = xd
		counter = (total_inr+total_usd)

		total_amount 		  = 0
		calc_amount_boss_inr  = 0
		calc_amount_chm 	  = 0
		calc_amount_boss_usd  = 0
		calc_amount_chm_usd   = 0
		calc_amount_chm_inr   = 0
		calc_boss_inr 		  = 0
		label 				  = ''
		check_counter_invoice = []
		invoice_Date 		  = '2023-01-01'
		invoice_dets 		  = models.invoice.objects.filter(payment_status='Paid',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31')
		for j in invoice_dets:
			if j.invoice_no not in check_counter_invoice:
				check_counter_invoice.append(j.invoice_no)
		for clx in check_counter_invoice:
			invoice_calc = models.invoice.objects.filter(invoice_no=clx,payment_status='Paid',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').first()
			try:
				calc_boss_inr+=invoice_calc.invoice_amount
				if invoice_calc.proj_name=='BOSS' and invoice_calc.client.currency_type=='INR':
					if invoice_calc.invoice_amount:
						calc_amount_boss_inr+=invoice_calc.invoice_amount
						label = 'INR'
				elif invoice_calc.proj_name=='CHM' and invoice_calc.client.currency_type=='INR':
					if invoice_calc.invoice_amount:
						calc_amount_chm_inr+=invoice_calc.invoice_amount
						label = 'INR'
				if invoice_calc.proj_name=='BOSS' and invoice_calc.client.currency_type=='USD':
					if invoice_calc.invoice_amount:
						calc_amount_boss_usd+=invoice_calc.invoice_amount
						label = 'USD'
				elif invoice_calc.proj_name=='CHM' and invoice_calc.client.currency_type=='USD':
					if invoice_calc.invoice_amount:
						calc_amount_chm_usd+=invoice_calc.invoice_amount
						label = 'USD'
				if invoice_calc.payment_status=='Paid':
					total_amount = (calc_amount_chm_usd+calc_amount_boss_usd+calc_amount_chm_inr+calc_amount_boss_inr)
				#print '_____>',calc_boss_inr
			except:
				calc_amount_boss_inr = ''
				label 			     = ''
				calc_amount_boss_usd = ''
				calc_amount_chm_inr  = ''



		tag_label 	  = label
		total_invoice = total_amount
		chm_usd       = calc_amount_chm_usd
		boss_usd      = calc_amount_boss_usd
		chm_inr       = calc_amount_chm_inr
		boss_inr      = calc_amount_boss_inr

		total_deleted_invoice = 0
		del_invoice_details   = models.delete_vessel_details.objects.all()		
		del_details 		  = []
		ix 					  = 0
		for d in del_invoice_details:
			client_det 		 = models.Client.objects.filter(id=d.client_id_id,currency_type=d.currency_type,proj_name=d.proj_name).first()
			del_invoice_date = d.delete_date.strftime("%d-%b-%Y")
			gen_invoice_date = d.invoice_date.strftime("%d-%b-%Y")
			ix+=1
			total_deleted_invoice = ix	
			#print '---------',	d.client_id_id

			del_details.append({
				'invoice_no' 		: d.invoice_no,
				'proj_name'  		: d.proj_name,
				'vessel_name' 		: d.ship_name,
				'client_name'   	: client_det.client_name,
				'currency_type' 	: d.currency_type,
				'invoice_date'  	: str(gen_invoice_date),
				'deleted_invoice' 	: str(del_invoice_date),
				})

		curr_date_invoice = datetime.now().date()
		curr_invoice 	  = models.invoice.objects.filter(invoice_date=curr_date_invoice,invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').order_by('invoice_no')
		curr_array 		  = []
		inv_arr = []
		for x in curr_invoice:
			if x.invoice_no not in inv_arr:
				inv_arr.append(x.invoice_no)

		for b in inv_arr:
			invoice_log 	  = models.invoice.objects.filter(invoice_no=b,invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').first()
			curr_array.append({
				'proj_name' : invoice_log.proj_name,
				'client_name' : invoice_log.client.client_name,
				'invoice_no'  : invoice_log.invoice_no
				})

		check_curr 	  = models.invoice.objects.filter(invoice_date=curr_date_invoice,invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').count()		
		if check_curr>1:
			show_table = ''
		else:
			show_table = 'none'

		
		context={
			'chm_total_paid' 		 : chm_total_paid,
			'boss_total_paid' 		 : boss_total_paid,
			'unpaid_boss_total_paid' : unpaid_boss_total_paid,
			'unpaid_chm_total_paid'  : unpaid_chm_total_paid,
			'total_invoice_chm'      : total_invoice_chm,
			'total_invoice_of_boss'  : total_invoice_of_boss,
			'total_invoice_counter'  : counter,
			'total_cancel_chm'		 : cancel_invoice_chm,
			'chm_usd' 			     : chm_usd,
			'boss_usd' 			     : boss_usd,
			'chm_inr' 			     : chm_inr,
			'boss_inr' 			     : boss_inr,
			'tag_label' 			 : tag_label,
			'total_invoice'  		 : total_invoice,
			'del_details' 			 : del_details,
			'total_deleted_invoice'  : total_deleted_invoice,
			'curr_array' 			 : curr_array,
			'show_table' 			 : show_table,
			'login_user' 			 : login_user,
 		}
		return render_to_response("invoice_display/index.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')

@csrf_exempt
def saving_fetching_data(request):
	if request.user.is_authenticated():
		table_details = json.loads(request.POST['table_container'])
		for x in table_details:
			valid = models.Client.objects.filter(client_name=x['client_name'],proj_name=x['proj_name'],currency_type=x['curr_type'],duration_type=x['dur_type'],price=x['client_price'],rate=x['price_rate'],price_type=x['price_type']).count()
			if valid>0:
				save_client_db = models.Client.objects.filter(client_name=x['client_name'],proj_name=x['proj_name'],currency_type=x['curr_type'],duration_type=x['dur_type'],price=x['client_price'],rate=x['price_rate'],price_type=x['price_type']).first()
			else:
				save_client_db = models.Client()
			save_client_db.client_name   = x['client_name']
			save_client_db.proj_name     = x['proj_name']
			save_client_db.currency_type = x['curr_type']
			save_client_db.duration_type = x['dur_type']
			save_client_db.price 		 = x['client_price']
			save_client_db.price_type 	 = x['price_type']
			save_client_db.rate 		 = x['price_rate']
			# save_client_db.tin_number	 = x['tin_number']
			save_client_db.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

@csrf_exempt
def load_fetching_data(request):
	if request.user.is_authenticated():
		try:
			table_details = json.loads(request.POST['table_container'])
			for x in table_details:
				valid = models.Client.objects.filter(client_name=x['client_name'],proj_name='CHM',currency_type=x['curr_type'],duration_type=x['dur_type'],price=x['price'],rate=x['rate'],price_type=x['price_type'],tin_number=x['tin_number']).count()
				if valid>0:
					save_client_db = models.Client.objects.filter(client_name=x['client_name'],proj_name='CHM',currency_type=x['curr_type'],duration_type=x['dur_type'],price=x['price'],rate=x['rate'],price_type=x['price_type'],tin_number=x['tin_number']).first()
				else:
					save_client_db = models.Client()
				save_client_db.client_name   = x['client_name']
				save_client_db.proj_name     = x['proj_name']
				save_client_db.currency_type = x['curr_type']
				save_client_db.duration_type = x['dur_type']
				save_client_db.price 		 = x['price']
				save_client_db.price_type 	 = x['price_type']
				save_client_db.rate 		 = x['rate']
				save_client_db.tin_number	 = x['tin_number']
				save_client_db.save()
		except:
			pass
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')


def update_client_chm_details(request):
	if request.user.is_authenticated():
		e_proj_name  	= json.loads(request.GET['e_proj_name'])
		e_currency_type = json.loads(request.GET['e_currency_type'])
		e_duration_type = json.loads(request.GET['e_duration_type'])
		e_price_type  	= json.loads(request.GET['e_price_type'])
		e_price  		= json.loads(request.GET['e_price'])
		e_rate  		= json.loads(request.GET['e_rate'])
		e_tin_number  	= json.loads(request.GET['e_tin_number'])
		e_vm_name_c  	= json.loads(request.GET['e_vm_name_c'])
		e_client_name   = json.loads(request.GET['e_client_name'])
		e_status_c      = json.loads(request.GET['e_status_x'])
		e_id      		= json.loads(request.GET['e_id'])
		

		save_client_db  = models.Client.objects.filter(id=e_id).first()
		try:
			save_client_db.client_name   = e_client_name
			save_client_db.proj_name     = e_proj_name
			save_client_db.currency_type = e_currency_type
			save_client_db.duration_type = e_duration_type
			save_client_db.vm_name       = e_vm_name_c
			save_client_db.price 		 = e_price
			save_client_db.price_type    = e_price_type
			save_client_db.rate 		 = e_rate
			save_client_db.tin_number 	 = e_tin_number
			save_client_db.status        = e_status_c
			save_client_db.save()
		except:
			pass
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

def view_client(request):
	if request.user.is_authenticated():		
		curr_date 		  = datetime.now().date()
		name  			  = ""
		ship_type 		  = ""
		start_date_format = "2019-01-01"
		end_date_format   = curr_date
		login_user 		  = request.user
		api_url 	      = "https://chm.bwesglobal.com/hb/get_chm_data/"
		api_method        = "GET"
		parameters        = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'name': name,'ship_type':ship_type,'start_date':str(start_date_format),'end_date': str(end_date_format)}
		response          = requests.get(api_url, params=parameters,verify=False)
		ch_array     	  = json.loads(response.content)
		ch_array    	  = ch_array['cl_array']	

		ship_arr	 	  = []
		client_arr   	  = []
		client_list  	  = []
		chm_array 		  = models.Client.objects.filter(proj_name="CHM")
		for ch in ch_array:
			if ch['client_name'] not in ship_arr:
				ship_arr.append(ch['client_name'])
		for cl in ship_arr:
			client_list.append({
				'client_name' : cl
				})

		client_details = models.Client.objects.filter(proj_name='CHM')
		client_array   = []
		for x in client_details:
			
			if x.price:
				price = x.price
			else:
				price = 0.0
			
			
			if x.price_type!='None':
				price_type = x.price_type
			else:
				price_type = ''

			if x.tin_number:
				tin_number = x.tin_number
			else:
				tin_number = 0.0

			if x.rate:
				rate = x.rate
			else:
				rate = 0.0

			if x.vm_name:
				vm_name = x.vm_name
			else:
				vm_name = ''



			# if x.status:
			# 	statusc = x.status
			# else:
			# 	statusc = 0			

			client_array.append({
				'client_name'   : x.client_name,
				'proj_name'     : x.proj_name,
				'currency_type' : x.currency_type,
				'duration_type' : x.duration_type,
				'price' 		: price,
				'price_type'    : price_type,
				'tin_number'	: tin_number,
				'rate' 			: rate,
				'vm_name' 		: vm_name,
				'id'			: x.id,
				'status'        : x.status,
				})
		price_list  = models.price_type_details.objects.all().order_by('id')
		price_array = []
		for p in price_list:
			price_array.append({
				'price_type' : p.price_type,
				'id' 		 : p.id
				})

		context={
		'client_list'  : client_list,
		'client_array' : client_array,
		'price_array'  : price_array,
		'login_user'   : login_user
		}
		return render_to_response("invoice_display/chm/view_chm_list.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')

def load_client(request):
	if request.user.is_authenticated():


		# client_details = models.Client.objects.filter(proj_name='CHM')
		# client_array   = []
		# for x in client_details:
		# 	if x.price:
		# 		price = x.price
		# 	else:
		# 		price = 0.0
		# 	if x.price_type:
		# 		price_type = x.price_type
		# 	else:
		# 		price_type = 0.0

		# 	if x.tin_number:
		# 		tin_number = x.tin_number
		# 	else:
		# 		tin_number = 0.0

		# 	if x.rate:
		# 		rate = x.rate
		# 	else:
		# 		rate = 0.0

		# 	if x.vm_name:
		# 		vm_name = x.vm_name
		# 	else:
		# 		vm_name = ''

		# 	client_array.append({
		# 		'client_name'   : x.client_name,
		# 		'proj_name'     : x.proj_name,
		# 		'currency_type' : x.currency_type,
		# 		'duration_type' : x.duration_type,
		# 		'price' 		: price,
		# 		'price_tpye'    : price_type,
		# 		'tin_number'	: tin_number,
		# 		'rate' 			: rate,
		# 		'vm_name' 		: vm_name,
		# 		'id'			: x.id,
		# 		})
		# context={
		# 'client_list'  : client_list,
		# 'client_array' : client_array,
		# }
		# client_details = models.Client.objects.all().exclude(proj_name='BOSS')
		# cl_list = []
		# for cl in client_details:
		# 	cl_list.append({
		# 		'id' 			: cl.id,
		# 		'client_name'   : cl.client_name,
		# 		'proj_name' 	: cl.proj_name,
		# 		'curr_type' 	: cl.currency_type,
		# 		'dur_type' 		: cl.duration_type,
		# 		'price' 		: cl.price,
		# 		'rate' 			: cl.rate,
		# 		'price_type' 	: cl.price_type,
		# 		'tin_number' 	: cl.tin_number,
		# 		})
		# context={
		# 'cl_list' : cl_list,
		# }
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')



# def function_call():
		
# 		api_url 	 = "https://chm.bwesglobal.com/hb/get_chm_data/"
# 		api_method   = "GET"
# 		parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
# 		response     = requests.get(api_url, params=parameters,verify=False)
# 		ch_array     = json.loads(response.content)
# 		chm_array    = ch_array['finance_array']
# 		for x in chm_array:
# 			client_details = models.Client.objects.filter(client_name=x['client_name'],proj_name='CHM').first()
# 			check = models.Ship.objects.filter(ship_name=x['ship_name'],client_id=client_details).count()
# 			if check>0:
# 				save_ship = models.Ship.objects.filter(ship_name=x['ship_name'],client_id=client_details).first()
# 			else:
# 				save_ship = models.Ship()

# 			save_ship.ship_name = x['ship_name']
# 			save_ship.client_id = client_details.id
# 			save_ship.save()

		
# 		return HttpResponse(json.dumps('done'))

# 		return HttpResponseRedirect('/it/user_login')

################# BOSS #######################################################
def fetching_get_api_boss(request):
	if request.user.is_authenticated():
		#api_url 	= "http://0.0.0.0:8003/api/get_data_boss/"
		api_url 	= "https://bossv2.bwesglobal.com/api/get_data_boss/"
		api_method  = "GET"
		parameters  = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response    = requests.get(api_url, params=parameters,verify=False)
		return HttpResponse(response.content)
	else:
		return HttpResponseRedirect('/it/user_login')

def fetch_boss(request):
	if request.user.is_authenticated():

		return render_to_response("invoice_display/boss/fetch_boss.html")
	else:
		return HttpResponseRedirect('/it/user_login')

def view_boss_client(request):
	if request.user.is_authenticated():
		curr_date 			= datetime.now().date()
		name 				= ""
		ship_type 			= ""
		start_date_format 	= '2020-01-01'
		end_date_format 	= curr_date
		client_list  		= ''
		client_array 		= '' 
		login_user 			= request.user	
		#api_url 			= "http://0.0.0.0:8004/api/get_data_boss/"
		api_url 			= "https://aboss.bwesglobal.com/api/get_static_details/"
		api_method  		= "GET"
		parameters  		= {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response    		= requests.get(api_url, params=parameters,verify=False)
		client_arr  		= json.loads(response.content)
		cl_list     		= client_arr['client_details']	

		
		client_arr  		= []
		ship_array 			= []
		chm_array   		= []
		merge_ship  		= []
		client_list 		= []
		client_arr  		= []
		
		for sh in cl_list:			
			if cl_list[sh]['name'] not in client_arr:				
				client_arr.append(cl_list[sh]['name'])
		
		for cl in client_arr:
			client_list.append({
				'client_name' : cl
				})
		
		client_details = models.Client.objects.filter(proj_name='BOSS')
		client_array   = []
		for x in client_details:
			if x.price:
				price = x.price
			else:
				price = 0.0
			if x.price_type:
				price_type = x.price_type
			else:
				price_type = 0.0

			if x.tin_number:
				tin_number = x.tin_number
			else:
				tin_number = 0.0

			if x.rate:
				rate = x.rate
			else:
				rate = 0.0

			if x.vm_name:
				vm_name = x.vm_name
			else:
				vm_name = ''

			if x.tax:
				e_tax = x.tax
			else:
				e_tax = 0

			try:
				day_cals  = x.day_calculate
			except:
				day_cals = ''

			# if x.status:
			# 	status = x.status
			# else:
			# 	status = ''

			if x.status==1:
				_active = 'Active'
			else:
				_active = ''

			client_array.append({
				'client_name'   : x.client_name,
				'proj_name'     : x.proj_name,
				'currency_type' : x.currency_type,
				'duration_type' : x.duration_type,
				'price' 	   	: price,
				'price_tpye'    : price_type,
				'tin_number'   	: tin_number,
				'rate' 		   	: rate,
				'vm_name' 	   	: vm_name,
				'id'		   	: x.id,
				'status'        : _active,
				'e_tax' 		: e_tax,
				'day_cals'		: day_cals,
				})
		
		context={
		'client_list'  : client_list,
		'client_array' : client_array,
		'login_user'   : login_user
		}
		return render_to_response("invoice_display/boss/view_boss_list.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')


def submit_boss_client_details(request):
	if request.user.is_authenticated():
		client_name 	= json.loads(request.GET['client_name'])
		proj_name 		= json.loads(request.GET['proj_name'])
		currency_type 	= json.loads(request.GET['currency_type'])
		duration_type 	= json.loads(request.GET['duration_type'])
		price 			= json.loads(request.GET['price'])
		price_type 		= json.loads(request.GET['price_type'])
		rate 			= json.loads(request.GET['rate'])
		customer_no 	= json.loads(request.GET['customer_no'])
		vm_name 		= json.loads(request.GET['vm_name'])
		#print '_______',client_name,proj_name,currency_type,duration_type,price,price_type,rate,customer_no,vm_name
		check = models.Client.objects.filter(client_name=client_name,proj_name=proj_name,price_type=price_type).count()
		if check>0:
			save_db_client = models.Client.objects.filter(client_name=client_name,proj_name=proj_name,price_type=price_type).first()
		else:
			save_db_client = models.Client()
		save_db_client.client_name 	 = client_name
		save_db_client.proj_name 	 = proj_name
		save_db_client.currency_type = currency_type
		save_db_client.duration_type = duration_type
		save_db_client.price 		 = price
		save_db_client.price_type    = price_type
		save_db_client.rate 		 = rate
		save_db_client.tin_number  	 = customer_no
		save_db_client.vm_name 		 = vm_name
		save_db_client.save()

		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

# def load_boss_client_details(request):
# 	if request.user.is_authenticated():
# 		client_details = models.Client.objects.filter(proj_name='BOSS')
# 		client_array   = []



# 		return HttpResponse(json.dumps(context))
# 	else:
# 		return HttpResponseRedirect('/it/user_login')


# def load_boss_client(request):
# 	if request.user.is_authenticated():
# 		client_details = models.Client.objects.all().exclude(proj_name='CHM')
# 		cl_list = []
# 		for cl in client_details:

# 			cl_list.append({
# 				'id' 			: cl.id,
# 				'client_name'   : cl.client_name,
# 				'proj_type' 	: cl.proj_name,
# 				'curr_type' 	: cl.currency_type,
# 				'dur_type' 		: cl.duration_type,
# 				'price' 		: cl.price,
# 				'price_type'    : cl.price_type,
# 				'rate' 			: cl.rate,
# 				'tin_number' 	: cl.tin_number,
# 				'vm_name' 		: cl.vm_name,
# 				})
# 		context={
# 		'cl_list' : cl_list,
# 		}
# 		return HttpResponse(json.dumps(context))
# 	else:
# 		return HttpResponseRedirect('/it/user_login')

@csrf_exempt
def saving_boss_fetching_data(request):
	if request.user.is_authenticated():
		table_details = json.loads(request.POST['table_container'])
		for x in table_details:
			check_client = models.Client.objects.filter(client_name=x['client_name'],proj_name='BOSS').first()
			if check_client>0:
			 	save_client_db = models.Client.objects.filter(client_name=x['client_name'],proj_name='BOSS').first()
			else:
				save_client_db = models.Client()
			save_client_db.client_name   = x['client_name']
			save_client_db.proj_name     = x['proj_type']
			save_client_db.currency_type = x['curr_type']
			save_client_db.duration_type = x['dur_type']
			save_client_db.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

def update_boss_client_details(request):
	if request.user.is_authenticated():
		client_id  		= json.loads(request.GET['client_id'])
		e_proj_name  	= json.loads(request.GET['e_proj_name'])
		e_currency_type = json.loads(request.GET['e_currency_type'])
		e_duration_type = json.loads(request.GET['e_duration_type'])
		e_price_type  	= json.loads(request.GET['e_price_type'])
		e_price  		= json.loads(request.GET['e_price'])
		e_rate  		= json.loads(request.GET['e_rate'])
		e_tin_number  	= json.loads(request.GET['e_tin_number'])
		e_vm_name_c  	= json.loads(request.GET['e_vm_name_c'])
		e_client_name   = json.loads(request.GET['e_client_name'])
		e_status_c      = json.loads(request.GET['e_status_c'])
		e_day_cal      	= json.loads(request.GET['e_day_cal'])
		
		
		save_client_db = models.Client.objects.filter(proj_name='BOSS',currency_type=e_currency_type,id=client_id).first()
		save_client_db.client_name   = e_client_name
		save_client_db.proj_name     = e_proj_name
		save_client_db.currency_type = e_currency_type
		save_client_db.duration_type = e_duration_type
		save_client_db.vm_name       = e_vm_name_c
		save_client_db.price 		 = e_price
		save_client_db.price_type    = e_price_type
		save_client_db.rate 		 = e_rate
		save_client_db.tin_number 	 = e_tin_number
		save_client_db.status 		 = e_status_c
		
		try:
			save_client_db.day_calculate = e_day_cal
		except:
			save_client_db.day_calculate = None

		save_client_db.save()

		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')


def view_chm_vessel(request):
	if request.user.is_authenticated():
		return render_to_response("invoice_display/chm/view_chm_vessel.html")
	else:
		return HttpResponseRedirect('/it/user_login')

def load_chm_vessel(request):
	if request.user.is_authenticated():
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

def view_boss_vessel(request):
	if request.user.is_authenticated():
		return render_to_response("invoice_display/boss/view_boss_vessel.html")
	else:
		return HttpResponseRedirect('/it/user_login')

################################## CHM #####################################
def vessel_details(request):
	if request.user.is_authenticated():
		invoice_details = models.vessel_selected_invoice.objects.all().order_by('-id')
		invoice_array   = []
		invoice_count = models.invoice.objects.all().count()
		today = datetime.now().strftime('%Y')
		if today < int(today)+1:
			start_invoice = '1718'
		else:
			start_invoice = '1718'

		voy_array = []
		if invoice_count:
			max_number 	= models.invoice.objects.all().order_by('-invoice_no').first()
			ser_no    	= max_number.invoice_no
			split_no  	= ser_no.split("/")
			ser_first 	= int(split_no[0])+1
			append_str 	= ''
			if ser_first>=0 and ser_first<=9:
			 	append_str='000'
			if ser_first>=10 and ser_first<=99:
				append_str='00'
			if ser_first>=100 and ser_first<=999:
				append_str='0'
			if ser_first>=1000 and ser_first<=9999:
				append_str=''
			invoice_no 	= str(append_str+ str(ser_first))+"/"+str(start_invoice)
		else:
			invoice_no 	= "0001/"+str(start_invoice)
		voy ={}
		for i in invoice_details:
			if len(i.ship_name)>1:
				voy_array.append(i.voyage_no)
				voyage_number = voy_array
			else:
				voyage_number = i.voyage_no

			format_disch_date = i.disch_date.strftime("%d-%b-%Y")
			ship_list 	 = models.Ship.objects.filter(ship_name=i.ship_name).first()
			client_name  = ship_list.client.client_name
			client_price = ship_list.client.price
			price_type   = ship_list.client.price_type
			price_rate   = ship_list.client.rate
			try:
				client_addre = ship_list.address
			except:
				client_addre = 'Not Available'
			invoice_array.append({
				'ship_name'  : i.ship_name,
				'voyage_no'  : voyage_number,#i.voyage_no,
				'disch_port' : i.disch_port,
				'disch_date' : str(format_disch_date),
				'vm_name'    : i.vm_name,
				'client'     : client_name,
				'price'      : client_price,
				'rate' 		 : price_rate,
				'price_type' : price_type,
				'invoice_no' : invoice_no,
				'address'    : client_addre,
				'proj_name'  : 'CHM',
				'client_id'  : ship_list.client.id,
				'qty' 		 : i.qty,
				})

		voy 	  = voyage_number
		voyage_no = ', '.join(voy)

		context={
		'invoice_array' : invoice_array,
		'voyage_no'     : voyage_no,

		}
		return render_to_response("invoice_display/chm/submit_invoice.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')


def load_for_invoice_details(request):
	if request.user.is_authenticated():
		client 		  = json.loads(request.GET['client_name'])
		ship   		  = json.loads(request.GET['ship_name'])
		get_client 	  = models.Client.objects.filter(client_name=client,proj_name='CHM').order_by('price_type')
		price_arr  	  = []
		price 		  = []

		ship_details  = models.Ship.objects.filter(ship_name=ship).first()
		try:
			ship_address  = ship_details.address
		except:
			ship_address  = 'Not available'
		invoice_count = models.invoice.objects.all().count()
		today = datetime.now().strftime('%Y')
		if today < int(today)+1:
			start_invoice = '1718'
		else:
			start_invoice = '1718'

		if invoice_count:
			max_number 	= models.invoice.objects.all().order_by('-invoice_no').first()
			ser_no    	= max_number.invoice_no
			split_no  	= ser_no.split("/")
			ser_first 	= int(split_no[0])+1
			append_str 	= ''
			if ser_first>=0 and ser_first<=9:
			 	append_str='000'
			if ser_first>=10 and ser_first<=99:
				append_str='00'
			if ser_first>=100 and ser_first<=999:
				append_str='0'
			if ser_first>=1000 and ser_first<=9999:
				append_str=''
			invoice_no 	= str(append_str+ str(ser_first))+"/"+str(start_invoice)
		else:
			invoice_no 	= "0001/"+str(start_invoice)

		for x in get_client:
			if x.proj_name=='CHM':
				proj_type = "Cargo Heating Management Services"

			if x.client_name=="Stena Bulk Veg Oil" or x.client_name=="stena bulk":
				if x.price_type not in price_arr:
					price_arr.append(x.price_type)
			else:
				price.append({
				'price_type'   : 'Flat',
				'proj_name'    : x.proj_name,
				'proj_type'    : proj_type,
				'price'        : x.price,
				'ship_address' : ship_address,
				'pool_name'    : client+' Pool',
				'invoice_no'   : invoice_no,
				})

		for p in price_arr:
			if p!='0':
				get_price 	  = models.Client.objects.filter(client_name=client,price_type=p,proj_name='CHM').first()
				price.append({
					'price_type'   : get_price.price_type,
					'proj_name'    : x.proj_name,
					'proj_type'    : proj_type,
					'price'        : get_price.price,
					'ship_address' : ship_address,
					'pool_name'    : client+' Pool',
					'invoice_no'   : invoice_no,
					})


		return HttpResponse(json.dumps(price))
	else:
		return HttpResponseRedirect('/it/user_login')

def submit_invoice_details(request):
	if request.user.is_authenticated():
		today       	  = datetime.now().date()
		ship_name   	  = json.loads(request.GET['vessel_name'])
		invoice_id  	  = json.loads(request.GET['invoice_id'])
		voy_no 	    	  = json.loads(request.GET['voyage_no'])
		client_name 	  = json.loads(request.GET['client_name'])
		price_type  	  = json.loads(request.GET['price_type'])
		proj_name   	  = json.loads(request.GET['proj_name'])
		proj_type   	  = json.loads(request.GET['proj_type'])
		address     	  = json.loads(request.GET['addres'])
		price 			  = json.loads(request.GET['price'])
		vm_name     	  = json.loads(request.GET['vm_name'])
		client_id   	  = json.loads(request.GET['client_id'])
		disch_date  	  = json.loads(request.GET['disch_date'])
		disch_port  	  = json.loads(request.GET['disch_port'])
		format_disch_date = disch_date
		disch_date_for    = datetime.strptime(format_disch_date, "%d-%b-%Y").strftime('%Y-%m-%d')
		get_client_id 	  = models.Client.objects.filter(client_name=client_name).first()
		get_clientID  	  = get_client_id.id

		submit_invoice = models.invoice()
		submit_invoice.ship_name      = ship_name
		submit_invoice.invoice_no 	  = invoice_id
		submit_invoice.voyage_no  	  = voy_no
		submit_invoice.invoice_date   = today
		submit_invoice.proj_name      = proj_name
		submit_invoice.client_address = address
		submit_invoice.invoice_amount = price
		submit_invoice.vm_name 		  = vm_name
		submit_invoice.client_id 	  = get_clientID
		submit_invoice.disch_port     = disch_port
		submit_invoice.disch_date     = disch_date_for
		if get_client_id.currency_type=='USD':
			submit_invoice.usd = 'USD'
		else:
			submit_invoice.inr = 'INR'

		check = models.invoice.objects.filter(voyage_no=voy_no,ship_name=ship_name).count()
		if check>0:
			disable= 'none'
			msg = ''
		else:
			disable = ''
			msg = 'done'
			submit_invoice.save()

		context={
		'disable' : disable,
		'msg'     : msg,
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')


def select_price_type(request):
	if request.user.is_authenticated():
		price_type   = json.loads(request.GET['price_type'])
		client_name  = json.loads(request.GET['client_name'])
		select_price = models.Client.objects.filter(price_type=price_type,client_name=client_name).first()
		prices       = select_price.price
		return HttpResponse(json.dumps(prices))
	else:
		return HttpResponseRedirect('/it/user_login')

@csrf_exempt
def vaild_invoice_details(request):
	if request.user.is_authenticated():
		ship_name 		= request.POST['vessel_name']
		voy_no    		= request.POST['voyage_no']
		sno       		= request.POST['sno']
		client_name  	= request.POST['client_name']
		cancel_shipname = request.POST['cancel_shipname']
		cancel_voyno 	= request.POST['cancel_voyno']
		cancel_vessel 	= request.POST['cancel_vessel']
		vessel_type 	= request.POST['vessel_type']
		mix_vessel 		= ship_name.replace(' ', '_')
		arr 	  		= []

		if client_name=='Shell NWE':
			client_id = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()
			check     = models.invoice.objects.filter(ship_name=ship_name,proj_name='CHM',cancel_invoice='0',client_id=client_id,voyage_no=voy_no).count()
			#print '_____',check,'_______',ship_name,'____',voy_no,'-____',client_id
		else:
			# if client_name=='Navig8':
			# 	client_id = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()
			# 	check  = models.invoice.objects.filter(ship_name=ship_name,voyage_no=voy_no,proj_name='CHM',cancel_invoice='0',vessel_type=vessel_type,client_id).count()
			# else:
			client_id = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()			
			check  	  = models.invoice.objects.filter(ship_name=ship_name,voyage_no=voy_no,proj_name='CHM',cancel_invoice='0',client_id=client_id).count()

		cdk       = models.invoice.objects.filter(ship_name=ship_name,proj_name='CHM',cancel_invoice='0')
		icon      = ''
		button    = ''
		msg = ''
		for z in cdk:
			if len(z.voyage_no.split(','))>1:
				for i in range(0,len(z.voyage_no.split(','))):
					split_voy_no     = z.voyage_no.split(',')
					modify_voyage_no = split_voy_no[i]
					client_id = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()
					if voy_no in modify_voyage_no:
						check_invoice_details = models.invoice.objects.filter(ship_name=ship_name,voyage_no=modify_voyage_no,cancel_invoice='0',client__client_name=client_name).count()
						#print '_____',check_invoice_details
						if check_invoice_details==0:
							icon   = 'none'
							button = 'none'
							msg    = 'Invoice already submitted'
						else:
							icon   = ''
							button = ''
							msg    = ''
			else:
				client_id = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()
				#check_invoice_details = models.invoice.objects.filter(ship_name=ship_name,voyage_no=voy_no,cancel_invoice='0').count()
				check_invoice_details = models.invoice.objects.filter(ship_name=ship_name,voyage_no=voy_no,cancel_invoice='0',client__client_name=client_name).count()
				#print '___________',client_id,'_____',ship_name,'____',voy_no
				if check_invoice_details==1:
					icon   = 'none'
					button = 'none'
					msg    = 'Invoice already submitted'
				else:
					icon   = ''
					button = ''
					msg    = ''




		if check>0:
		 	display_button = 'none'
		 	shipname       = ship_name
		 	voyno   	   = voy_no
		 	s_no 		   = sno
		 	already 	   = 'Already submitted'
		 	mix_vessel     = mix_vessel
		 	#print '______',cancel_shipname,'______',cancel_voyno
		 	if cancel_shipname!='' and  cancel_voyno!='':
		 		display_button = 'none'
			 	shipname       = cancel_shipname
			 	voyno   	   = cancel_voyno
			 	s_no 		   = sno
			 	already 	   = 'Already submitted'
			 	mix_vessel     = mix_vessel
			else:
				# display_button = 'none'
			 # 	shipname       = ship_name
			 # 	voyno   	   = voy_no
			 # 	s_no 		   = sno
			 # 	already 	   = ''
			 # 	mix_vessel     = mix_vessel
				pass

		else:
		 	display_button = ''
		 	shipname       = ship_name
		 	voyno   	   = voy_no
		 	s_no 		   = sno
		 	already 	   = ''
		 	mix_vessel     = ''


		context={
		'display_button' : display_button,
		'shipname'   	 : shipname,
		'voyno'   		 : voyno,
		's_no' 		     : s_no,
		'icon'			 : icon,
		'button' 		 : button,
		'already'	     : already,
		'mix_vessel'     : mix_vessel,
		'msg' 			 : msg
		}
		#pprint.pprint(context)
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def view_chm_tracker(request):
	if request.user.is_authenticated():
		tracker_details = models.invoice.objects.all()
		tracker_array   = []
		i = 0
		for x in tracker_details:
			invoice_no   = x.invoice_no
			invoice_date = x.invoice_date
			ship_name 	 = x.ship_name
			voyage_no    = x.voyage_no
			invoice_id   = x.id
			if x.received_date!=None:
				show 	 = 'none'
			else:
				show 	 = ''
			if x.received_date:
				rec_date = x.received_date
			else:
				rec_date = ''
			if x.cancel_invoice!=0:
				cancel 	 = 'Cancel'
			else:
				cancel 	 = ''

			try:
				client_name = x.client.client_name
			except:
				client_name = ''

			if len(x.voyage_no.split(','))>1:
				for i in range(0,len(x.voyage_no.split(','))):
					split_voy_no          = x.voyage_no.split(',')
					modify_voyage_no      = split_voy_no[i]
					check_invoice_details = models.invoice.objects.filter(ship_name=x.ship_name,voyage_no=modify_voyage_no,payment_status=None)
					for c in check_invoice_details:
						c.payment_status  = 'Paid'
						c.received_date   = rec_date
						c.save()


			tracker_array.append({
				'invoice_no'   : invoice_no,
				'invoice_date' : invoice_date,
				'ship_name'    : ship_name,
				'voyage_no'    : voyage_no,
				'client_name'  : client_name,
				'invoice_id'   : invoice_id,
				'show' 		   : show,
				'receive_date' : rec_date,
				'cancel'       : cancel,
	 			})

		context={
		'tracker_array' : tracker_array
		}

		return render_to_response("invoice_display/chm/tracker_chm_invoice.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')


def view_ship_address(request):
	if request.user.is_authenticated():
		ship_details = models.Ship.objects.all()
		ship_array   = []
		for sh in ship_details:
			if sh:
				if sh.client:
					client_name = sh.client.client_name
				else:
					client_name = ''

				if sh.vm_name:
					vm_name = sh.vm_name
				else:
					vm_name = ''
				ship_array.append({
					'ship_name' : sh.ship_name,
					'address'   : sh.address,
					'email'     : sh.email,
					'email_cc'  : sh.email_cc,
					'client'    : client_name,
					'vm_name'   : vm_name
					})

		ship_details = models.Ship.objects.all()
		ship_list    = []
		ship = []
		for sh in ship_details:
			if sh.ship_name not in ship_list:
				ship_list.append(sh.ship_name)
		for x in ship_list:
			ship_det = models.Ship.objects.filter(ship_name=x).first()
			ship.append({
				'id'        : ship_det.id,
				'ship_name' : x,
				})

		context={
		'ship_array' : ship_array,
		'ship' 		 : ship
		}
		return render_to_response("invoice_display/chm/view_ship_address.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')

def update_ship_address(request):
	if request.user.is_authenticated():
		address = request.GET['address']
		email 	= request.GET['email']
		email_c = request.GET['email_c']
		IDx     = request.GET['id']
		vm_name = request.GET['vm']
		update  = models.Ship.objects.filter(id=IDx).first()
		update.address  = address
		update.email    = email
		update.email_cc = email_c
		update.vm_name  = vm_name
		update.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

def select_ship_address(request):
	if request.user.is_authenticated():
		ship = json.loads(request.GET['shipID'])
		if ship==0:
			ship_details = models.Ship.objects.all()
		else:
			ship_details = models.Ship.objects.filter(id=ship)
		select_ship	= []
		s_no = 1
		for sh in ship_details:
			if sh.client:
				client_name = sh.client.client_name
				proj_name   = sh.client.proj_name
				vm_name     = sh.vm_name
			else:
				client_name = ''
				proj_name   = ''
				vm_name     = ''

			select_ship.append({
				'ship_id'   : sh.id,
				'ship_name' : sh.ship_name,
				'address'   : sh.address,
				'email'     : sh.email,
				'email_cc'  : sh.email_cc,
				'client'    : client_name,
				's_no' 		: s_no,
				'proj_name' : proj_name,
				'vm_name'   : vm_name,
				})
			s_no+=1
		context={
		'select_ship' : select_ship,
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def paid_invoice_details(request):
	if request.user.is_authenticated():
		return render_to_response("invoice_display/paid_invoice.html")
	else:
		return HttpResponseRedirect('/it/user_login')

def getting_invoice_id(request):
	if request.user.is_authenticated():
		invoice_number 	= json.loads(request.GET['invoice_no'])[0]
		invoice_details = models.invoice.objects.filter(invoice_no=invoice_number)
		invoice_array   = []
		voy_no 			= []
		c = 1

		for x in invoice_details:
			if x.invoice_no>1:
				counter = c
				c+=1
			price = x.client.price

			try:
				c_date = x.received_date
				if c_date==None:
					rec_date = datetime.now().date()
				else:
					rec_date = c_date
			except:
				pass

			invoice_array.append({
				'invoice_amount' : x.invoice_amount,
				'ship_name'      : x.ship_name,
				'voyage_no'		 : x.voyage_no,
				'invoice_no'     : x.invoice_no,
				'price'			 : price,
				'rec_date' 		 : str(rec_date),
				})

		qtyw = (counter*price)
		context={
			'invoice_array' : invoice_array,
			'total_amount'  : qtyw,
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def payment_invoice(request):
	if request.user.is_authenticated():
		invoice_no     = json.loads(request.GET['invoice_no'])[0]
		cancel  	   = json.loads(request.GET['cancel'])
		rec_date  	   = json.loads(request.GET['rec_date'])

		try:
			for_rec_date   = rec_date
			rec_date_for   = datetime.strptime(for_rec_date, "%m/%d/%Y").strftime('%Y-%m-%d')
		except:
			rec_date_for = rec_date

		amount  	   				  = json.loads(request.GET['amount'])
		status  	   				  = json.loads(request.GET['status'])
		voy_no 		   				  = json.loads(request.GET['voy_no'])
		update_invoice 				  = models.invoice.objects.filter(invoice_no=invoice_no).first()
		update_invoice.invoice_amount = amount
		update_invoice.received_date  = rec_date_for
		update_invoice.cancel_invoice = cancel
		update_invoice.payment_status = status
		update_invoice.voyage_no	  = voy_no
		update_invoice.save()

		invoice_details = models.invoice.objects.filter(invoice_no=invoice_no)
		invoice_array   = []
		voy_no 			= []
		for x in invoice_details:
			ship_name_list 	= x.ship_name
			invoice_list 	= models.invoice.objects.filter(ship_name=ship_name_list)
			invoice_ct 		= models.invoice.objects.filter(ship_name=ship_name_list).exclude(payment_status=None).count()
			try:
				rec_date = x.received_date
			except:
				rec_date = ''

			for i in invoice_list:
				price = x.client.price
				check_list 		= models.invoice.objects.filter(ship_name=i.ship_name).first()
				if check_list.payment_status=="Paid":
					all_list 	= models.invoice.objects.filter(invoice_no=check_list.invoice_no).exclude(payment_status="Paid")
					for x in all_list:
						modify_list = models.invoice.objects.filter(invoice_no=check_list.invoice_no).exclude(payment_status="Paid").first()
						modify_list.payment_status = "Paid"
						modify_list.received_date  = rec_date
						modify_list.invoice_amount = amount
						modify_list.cancel_invoice = cancel
						modify_list.save()

		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')


def view_invoice_template(request):
	if request.user.is_authenticated():
		invoice_no    = request.GET['invoice_no']
		invoice_array = []
		x = models.invoice.objects.filter(invoice_no=invoice_no).first()
		if x.proj_name=='CHM':
			invoice_details = models.invoice.objects.filter(invoice_no=invoice_no)
			invoice_arr = get_proj_name(invoice_details,'CHM')
		elif x.proj_name=='BOSS':
			invoice_details = models.invoice.objects.filter(invoice_no=invoice_no)
			invoice_arr = get_proj_name(invoice_details,'BOSS')

		for i in invoice_arr:
			client_address = i['client_address'],
			vm_name 	   = i['vm_name'],
			invoice_date   = i['invoice_date'],
			invoice_no     = i['invoice_no'],
			voyage_no 	   = i['voyage_no'],
			proj_id        = i['projected_id'],
			due_date 	   = i['due_date'],
			disch_date     = i['disch_date'],
			disch_port 	   = i['disch_port'],
			client_name    = i['client_name'],
			in_words 	   = i['in_words'],
			description    = i['description'],

			invoice_array.append({
			'ship_name' 	 : i['ship_name'],
			'rate' 			 : i['rate'],
			'price' 		 : i['price'],
			'ship_name'      : i['ship_name'],
			'invoice_amount' : i['invoice_amount'],
			'cancel' 		 : i['cancel'],
			'project_type'   : i['project_type'],
			'client_amount'  : i['client_amount'],
			})

		client_address  = client_address[0]
		vm_name   		= vm_name[0]
		invoice_date   	= invoice_date[0]
		invoice_no   	= invoice_no[0]
		voyage_no   	= voyage_no[0]
		proj_id   		= proj_id[0]
		due_date   		= due_date[0]
		disch_date      = disch_date[0]
		disch_port      = disch_port[0]
		client_name  	= client_name[0]
		in_word  		= in_words[0]
		desc 			= description[0]

		context={
		'invoice_array'  : invoice_array,
		'client_address' : client_address,
		'vm_name' 		 : vm_name,
		'invoice_date' 	 : invoice_date,
		'invoice_no' 	 : invoice_no,
		'voyage_no' 	 : voyage_no,
		'proj_id' 		 : proj_id,
		'due_date' 		 : due_date,
		'disch_date' 	 : disch_date,
		'disch_port' 	 : disch_port,
		'client_name'    : client_name,
		'in_words'       : in_word,
		'desc' 			 : desc,
		}
		if x.proj_name=='CHM':
			return render_to_response("invoice_display/invoice.html",context)
		elif x.proj_name=='BOSS':
			return render_to_response("invoice_display/invoice_boss.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')

def get_proj_name(invoice_details,proj_name):
	in_arr = []
	for c in invoice_details:
		try:
			addr = c.client_address.encode('utf-8')
			add1 = addr.split(',')
			client_header  = add1[0]
			client_address = add1[1]
		except:
			client_header  = ''
			client_address = ''

		invoice_date 	  	= c.invoice_date
		format_invoice_date = invoice_date.strftime("%d-%b-%Y")
		disch_date 	  		= c.disch_date
		if disch_date:
			format_disch_date = disch_date.strftime("%d-%b-%Y")
		else:
			format_disch_date = ''

		try:
			projected_id = c.client.client_name+'/BW/'+proj_name
		except:
			projected_id = ''

		if c.payment_status=='Paid':
			invoice_price = c.invoice_amount
			try:
				rate =  round(c.invoice_amount)
			except:
				rate = 0.0
		else:
			invoice_price = 0
			rate = 0

		try:
			if c.client.client_name=='Shell':
				format_due_date = c.invoice_date + timedelta(days=60)
				due_date 	   	= format_due_date.strftime("%d-%b-%y")
			else:
				format_due_date = c.invoice_date + timedelta(days=30)
				due_date 	   	= format_due_date.strftime("%d-%b-%y")
		except:
			format_due_date = ''
			due_date 		= ''

		if proj_name=="CHM":
			project_name = 'Cargo Heating Management Services'
			description  = 'Cargo Heating Management Services'
		else:
			project_name = c.ship_name
			description  = 'Bluewater Optimum Speed Services'

		client_price  = c.client.price
		client_rate   = c.client.rate
		client_amount = (client_price)
		in_words = num2words(client_amount)

		in_arr.append({
		'ship_name' 	 : c.ship_name,
		'rate' 			 : c.client.price,
		'price' 		 : c.client.price,
		'client_name'    : client_header,
		'client_address' : client_address,
		'vm_name' 	     : c.vm_name,
		'invoice_date'   : str(format_invoice_date),
		'invoice_no'     : 'CUSD/'+str(c.invoice_no),
		'disch_date'     : str(format_disch_date),
		'disch_port'     : c.disch_port,
		'ship_name'      : c.ship_name,
		'voyage_no' 	 : c.voyage_no,
		'projected_id'   : projected_id,
		'due_date' 		 : str(due_date),
		'invoice_amount' : invoice_price,
		#'rate' 			 : int(rate),
		'cancel' 		 : c.cancel_invoice,
		'project_type'   : project_name,
		'client_amount'  : client_amount,
		'in_words' 		 : in_words,
		'description'    : description,   
		})

	return in_arr


def login_user(request):
	if request.method == 'POST':
		username 	= json.loads(request.POST['user_name'])
		password 	= json.loads(request.POST['password'])
		user 		= authenticate(username = username, password = password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponse(json.dumps('loggedin'))
			else:
				return HttpResponse(json.dumps("account disabled"))
		else:
			return HttpResponse(json.dumps("invalid"))
	else:
		if request.user.is_authenticated():
			return HttpResponseRedirect('/it/chm_tracker')
		return render_to_response('login/login.html',  RequestContext(request, {}))

def user_logout(request):
	logout(request)	
	return HttpResponseRedirect('/it/user_login')


def view_combined_tracker(request):
	if request.user.is_authenticated():


		return render_to_response("invoice_display/chm/view_combined_tracker.html")
	else:
		return HttpResponseRedirect('/it/user_login')

@csrf_exempt
def combined_tracker(request):
	if request.user.is_authenticated():
		from collections import Counter
		models.vessel_selected_invoice.objects.all().delete()
		voyage_array 	    = json.loads(request.POST['selection_array'])
		client_lt    	    = json.loads(request.POST['client_lt'])
		proj_name    	    = json.loads(request.POST['proj_name'])
		vessel_details 	    = json.loads(request.POST['vessel_det'])
		vessel_type         = json.loads(request.POST['vessel_type'])
		update_invoice_date = json.loads(request.POST['update_invoice_date'])
		stt_dt 	 	 		= json.loads(request.POST['start_dt'])
		ed_dt 		 		= json.loads(request.POST['end_dt'])
		merge 		 		= request.POST['merge']
		#f_invoice_no 		= models.financial_invoice_no.objects.all().order_by('-id').first()
		#print '------->>>>>',f_invoice_no

		try:
			models.generate_for_vessel.objects.all().delete()                
		except:
			pass
		try:
			start_dt = datetime.strptime(stt_dt, "%m/%d/%Y").strftime('%Y-%m-%d')
			end_dt   = datetime.strptime(ed_dt, "%m/%d/%Y").strftime('%Y-%m-%d')
		except:
			start_dt = ''
			end_dt   = ''

		voyage 		 = [int(x) for x in voyage_array]
		api_url 	 = "https://chm.bwesglobal.com/hb/get_chm_data/"
		api_method   = "GET"
		parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'name': client_lt,'start_date':str(start_dt),'end_date': str(end_dt),'ship_type' : (vessel_type)}

		response     = requests.get(api_url, params=parameters,verify=False)
		ch_array     = json.loads(response.content)
		chm_array    = ch_array['finance_array']
		chm_append   = []
		if start_dt:
			start_date = start_dt			
		else:
			start_date = datetime.now().date()			
		
		# invoice_count   = models.invoice.objects.all().count()
		# today = datetime.now().strftime('%Y')
		# if today < int(today)+1:
		f_invoice_no 		= models.financial_invoice_no.objects.all().order_by('-id').first()
		get_fin_invoice_no  = f_invoice_no.fin_invoice_no
		start_invoice 		= get_fin_invoice_no  #'2425'
		# else:
		# 	start_invoice = '1718'
		# if invoice_count:
		# 	max_number 	= models.invoice.objects.all().order_by('-invoice_no').first()
		# 	ser_no    	= max_number.invoice_no
		# 	split_no  	= ser_no.split("/")
		# 	ser_first 	= int(split_no[0])+1
		# 	append_str 	= ''
		# 	if ser_first>=0 and ser_first<=9:
		# 	 	append_str=''
		# 	if ser_first>=10 and ser_first<=99:
		# 		append_str=''
		# 	if ser_first>=100 and ser_first<=999:
		# 		append_str=''
		# 	if ser_first>=1000 and ser_first<=9999:
		# 		append_str=''
		# 	invoice_n 	= str(append_str+ str(ser_first))+"/"+str(start_invoice)
		# else:
		# 	invoice_n 	= "0001/"+str(start_invoice)
		i   			= 0
		start_invoice 	= get_fin_invoice_no #'2425'
		voy 			= {}
		voy_array 		= []
		if not voyage:
			append_str 		= ''
			ships_singles 	= []
			for t in vessel_details:
				#print '----1--phele dharshan karo'
				client 	  		  = models.Client.objects.filter(client_name=client_lt,proj_name='CHM').first()
			 	ship_name 		  = t['Ship Name']
			 	voyage_no  		  = t['Voyage No']
			 	voyage_id  		  = t['Voyage ID']
			 	disch_port 		  = t['Disch Port']
			 	format_disch_date = t['Disch Date']
			 	max_dische		  = x['finance_date']
			 	disch_date_for    = datetime.strptime(format_disch_date, "%d-%b-%Y").strftime('%Y-%m-%d')
			 	
			 	vm_name    		  = t['VM Name']
			 	today      		  = update_invoice_date #datetime.now().date()
			 	chm 	   		  = 'CHM'
			 	try:
			 		account_type  = t['account_tab']
			 	except:
			 		account_type  = None
			 	#address 		  = ''

				try:
					address = t['account_address']
				except:
					address = None

			 	if account_type:
			 		accounting_tab = account_type
			 	else:
			 		accounting_tab = None


				if client_lt=='Navig8':
					check_validate = models.invoice.objects.filter(ship_name=ship_name,voyage_no=voyage_no,client_id=client,proj_name='CHM',cancel_invoice='0',vessel_type=vessel_type).count()
				else:
					check_validate = models.invoice.objects.filter(ship_name=ship_name,voyage_no=voyage_no,client_id=client,proj_name='CHM',cancel_invoice='0').count()

			 	if check_validate>0:
			 		return HttpResponse(json.dumps('error'))

			 	client_details = models.Client.objects.filter(client_name=client_lt,proj_name=proj_name).first()
				if proj_name=='CHM' and client_details.currency_type=='INR':
					currency_type = get_invoice_no(client_details.currency_type)
					for x in currency_type:
						split_no  = x.split("/")
						ser_first = int(split_no[0])+i
						if ser_first>=0 and ser_first<=9:
						 	append_str='000'
						if ser_first>=10 and ser_first<=99:
							append_str='00'
						if ser_first>=100 and ser_first<=999:
							append_str='0'
						if ser_first>=1000 and ser_first<=9999:
							append_str=''

						if client_details.currency_type=='INR':
							start_invoices = get_fin_invoice_no #'2425'
						elif client_details.currency_type=='USD':
							start_invoices = get_fin_invoice_no #'2425'
						invoice_n 	= str(append_str+ str(ser_first))+"/"+str(start_invoices)
				elif proj_name=='CHM' and client_details.currency_type=='USD':
					currency_type = get_invoice_no(client_details.currency_type)
					for x in currency_type:
						split_no  = x.split("/")
						ser_first = int(split_no[0])+i
						if ser_first>=0 and ser_first<=9:
						 	append_str='000'
						if ser_first>=10 and ser_first<=99:
							append_str='00'
						if ser_first>=100 and ser_first<=999:
							append_str='0'
						if ser_first>=1000 and ser_first<=9999:
							append_str=''
						if client_details.currency_type=='INR':
							start_invoices = get_fin_invoice_no #'2425'
						elif client_details.currency_type=='USD':
							start_invoices = get_fin_invoice_no #'2425'
						invoice_n 	= str(append_str+ str(ser_first))+"/"+str(start_invoices)					
				else:
					if merge=="1":
						currency_type = get_invoice_no(client_details.currency_type)
						for x in currency_type:
							split_no  = x.split("/")
							ser_first = int(split_no[0])+i
							if ser_first>=0 and ser_first<=9:
							 	append_str='000'
							if ser_first>=10 and ser_first<=99:
								append_str='00'
							if ser_first>=100 and ser_first<=999:
								append_str='0'
							if ser_first>=1000 and ser_first<=9999:
								append_str=''

							if client_details.currency_type=='INR':
								start_invoices = get_fin_invoice_no #'2425'
							elif client_details.currency_type=='USD':
								start_invoices = get_fin_invoice_no #'2425'
							invoice_n 	= str(append_str+ str(ser_first))+"/"+str(start_invoices)


				check = models.vessel_selected_invoice.objects.filter(ship_name=ship_name,voyage_no=voyage_no).count()
				if check>0:
				 	save_select = models.vessel_selected_invoice.objects.filter(ship_name=ship_name,voyage_no=voyage_no).first()
				else:
					save_select = models.vessel_selected_invoice()

				if client_lt=='Shell NWE':
					if len(ship_name)>1:
						voy_array.append(voyage_no)
						voyage_number = voy_array
					else:
						voyage_number = voyage_no
					currency_type = get_invoice_no(client_details.currency_type)				
					for x in currency_type:
						split_no  = x.split("/")
						ser_first = int(split_no[0])+i
						if ser_first>=0 and ser_first<=9:
						 	append_str='000'
						if ser_first>=10 and ser_first<=99:
							append_str='00'
						if ser_first>=100 and ser_first<=999:
							append_str='0'
						if ser_first>=1000 and ser_first<=9999:
							append_str=''

						if client_details.currency_type=='INR':
							start_invoices = get_fin_invoice_no #'2425'
						elif client_details.currency_type=='USD':
							start_invoices = get_fin_invoice_no #'2425'
						invoice_n 	= str(append_str+ str(ser_first))+"/"+str(start_invoices)				
					if ship_name not in ships_singles:
						ships_singles.append(ship_name)

				else:					
					get_address  			  = models.pool_master.objects.filter(client_id=client.id).first()
					save_select.ship_name     = ship_name
					save_select.voyage_no     = voyage_no
					save_select.today         = today
					save_select.proj_name     = chm
					save_select.voyage_cancel = voyage_id
					save_select.disch_date    = disch_date_for
					save_select.disch_port    = disch_port
					save_select.vm_name    	  = vm_name
					save_select.client_id     = client.id
					save_select.invoice_no    = invoice_n
					save_select.month 		  = start_date
					save_select.vessel_type   = vessel_type # get_address.pool
					try:
						save_select.account_type = accounting_tab
					except:
						pass
					save_select.address 	     = address	
					save_select.nomination_date  = max_dische
					
					try:
						save_select.book_names 	 = t['ref_name']
					except:
						save_select.book_names 	 = None
					
					save_select.save()
					i+=1

			try:
				voy 	   = voyage_number
				voyage_nox = ', '.join(sorted(voy))
			except:
				pass
			#print '-----------',address
			for st in ships_singles:
				get_address  					 = models.pool_master.objects.filter(client_id=client.id).first()
				save_single_vessel 				 = models.vessel_selected_invoice()
				save_single_vessel.ship_name     = st
				save_single_vessel.voyage_no     = voyage_nox
				save_single_vessel.today         = today
				save_single_vessel.proj_name     = chm
				save_single_vessel.voyage_cancel = voyage_id
				save_single_vessel.disch_date    = disch_date_for
				save_single_vessel.disch_port    = disch_port
				save_single_vessel.vm_name    	 = vm_name
				save_single_vessel.client_id     = client.id
				save_single_vessel.month 		 = start_date
				save_single_vessel.invoice_no    = invoice_n
				save_single_vessel.vessel_type   = vessel_type

				try:
					save_single_vessel.account_type  = accounting_tab
				except:
					pass				
				save_single_vessel.address 		 = address			
				# format_nomination_date 		= t['Nomination Date']
			 # 	format_nomination_for    	= datetime.strptime(format_nomination_date, "%d-%b-%Y").strftime('%Y-%m-%d')
				# print '-------->>>>>>>>',format_nomination_for
				save_single_vessel.nomination_date = max_dische
				save_single_vessel.save()
		else:
			#print '----2--phele dharshan karo'
			append_str 	  = ''
			ship_single   = []
			voyage_number = ''
			address       = ''
			for x in chm_array:
				if x['voyage_id'] in voyage:
					client 	  		   = models.Client.objects.filter(client_name=x['client_name'],proj_name='CHM').first()
					ship_name 		   = x['ship_name']
					voyage_no  		   = x['voyage_no']
					voyage_id  		   = x['voyage_id']
					disch_port 		   = x['disch_port']
					disch_date 		   = x['disch_date']
					max_disch		   = x['finance_date']
					format_disch_date  = disch_date
					disch_date_for     = format_disch_date #datetime.strptime(format_disch_date, "%d-%b-%Y").strftime('%Y-%m-%d')	
					ref_names 		   = x['ref_name']
					#print '-----------------====',max_disch		
					vm_name    		   = x['vm_name']
					today      		   = update_invoice_date
					chm 	   		   = 'CHM'
					try:
						accounting_tab = x['account_tab']
					except:
						accounting_tab = None




					try:
				 		addressx = x['account_address']
				 	except:
				 		addressx = None

					if client_lt=='Navig8':
						check_validate = models.invoice.objects.filter(ship_name=ship_name,voyage_no=voyage_no,client_id=client,proj_name='CHM',cancel_invoice='0',vessel_type=vessel_type).count()
					else:
						check_validate = models.invoice.objects.filter(ship_name=x['ship_name'],voyage_no=x['voyage_no'],client_id=client,proj_name='CHM',cancel_invoice='0').count()
					if check_validate>0:
						return HttpResponse(json.dumps('error'))

					client_details = models.Client.objects.filter(client_name=client_lt,proj_name=proj_name).first()
					currency_type  = get_invoice_no(client_details.currency_type)
					for x in currency_type:
						split_no  = x.split("/")
						ser_first = int(split_no[0])+i
						if ser_first>=0 and ser_first<=9:
						 	append_str='000'
						if ser_first>=10 and ser_first<=99:
							append_str='00'
						if ser_first>=100 and ser_first<=999:
							append_str='0'
						if ser_first>=1000 and ser_first<=9999:
							append_str=''

						if client_details.currency_type=='INR':
							start_invoices = get_fin_invoice_no #'2425'
						elif client_details.currency_type=='USD':
							start_invoices = get_fin_invoice_no #'2425'
						invoice_n 	= str(append_str+ str(ser_first))+"/"+str(start_invoices)

					check = models.vessel_selected_invoice.objects.filter(ship_name=ship_name,voyage_no=voyage_no).count()
					if check>0:
					 	save_select = models.vessel_selected_invoice.objects.filter(ship_name=ship_name,voyage_no=voyage_no).first()
					else:
						save_select = models.vessel_selected_invoice()

					if client_lt=='Shell NWE':
						shp_name       		= ship_name
						vo_no  	       		= voyage_no
						deta           		= models.generate_for_vessel()
						deta.ship_name 		= shp_name
						deta.voyage_no 		= vo_no
						deta.discharge_port = disch_port						
						deta.nomination_date = max_disch
						deta.save()

						if len(ship_name)>1:						
							voy_array.append(voyage_no)
							voyage_number = voy_array
						else:
							voyage_number = voyage_no

						currency_type = get_invoice_no(client_details.currency_type)
						for x in currency_type:
							split_no  = x.split("/")
							ser_first = int(split_no[0])
							if ser_first>=0 and ser_first<=9:
							 	append_str='000'
							if ser_first>=10 and ser_first<=99:
								append_str='00'
							if ser_first>=100 and ser_first<=999:
								append_str='0'
							if ser_first>=1000 and ser_first<=9999:
								append_str=''

							if client_details.currency_type=='INR':
								start_invoices = '1617'
							elif client_details.currency_type=='USD':
								start_invoices = get_fin_invoice_no  #'2425'
							invoice_n 	= str(append_str+ str(ser_first))+"/"+str(start_invoices)

						if ship_name not in ship_single:
							ship_single.append(ship_name)
					else:
						#print '---------',
						get_address  			  	= models.pool_master.objects.filter(client_id=client.id).first()
						save_select.ship_name     	= ship_name
						save_select.voyage_no     	= voyage_no
						save_select.today         	= today
						save_select.proj_name     	= chm
						save_select.voyage_cancel 	= voyage_id
						save_select.disch_date    	= disch_date_for
						save_select.disch_port    	= disch_port
						save_select.vm_name    	  	= vm_name
						save_select.client_id     	= client.id
						save_select.invoice_no    	= invoice_n
						save_select.month 		  	= start_date
						save_select.vessel_type   	= vessel_type
						save_select.account_type   	= accounting_tab
						save_select.address 	    = get_address.address #addressx
						save_select.nomination_date = max_disch
						save_select.book_names  	= ref_names					
						save_select.save()
						i+=1					
			
			try:
				voy 	   = voyage_number
				voyage_nox = ', '.join(sorted(voy))
			except:				
				pass

			#for vx in ship_single:
			split = invoice_n.split('/')
			cc 	  = split[0]
			dd 	  = split[1]
			v  	  = 0
			ww    = []		
			for st in ship_single:
				voyage_deails = models.generate_for_vessel.objects.filter(ship_name=st)
				#print '========...',chm_array[v]['disch_port']
				try:
					formatdischdate = chm_array[v]['disch_date']
					disch_datefor   = format_disch_date #datetime.strptime(formatdischdate, "%d-%b-%Y").strftime('%Y-%m-%d')
				except:
					disch_datefor   = ''

				invoice_first 					 = int(cc)+v
				invoice_sec   					 = str(invoice_first)+'/'+str(dd)
				get_address  					 = models.pool_master.objects.filter(client_id=client.id).first()
				save_single_vessel 				 = models.vessel_selected_invoice()
				save_single_vessel.ship_name     = st
				we = []
				for r in voyage_deails:				
					we.append(r.voyage_no)			
				save_single_vessel.voyage_no     = ",  ".join(we) #voyage_nox			
				save_single_vessel.today         = today
				save_single_vessel.proj_name     = chm
				save_single_vessel.voyage_cancel = chm_array[v]['voyage_id']
				save_single_vessel.disch_date    = disch_datefor
				save_single_vessel.disch_port    = r.discharge_port #chm_array[v]['disch_port'] #disch_port
				save_single_vessel.vm_name    	 = chm_array[v]['vm_name'] #vm_name
				save_single_vessel.client_id     = client.id
				save_single_vessel.month 		 = start_date
				save_single_vessel.invoice_no    = invoice_sec
				save_single_vessel.vessel_type   = vessel_type
				save_single_vessel.account_type  = accounting_tab
				save_single_vessel.address  	 = addressx
				save_single_vessel.nomination_date = max_disch
				save_single_vessel.save()
				#print '=========',r.discharge_port
				v+=1
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

############################################################################
def get_invoice_no(currency_type):
	invoice_no_arr = []
	start_invoice  = '1718'
	if currency_type=='USD':
		invoice_count   = models.invoice.objects.filter(usd='USD').count()
	elif currency_type=='INR':
		invoice_count   = models.invoice.objects.filter(inr='INR').count()

	if invoice_count:
		if currency_type=='USD':
			max_number 	= models.invoice.objects.filter(usd='USD').order_by('-invoice_no').first()
		elif currency_type=='INR':
			max_number 	= models.invoice.objects.filter(inr='INR').order_by('-invoice_no').first()

		ser_no    	= max_number.invoice_no
		split_no  	= ser_no.split("/")
		ser_first 	= int(split_no[0])+1
		append_str 	= ''
		if ser_first>=0 and ser_first<=9:
		 	append_str=''
		if ser_first>=10 and ser_first<=99:
			append_str=''
		if ser_first>=100 and ser_first<=999:
			append_str=''
		if ser_first>=1000 and ser_first<=9999:
			append_str=''
		invoice_x 	= str(append_str+ str(ser_first))+"/"+str(start_invoice)
	else:
		invoice_x 	= "0001/"+str(start_invoice)

	invoice_no_arr.append(invoice_x)
	return invoice_no_arr

############################# boss
def submit_invoice_for_boss(request):
	if request.user.is_authenticated():


		return render_to_response("invoice_display/boss/submit_invoice.html")
	else:
		return HttpResponseRedirect('/it/user_login')

def address_entry(request):
	if request.user.is_authenticated():
		#api_url 	   	= "http://0.0.0.0:8003/api/get_data_boss/"
		api_url 	   	= "https://bossv2.bwesglobal.com/api/get_data_boss/"
		api_method     	= "GET"
		parameters     	= {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response       	= requests.get(api_url, params=parameters,verify=False)
		boss_array     	= json.loads(response.content)
		boss_array     	= boss_array['boss_array']
		boss_ship      	= []
		ship_array 	   	= []
		chm_array  		= []
		merge_ship 		= []
		for sh in boss_array:
			boss_ship_name = sh['ship_name']
			if sh['ship_name'] not in boss_ship:
				boss_ship.append(sh['ship_name'])

		for x in boss_ship:
			check = models.Ship.objects.filter(ship_name=x).first()
			if check:
				select_ship_name = check.ship_name
			else:
				select_ship_name = x


			ship_array.append({
				'select_ship_name' : select_ship_name,
				})

		context={
		'ship_array' : ship_array,
		}
		return render_to_response("invoice_display/address_entry.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')

def submit_ship_address_for_address(request):
	if request.user.is_authenticated():
		ship_name 	 = json.loads(request.GET['ship_list'])
		address 	 = json.loads(request.GET['address'])
		email 		 = json.loads(request.GET['email'])
		email_c 	 = json.loads(request.GET['email_c'])
		vm_name 	 = json.loads(request.GET['vm_name'])
		#api_url 	 = "http://0.0.0.0:8003/api/get_data_boss/"
		api_url 	 = "https://bossv2.bwesglobal.com/api/get_data_boss/"
		api_method   = "GET"
		parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response     = requests.get(api_url, params=parameters,verify=False)
		boss_array   = json.loads(response.content)
		boss_array   = boss_array['boss_array']
		client_name  = boss_array[0]['client_name'] #client_name_details[0]['client_name']
		clientID 	 = models.Client.objects.filter(client_name=client_name,proj_name='BOSS').first()
		check 	 	 = models.Ship.objects.filter(ship_name=ship_name,client_id=str(clientID)).count()
		if check>0:
			save_address = models.Ship.objects.filter(ship_name=ship_name,client_id=str(clientID)).first()
		else:
			save_address = models.Ship()
		save_address.ship_name 	= ship_name
		save_address.address 	= address
		save_address.email 		= email
		save_address.email_cc   = email_c
		save_address.client_id  = str(clientID)
		save_address.vm_name	= vm_name
	 	#save_address.save()

		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')


@csrf_exempt
def combined_vessel_details(request):
	if request.user.is_authenticated():
		models.vessel_selected_invoice.objects.all().delete()
		voyage_array   = json.loads(request.POST['selection_array'])
		start_date     = json.loads(request.POST['start_date'])
		end_date	   = json.loads(request.POST['end_date'])
		if start_date and end_date:
			start_date_for = datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y-%m-%d')
			end_date_for   = datetime.strptime(end_date,"%m/%d/%Y").strftime('%Y-%m-%d')
			month_start    = datetime.strptime(start_date,"%m/%d/%Y").strftime('%b')
			month_end      = datetime.strptime(end_date,"%m/%d/%Y").strftime('%b')
		else:
			today = datetime.now().date()
			start_date_for = datetime.now().date()
			end_date_for   = datetime.now().date()
			month_start    = datetime.today().strftime("%b")
			month_end      = datetime.today().strftime("%b")
		voyage 		   = [int(x) for x in voyage_array]
		#api_url 	   = "http://0.0.0.0:8003/api/get_data_boss/"
		api_url 	   = "https://bossv2.bwesglobal.com/api/get_data_boss/"
		api_method     = "GET"
		parameters     = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response       = requests.get(api_url, params=parameters,verify=False)
		boss_array     = json.loads(response.content)
		boss_array     = boss_array['boss_array']
		boss_append    = []
		delete 		   = models.vessel_selected_invoice.objects.all().delete()
		today 		   = datetime.now().strftime('%Y')
		if today < int(today)+1:
			start_invoice = '1718'
		else:
			start_invoice = '1718'
		invoice_count   = models.invoice.objects.all().count()
		if invoice_count:
			max_number 	= models.invoice.objects.all().order_by('-invoice_no').first()
			ser_no    	= max_number.invoice_no
			split_no  	= ser_no.split("/")
			ser_first 	= int(split_no[0])+1
			append_str 	= ''
			if ser_first>=0 and ser_first<=9:
			 	append_str='000'
			if ser_first>=10 and ser_first<=99:
				append_str='00'
			if ser_first>=100 and ser_first<=999:
				append_str='0'
			if ser_first>=1000 and ser_first<=9999:
				append_str=''

			invoice_no 	= str(append_str+ str(ser_first))+"/"+str(start_invoice)
		else:
			invoice_no 	= "0001/"+str(start_invoice)

		for x in boss_array:
			if x['voyage_id'] in voyage:
				client 	= models.Client.objects.filter(client_name=x['client_name']).first()
				ship_name  			= x['ship_name']
				voyage_no  			= x['voyage_no']
				voyage_id  			= x['voyage_id']
				disch_port 			= x['disch_port']
				disch_date 			= x['disch_date']
				vm_name    			= x['vm_name']
				format_disch_date 	= disch_date
				disch_date_for    	= datetime.strptime(format_disch_date, "%d-%b-%Y").strftime('%Y-%m-%d')
				today      			= datetime.now().date()
				boss 	   			= 'BOSS'
				check 				= models.vessel_selected_invoice.objects.filter(ship_name=ship_name,voyage_no=voyage_no).count()
				if check>0:
					save_select = models.vessel_selected_invoice.objects.filter(ship_name=ship_name,voyage_no=voyage_no).first()
				else:
					save_select = models.vessel_selected_invoice()
				save_select.ship_name     = ship_name
				save_select.voyage_no     = voyage_no
				save_select.today         = today
				save_select.proj_name     = boss
				save_select.voyage_cancel = voyage_id
				save_select.disch_date    = disch_date_for
				save_select.disch_port    = disch_port
				save_select.vm_name    	  = vm_name
				save_select.client_id     = client.id
				save_select.month 		  = start_date_for
				save_select.invoice_no    = invoice_no
				save_select.save()

				check = models.invoice.objects.filter(ship_name=x['ship_name'],voyage_no=x['voyage_no'],month=start_date_for).count()
				if check>0:
					return HttpResponse(json.dumps('error'))
				else:
					invoice_details = models.invoice()
				invoice_details.ship_name 	= x['ship_name']
				invoice_details.vm_name   	= x['vm_name']
				invoice_details.voyage_id 	= x['voyage_id']
				invoice_details.proj_name 	= 'BOSS'
				invoice_details.today	 	= datetime.now().date()
				invoice_details.client_id   = client.id
				invoice_details.invoice_no 	= invoice_no
				invoice_details.month       = start_date_for
				invoice_details.voyage_no   = x['voyage_no']
				invoice_details.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')



def selected_vessel_details(request):
	selected_vessel = models.vessel_selected_invoice.objects.all()
	vessel 			= []
	# invoice_count 	= models.invoice.objects.all().count()
	# max_number 	  	= models.invoice.objects.all().order_by('-invoice_no').first()
	# ser_no 			= max_number.invoice_no

	# max_number 	  	= models.invoice.objects.all().order_by('-invoice_no').first()
	# ser_no    		= max_number.invoice_no
	# split_no  		= ser_no.split("/")
	# ser_first 		= int(split_no[0])+1
	# append_str = ''
	# if ser_first>=0 and ser_first<=9:
	#  	append_str='000'
	# if ser_first>=10 and ser_first<=99:
	# 	append_str='00'
	# if ser_first>=100 and ser_first<=999:
	# 	append_str='0'
	# if ser_first>=1000 and ser_first<=9999:
	# 	append_str=''

	# invoice_no 	= str(append_str+ str(ser_first))+"/1718"
	today = datetime.now().strftime('%Y')
	if today < int(today)+1:
		start_invoice = '1718'
	else:
		start_invoice = '1718'
	invoice_count = models.invoice.objects.all().count()
	# serial_number = models.invoice.objects.all().order_by('-invoice_no').first()
	if invoice_count:
		max_number 	= models.invoice.objects.all().order_by('-invoice_no').first()
		ser_no    	= max_number.invoice_no
		split_no  	= ser_no.split("/")
		ser_first 	= int(split_no[0])+1
		append_str 	= ''
		if ser_first>=0 and ser_first<=9:
		 	append_str='000'
		if ser_first>=10 and ser_first<=99:
			append_str='00'
		if ser_first>=100 and ser_first<=999:
			append_str='0'
		if ser_first>=1000 and ser_first<=9999:
			append_str=''
		invoice_no 	= str(append_str+ str(ser_first))+"/"+str(start_invoice)
	else:
		invoice_no 	= "0001/"+str(start_invoice)
	
	bluewater   = models.BlueWater.objects.all().order_by('-id').first()
	disable 	= ''
	for x in selected_vessel:
		rate = 0
		price	= 0
		ship_address  = models.Ship.objects.filter(ship_name=x.ship_name).first()
		if ship_address:
			client_name = ship_address.client.client_name
			address 	= ship_address.address
			curr_type   = ship_address.client.currency_type
			if curr_type=='USD':
				rate  = ship_address.client.rate
				price = ship_address.client.price
			elif curr_type=='INR':
				rate  = ship_address.client.rate
				price = ship_address.client.price
		else:
			address 	= ''
			client_name = ''
		check_address = models.Ship.objects.filter(ship_name=x.ship_name).count()
		if check_address>0:
			alert 		= ''
			color 		= ''
			disable 	= ''
			href 		= ""
		else:
			alert   	= 'Please Fill up address of '+str(x.ship_name)
			color   	= 'red'
			disable 	= 'disabled'
			href    	= '/it/address_entry/'
		
		amount = (rate*price)
		vessel.append({
			'ship_name' : x.ship_name,
			'voyage_no' : x.voyage_no,
			'proj_name' : x.proj_name,
			'address'   : ship_address,
			'invoice_no': invoice_no,
			'bluewater' : bluewater.tin_number,
			'client'    : client_name,
			'disch_port': x.disch_port,
			'disch_date': x.disch_date,
			'vm_name'   : x.vm_name,
			'alert' 	: alert,
			'colors' 	: color,
			'href'  	: href,
			'rate' 		: rate,
			'price' 	: price,
			'amount'    : amount,
			})
	context={
	'vessel'  : vessel,
	'disable' : disable,
	}
	return render_to_response("invoice_display/boss/generate_invoice_boss.html",context)


@csrf_exempt
def submit_invoice_boss(request):
	item_details  = json.loads(request.POST['items'])
	invoice_date  = json.loads(request.POST['invoice_date'])
	#invoice_no   = json.loads(request.POST['invoice_no'])
	client_name   = json.loads(request.POST['client_name'])
	invoice_count = models.invoice.objects.all().count()
	today 		  = datetime.now().strftime('%Y')

	if today < int(today)+1:
		start_invoice = '1718'
	else:
		start_invoice = '1718'
	if invoice_count:
		max_number 	= models.invoice.objects.all().order_by('-invoice_no').first()
		ser_no    	= max_number.invoice_no
		split_no  	= ser_no.split("/")
		ser_first 	= int(split_no[0])+1
		append_str 	= ''
		if ser_first>=0 and ser_first<=9:
		 	append_str='000'
		if ser_first>=10 and ser_first<=99:
			append_str='00'
		if ser_first>=100 and ser_first<=999:
			append_str='0'
		if ser_first>=1000 and ser_first<=9999:
			append_str=''
		invoice_n 	= str(append_str+ str(ser_first))+"/"+str(start_invoice)
	else:
		invoice_n 	= "0001/"+str(start_invoice)
	for i in item_details:
		#if i['Vessel']!='Add a row':
		vessel_name = i['Vessel']
		voyage_no   = i['Voyage No']
		address 	= i['Address']
		disch_port  = i['Disch Port']
		disch_date  = i['Disch Date']
		qty 		= i['Qty']

		client_id   = models.Client.objects.filter(client_name=client_name).first()
		price 		= client_id.price
		rate  		= client_id.rate
		check 		= models.invoice.objects.filter(ship_name=i['Vessel'],voyage_no= i['Voyage No'],client_id=client_id.id).count()
		if check>0:
		 	return HttpResponse(json.dumps("already"))
		else:
			submit_invoice = models.invoice()

		submit_invoice.invoice_no 	= invoice_n
		submit_invoice.invoice_date = invoice_date
		submit_invoice.ship_name    = i['Vessel']
		submit_invoice.voyage_no    = i['Voyage No']
		submit_invoice.proj_name    = 'BOSS'
		submit_invoice.address 		= i['Address']
		submit_invoice.disch_date   = i['Disch Date']
		submit_invoice.disch_port   = i['Disch Port']
		submit_invoice.client_id    = str(client_id)
		submit_invoice.vm_name 		= i['VM Name']
		submit_invoice.price 	 	= price
		submit_invoice.rate 		= rate
		submit_invoice.save()

	return HttpResponse(json.dumps('done'))

@csrf_exempt
def vaild_boss_invoice_details(request):
	if request.user.is_authenticated():		
		ship_name 			= json.loads(request.POST['ship_name'])
	 	ship_class    		= json.loads(request.POST['ship_class'])
	 	client_name 		= json.loads(request.POST['client_name'])
	 	start_date_for  	= request.POST['start_date_for']
	 	format_month_name   = datetime.strptime(start_date_for, "%m/%d/%Y").strftime('%B')
	 	format_year_name    = datetime.strptime(start_date_for, "%m/%d/%Y").strftime('%Y')		
	 	remove_vessel_space = ship_name.replace('_', ' ')		 	
		client_details 		= models.Client.objects.filter(client_name=client_name,proj_name='BOSS').first()
		vessel_name 		= remove_vessel_space.strip()
		
		try:
			qry    			= "SELECT * FROM it_invoice where proj_name='BOSS' and vessel_type='"+str(ship_class)+"' and month_name='"+str(format_month_name)+"' and ship_name='"+str(vessel_name)+"' and cancel_invoice="'0'" and Year(month)='"+str(format_year_name)+"'"
			cursor 			= connection.cursor()
			cursor.execute(qry)
			invoice_details = cursor.fetchall()
			for x in invoice_details:
				if x>0:
					display_button = 'none'
					shipname       = ship_name
				else:
					display_button = ''
					shipname       = ship_name

			context={
			'shipname'   	 : shipname,
			'display_button' : display_button,
			}	
		except:
			context={
			'shipname'   	 : '',
			'display_button' : '',
			}
		

		return HttpResponse(json.dumps(context))
	else:
	 	return HttpResponseRedirect('/it/user_login')

def selected_client_boss(request):
	#api_url 	 = "http://0.0.0.0:8003/api/get_data_boss/"
	api_url 	 = "https://bossv2.bwesglobal.com/api/get_data_boss/"
	api_method   = "GET"
	parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
	response     = requests.get(api_url, params=parameters,verify=False)
	boss_array   = json.loads(response.content)
	boss_array   = boss_array['boss_array']
	boss_append  = []
	ship_array   = []
	client_array = []
	client 		 = []
	for x in boss_array:
		if x['ship_name'] not in ship_array:
			ship_array.append(x['ship_name'])

	for sh in ship_array:
		client_select = models.Ship.objects.filter(ship_name=sh).first()
		if client_select:
			if client_select.client.proj_name=='BOSS':
				client_name = client_select.client.client_name
				if client_name not in client_array:
					client_array.append(client_name)

	client_array1 = models.Client.objects.filter(proj_name='BOSS').exclude(client_name='BW Anurag').exclude(client_name='Test').exclude(client_name='Demo Client')
	vessel_arr    = []
	for cl in client_array1:
		client.append({
			'client_name' : cl.client_name,
			})
	for w in boss_array:
		if w['ship_class'] not in vessel_arr:
			vessel_arr.append(w['ship_class'])

	ship_type = []
	for i in vessel_arr:
		if i!=None:
			ship_type.append({
				'vessel_type' : i
				})
	context={
	'client' 	: client,
	'ship_type' : ship_type,
	}
	return render_to_response("invoice_display/boss/selected_client_boss.html",context)

@csrf_exempt
def using_date_select_boss_details(request):
	# try:
	# 	name  		 = json.loads(request.POST['client_name'])
	# 	start_date 	 = json.loads(request.POST['start_date'])
	# 	end_date 	 = json.loads(request.POST['end_date'])
	# 	ship_type    = json.loads(request.POST['vessel_type'])
	# except:
	# 	ship_type    = 0

	# api_url 	 = "http://0.0.0.0:8003/api/get_data_boss/"
	# api_method   = "GET"
	# parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
	# response     = requests.get(api_url, params=parameters)
	# boss_array   = json.loads(response.content)
	# boss_array   = boss_array['boss_array']
	# voyage_array = []
	# ship_details = []
	# ship_class   = ''
	# for x in boss_array:
	# 	if start_date!='NaN-NaN-NaN' and end_date!='NaN-NaN-NaN' and ship_type!="0":
	# 		if x['noon_date']>=start_date and x['noon_date']<=end_date:
	# 			if name!=0:
	# 				if ship_type!=0:
	# 					if x['client_name']==name:
	# 						if x['ship_class']==ship_type:
	# 							if x['ship_name'] not in voyage_array:
	# 								first_noon = x['noon_date']
	# 								last_noon  = x['last_noon_date']
	# 								voyage_array.append(x['ship_name'])

	# 	if start_date!='NaN-NaN-NaN' and end_date!='NaN-NaN-NaN' and ship_type=="0":
	# 		if x['noon_date']>=start_date and x['noon_date']<=end_date:
	# 			if name!=0:
	# 				if x['client_name']==name:
	# 					if x['ship_name'] not in voyage_array:
	# 						first_noon = x['noon_date']
	# 						last_noon  = x['last_noon_date']
	# 						voyage_array.append(x['ship_name'])

	# 	if start_date=='NaN-NaN-NaN' and end_date=='NaN-NaN-NaN':
	# 			if x['ship_name'] not in voyage_array:
	# 				if name!=0:
	# 					if x['client_name']==name:
	# 						first_noon  = x['noon_date']
	# 						last_noon   = x['last_noon_date']
	# 						voyage_array.append(x['ship_name'])



	# 	if start_date=='NaN-NaN-NaN' and end_date=='NaN-NaN-NaN' and ship_type=="0" and name=="0":
	# 		if x['ship_name'] not in voyage_array:
	# 			first_noon  = x['noon_date']
	# 			last_noon   = x['last_noon_date']
	# 			voyage_array.append(x['ship_name'])



	# s_no=1
	# for sh in voyage_array:
	# 	if start_date!='NaN-NaN-NaN' and end_date!='NaN-NaN-NaN':
	# 		startdate = start_date
	# 		enddate   = end_date
	# 	else:
	# 		years 	  = datetime.now().strftime('%Y')
	# 		startdate = str(int(years)-1)+'-01-01'
	# 		enddate   = str(years)+'-12-31'

	# 	import MySQLdb
	# 	import connection
	# 	conn   = connection.get_connection()
	# 	cursor = conn.cursor(MySQLdb.cursors.DictCursor)

	# 	if ship_type!="0":
	# 		QrySS  = "SELECT max(av.date),min(av.date),sh.ship_name,vm.name,vg.id,cl.id as client_id,sh.ship_class FROM va_finale.vast_voyage vg,va_finale.vast_actual_voyage_schedule av,va_finale.vast_port vp,va_finale.vast_voyage_manager vm,va_finale.vast_ship sh,va_finale.vast_client cl,va_finale.vast_pool pl where vg.id=av.voyage_id and vg.id=vp.voyage_id and sh.id=vg.ship_id and vm.client_id=cl.id and vm.id=vg.voyage_manager_id and pl.id=sh.pool_id and pl.client_id=cl.id and av.date>='"+str(startdate)+"' and av.date<='"+str(enddate)+"' and sh.ship_name='"+str(sh)+"' and sh.ship_class='"+str(ship_type)+"' and vg.voyage_mod is null group by vg.ship_id"
	# 	else:
	# 		QrySS  = "SELECT max(av.date),min(av.date),sh.ship_name,vm.name,vg.id,cl.id as client_id,sh.ship_class FROM va_finale.vast_voyage vg,va_finale.vast_actual_voyage_schedule av,va_finale.vast_port vp,va_finale.vast_voyage_manager vm,va_finale.vast_ship sh,va_finale.vast_client cl,va_finale.vast_pool pl where vg.id=av.voyage_id and vg.id=vp.voyage_id and sh.id=vg.ship_id and vm.client_id=cl.id and vm.id=vg.voyage_manager_id and pl.id=sh.pool_id and pl.client_id=cl.id and av.date>='"+str(startdate)+"' and av.date<='"+str(enddate)+"' and sh.ship_name='"+str(sh)+"' and vg.voyage_mod is null group by vg.ship_id"

	# 	cursor.execute(QrySS)
	# 	client_name_details   = cursor.fetchall()
	# 	ship_class = ''
	# 	for i in client_name_details:
	# 		if start_date!='NaN-NaN-NaN':
	# 			months = datetime.strptime(start_date,"%Y-%m-%d").strftime('%m')
	# 		else:
	# 			months = datetime.now().strftime('%m')
	# 		check  = models.invoice.objects.filter(ship_name=i['ship_name'],month__month=months).count()
	# 		if check>0:
	# 			show = 'none'
	# 		else:
	# 			show = ''

	# 		first  		  	= i['min(av.date)']
	# 		for_first_date 	= first.strftime("%d-%b-%Y")
	# 		last  		  	= i['max(av.date)']
	# 		for_last_date 	= last.strftime("%d-%b-%Y")
	# 		#print '________>>>>>>',i['ship_class']
	# 		try:
	# 			ship_class  = i['ship_class']
	# 		except:
	# 			ship_class  = ''

	# 		ship_details.append({
	# 		'ship_name'  : i['ship_name'],
	# 		'vm_name'    : i['name'],
	# 		'first_noon' : str(for_first_date),
	# 		'last_noon'  : str(for_last_date),
	# 		'voyage_id'  : i['id'],
	# 		's_no' 		 : s_no,
	# 		'show' 		 : show,
	# 		'start_date' : start_date,
	# 		'end_date'   : end_date,
	# 		'ship_class' : ship_class,
	# 		})
	# 		s_no+=1
	# context={
	# 'ship_details' : ship_details
	# }
	#return HttpResponse(json.dumps(context))
	return HttpResponse(json.dumps('done'))

@csrf_exempt
def submit_selected_boss(request):
	if request.user.is_authenticated():
		from time import strptime
		from calendar import monthrange
		sums 				   = 0
		usd_amt 			   = 0
		start_date 	 	  	   = json.loads(request.POST['start_date'])
		end_date     	  	   = json.loads(request.POST['end_date'])
		boss_selection 	  	   = json.loads(request.POST['selection_array'])
		update_invox_date 	   = json.loads(request.POST['update_invoice_date'])
		year_name 		  	   = datetime.strptime(start_date, "%m/%d/%Y").strftime('%Y')
		month_number      	   = datetime.strptime(start_date, "%m/%d/%Y").strftime('%m')
		start_date_format 	   = datetime.strptime(start_date, "%m/%d/%Y").strftime('%B')
		prev_mont 			   = int(month_number)-1
		if prev_mont==0:
			prev_month = 12
			year_diff  = int(year_name)-1
		else:
			prev_month = prev_mont
			year_diff  = int(year_name)

		get_month 	 	  	   = monthrange(int(year_diff),int(prev_month))[1]
		start_date_for 	  	   = str(year_diff)+'-'+str(prev_month)+'-01'
		#print '----->>',(year_diff),'--->>',get_month
		end_date_for   	  	   = str(year_diff)+'-'+str(prev_month)+'-'+str(get_month)
		table2json_ship_table  = json.loads(request.POST['ship_details_table'])
		client_name    		   = json.loads(request.POST['client_name'])
		ship_type      		   = json.loads(request.POST['vessel_type'])
		proj_name      		   = json.loads(request.POST['proj_name'])
		total_vessel  		   = json.loads(request.POST['total_vessel'])
		delete 		   		   = models.vessel_combined_invoice.objects.all().delete()
		tbodyRowCount	 	   = json.loads(request.POST['tbodyRowCount'])
		billing_day 		   = json.loads(request.POST['billing_no_day'])

		f_invoice_no 		   = models.financial_invoice_no.objects.all().order_by('-id').first()
		get_fin_invoice_no     = f_invoice_no.fin_invoice_no
				
		if total_vessel:			
			total_vessel = total_vessel
		else:
			total_vessel = tbodyRowCount		

		if proj_name=='BOSS':
			client_details 	 = models.Client.objects.filter(proj_name='BOSS',client_name=client_name).first()
		if proj_name=='CHM':
			client_details 	 = models.Client.objects.filter(proj_name='CHM',client_name=client_name).first()

		if client_name=='Shell' and client_details.currency_type=='USD' or client_name=='Clearlake' and client_details.currency_type=='USD':
			invoice_count = models.invoice.objects.filter(usd='USD',client__client_name='Shell',proj_name='BOSS').count()
		elif client_name!='Shell' and client_details.currency_type=='INR':
			invoice_count = models.invoice.objects.filter(inr='INR').exclude(client__client_name='Shell',proj_name='BOSS').count()
		else:		
			invoice_count = models.invoice.objects.all().exclude(proj_name='BOSS').count()

		curr_types 	= client_details.currency_type
		today 		= datetime.now().strftime('%Y')
		#start_inv = models.generate_invoice.objects.all().order_by('-invoice_no').first()
		if today > int(today)+1:
			start_invoice = get_fin_invoice_no #'2425'
		else:
			start_invoice = get_fin_invoice_no #'2425'

		if invoice_count:
			if client_details.currency_type=='INR' and client_details.proj_name=='BOSS':
				max_number 	= models.invoice.objects.filter(inr='INR').order_by('-invoice_no').first()
				#print '========1',max_number.invoice_no
			if client_details.currency_type=='INR' and client_details.proj_name=='CHM':
				max_number 	= models.invoice.objects.filter(inr='INR').order_by('-invoice_no').first()
				#print '========2',max_number.invoice_no
			if client_details.currency_type=='USD' and client_details.proj_name=='BOSS':
				max_number 	= models.invoice.objects.filter(usd='USD',proj_name='BOSS').order_by('-invoice_no').first()
				#max_number 	= models.invoice.objects.filter(usd='USD',client__client_name='Shell',proj_name='BOSS').order_by('-invoice_no').first()
				#print '========3',max_number.invoice_no,'====',client_details.currency_type
			if client_details.currency_type=='USD' and client_details.proj_name=='CHM':
				max_number 	= models.invoice.objects.filter(usd='USD',proj_name='CHM').order_by('-invoice_no').first()
				#max_number 	= models.invoice.objects.filter(usd='USD',client__client_name='Shell',proj_name='CHM').order_by('-invoice_no').first()

			ser_no    	= max_number.invoice_no
			split_no  	= ser_no.split("/")
			ser_first 	= int(split_no[0])+1

			append_str 	= ''
			if ser_first>=0 and ser_first<=9:
			 	append_str='000'
			if ser_first>=10 and ser_first<=99:
				append_str='00'
			if ser_first>=100 and ser_first<=999:
				append_str='0'
			if ser_first>=1000 and ser_first<=9999:
				append_str=''
			invoice_no 	= str(append_str+ str(ser_first))+"/"+str(start_invoice)
		else:
			invoice_no 	= "1059/"+str(start_invoice)


		ship_arr   = []
		client_det = models.Client.objects.filter(client_name=client_name,proj_name=proj_name).first()
		if ship_type!="0":
			ship_tails = models.Ship.objects.filter(client_id=client_det,pool_name=ship_type)
		else:
			ship_tails = models.Ship.objects.filter(client_id=client_det)
		
		if not boss_selection:
			print '======Click ho k nahi aya'
			sums 	= 0
			usd_amt = 0	
			v = 0
			cost = 1	

			for ship in table2json_ship_table:
				ship_name 		= ship['Ship Name']			
				client_details	= models.Client.objects.filter(client_name=client_name,proj_name='BOSS').first()
				
				if ship_type!="0":
					xx = models.pool_master.objects.filter(client_id=client_details,pool=ship_type).first()
				else:
					xx = models.pool_master.objects.filter(client_id=client_details).first()

				#try:
				ship_name 			= ship_name
				client 	  			= models.Client.objects.filter(id=xx.client_id,proj_name='BOSS').first()
				submit 	  			= models.vessel_combined_invoice()
				submit.ship_name 	= ship_name.strip()				
				try:
					submit.vm_name  = xx.vm_name
				except:
					submit.vm_name  = xx.vm_name
				submit.proj_name 	= 'BOSS'
				submit.today	 	= update_invox_date #datetime.now().date()
				submit.client_id    = xx.client_id
				submit.invoice_no 	= invoice_no
				submit.month        = start_date_for
				submit.vessel_type  = xx.pool

				try:
					submit.last_port 		= ship['Port Name (From)']
					submit.last_noon_date 	= ship['End Date']
				except:
					submit.last_port 		= None
					submit.last_noon_date 	= None 			
				
				try:
					submit.voyage_id    	= ship['Report ID']		
				except:
					submit.voyage_id    	= None	

				try:
					passage_merge = str(ship['Port Name (From)'])+'-'+str(ship['Port Name (To)'])
					submit.voyage_no    	= passage_merge #ship['Passage']
				except:
					submit.voyage_no    	= None

				
				try:
					getting_cost = models.cost_per_route.objects.filter(route__icontains=passage_merge,client_id__client_name=client_name)
					#print '------',getting_cost					
					for c in getting_cost:
						submit.price = c.cost
				except:
					submit.price = None
				submit.save()
				
				if ship_type!="0":
					if proj_name=='BOSS':
						check = models.invoice.objects.filter(ship_name=ship_name,month=start_date_for,voyage_no=0,vessel_type=ship_type,proj_name='BOSS').count()
					if proj_name=='CHM':
						check = models.invoice.objects.filter(ship_name=ship_name,month=start_date_for,voyage_no=0,vessel_type=ship_type,proj_name='CHM').count()
				else:
					if proj_name=='CHM':
						check = models.invoice.objects.filter(ship_name=ship_name,month=start_date_for,voyage_no=0,proj_name='CHM').count()
					if proj_name=='BOSS':
						check = models.invoice.objects.filter(ship_name=ship_name,month=start_date_for,voyage_no=0,proj_name='BOSS').count()
				if check>0:
				 	return HttpResponse(json.dumps('error'))
				else:
					invoice_details = models.invoice()

				invoice_details.ship_name 	= ship_name.strip()	
				
				try:
					invoice_details.vm_name = xx.vm_name
				except:
					invoice_details.vm_name = xx.vm_name

				
				# if client_name!='Shell':
				# 	try:
				# 		address 		= models.Ship.objects.filter(ship_name=ship_name).first()
				# 		client_address 	= address.address
				# 	except:
				# 		client_address 	= ''
				# else:
				# 	client_address 		= xx.address
				client_address = xx.address


				try:
					currency = xx.client.currency_type
					if currency=='INR' and proj_name=='BOSS':
						inr = 'INR'
						usd = None
					elif currency=='USD' and proj_name=='BOSS':
						usd = 'USD'
						inr = None
				except:
					inr = None
					usd = None
				
				
				try:
					if tbodyRowCount>12:						
						cl_price				= models.Client.objects.filter(proj_name='BOSS',price_type=1,client_name=client_name).first()
						shell_price 			= cl_price.price
						invoice_details.price	= shell_price						
						sums					= client.rate*cl_price.price*total_vessel
						usd_amt					= cl_price.price*total_vessel
					else:
						cl_price 				= models.Client.objects.filter(proj_name='BOSS',price_type=2,client_name=client_name).first()
						shell_price 			= cl_price.price
						invoice_details.price  	= shell_price						
						sums 					= client.rate*cl_price.price*total_vessel
						usd_amt 				= cl_price.price*total_vessel					

				except:
					passage_merge = str(ship['Port Name (From)'])+'-'+str(ship['Port Name (To)'])
					if client_name!='Poompuhar Shipping Corporation Limited' or client_name!='TNPGCL':										
						sums					= client.rate*client.price*total_vessel
						usd_amt					= client.price*total_vessel
						invoice_details.price	= client.price
					else:
						pass

				if client_name=='Poompuhar Shipping Corporation Limited' or client_name=='TNPGCL':			
					check_cost = models.cost_per_route.objects.filter(route__icontains=passage_merge,client_id__client_name=client_name)						
					for v in check_cost:
						
						invoice_details.price = v.cost							
						sums  				  = client.rate*v.cost*total_vessel
						usd_amt 			  = v.cost*total_vessel
				else:
					pass
						
								
												

				invoice_details.proj_name 		= 'BOSS'				
				invoice_details.today	 		= update_invox_date #datetime.now().date()
				invoice_details.client_id   	= xx.client_id
				invoice_details.invoice_no 		= invoice_no
				invoice_details.month       	= start_date_for				
				invoice_details.voyage_no   	= ''
				invoice_details.inr   			= inr
				invoice_details.usd   			= usd
				invoice_details.vessel_type 	= ship_type
				invoice_details.client_address  = client_address				
				
				invoice_details.rate  			= client.rate
				format_month_name 				= datetime.strptime(start_date_for, "%Y-%m-%d").strftime('%B')
				invoice_details.month_name 		= format_month_name
				invoice_details.invoice_date 	= update_invox_date				
				invoice_details.total_amount    = sums				
				invoice_details.usd_amount    	= usd_amt
				#invoice_details.price    		= v.cost
				#print '------------->>>',passage_merge
				try:
					invoice_details.voyage_no   = str(passage_merge)
				except:
					invoice_details.voyage_no   = ''

				try:
					invoice_details.deadwt   	= int(ship['Report ID']) #ship['Passage']
				except:
					invoice_details.deadwt   	= None				
				invoice_details.save()
				# except:
				# 	pass

		else:
			tt=0
			print '======Click ho k aya'	
			for ship in boss_selection:			
				print '------',client_name
				if client_name == 'TNPGCL':
					get_client_id  = 15576
				elif client_name == 'Reliance':
					get_client_id  = 90
				elif client_name=='Ultranav':
					get_client_id  = 8520
				if client_name == 'Apeejay Shipping Limited':
					get_client_id  = 107
				else:
					get_client_id  = client_details



				if ship_type!="0":
					x = models.pool_master.objects.filter(client_id=get_client_id,pool=ship_type).first()
				else:
					x = models.pool_master.objects.filter(client_id=get_client_id).first()
				
				client_details	  = models.Client.objects.filter(client_name=client_name,proj_name='BOSS').first()
				#print '_________________________>>', billing_day[tt]['Billing Days']	
				try:					
				 	bill_day = billing_day[tt]['Billing Days']	
				except:
					bill_day = 0
				#print '---------',client_name,'----',ship
				try:
					bill_dayx = models.merge_billing_day.objects.filter(client_name=client_name,ship_name=ship).first()				
					bill_day  = bill_dayx.no_of_day
				except:
					bill_day  = 0
				#try:
				ship_name = ship	
				client 	  = models.Client.objects.filter(id=x.client_id,proj_name='BOSS').first() #x.client_id
				submit 	  = models.vessel_combined_invoice()
				if client_name!='Poompuhar Shipping Corporation Limited' or client_name!='TNPGCL':
					submit.ship_name = ship_name.strip()	
				else:
					shp_name = ship_name.split('/')			
					submit.ship_name = shp_name[0]
					
				try:
					submit.vm_name  = x.vm_name
				except:
					submit.vm_name  = x.vm_name

				submit.proj_name 	= 'BOSS'
				try:					
					if client_name=='Oldendorff':
						submit.qty 	= bill_day
					else:
						submit.qty 	= 1
				except:
					submit.qty 		= 1

				submit.today	 	= update_invox_date #datetime.now().date()
				submit.client_id    = x.client_id
				submit.invoice_no 	= invoice_no
				submit.month        = start_date_for				
				submit.vessel_type  = x.pool
				try:
					submit.last_port 		= bill_dayx.port_name
					submit.last_noon_date 	= bill_dayx.noon_date
				except:
					submit.last_port 		= None
					submit.last_noon_date 	= None
				
				
				try:
					submit.voyage_id    = shp_name[3]	#ship['Report ID']		
				except:
					submit.voyage_id    = None	

				try:
					submit.voyage_no    = shp_name[2]	#ship['Passage']
				except:
					submit.voyage_no    = None					
				submit.save()
				tt+=1
				
				
				
				if ship_type!="0":
					if proj_name=='BOSS':
						check = models.invoice.objects.filter(ship_name=ship_name,month=start_date_for,voyage_no=0,vessel_type=ship_type,proj_name='BOSS').count()
						print '_____________1'
					if proj_name=='CHM':
						check = models.invoice.objects.filter(ship_name=ship_name,month=start_date_for,voyage_no=0,vessel_type=ship_type,proj_name='CHM').count()
						print '_____________2'
				else:
					if proj_name=='CHM':
						check = models.invoice.objects.filter(ship_name=ship_name,month=start_date_for,voyage_no=0,proj_name='CHM').count()
						print '_____________3'
					if proj_name=='BOSS':
						check = models.invoice.objects.filter(ship_name=ship_name,month=start_date_for,voyage_no=0,proj_name='BOSS').count()
						print '_____________4'
				
				if check>0:				
				 	return HttpResponse(json.dumps('error'))				 	
				else:
					invoice_details = models.invoice()

				if client_name!='Poompuhar Shipping Corporation Limited' or client_name!='TNPGCL':
					invoice_details.ship_name = ship_name.strip()				
				else:
					shp_name = ship_name.split('/')			
					invoice_details.ship_name  	= shp_name[0]					

				#invoice_details.ship_name 	= ship_name.strip()
				try:
					invoice_details.vm_name = x.vm_name
				except:
					invoice_details.vm_name = x.vm_name				

				client_address = x.address

				try:
					currency = x.client.currency_type
					if currency=='INR' and proj_name=='BOSS':
						inr = 'INR'
						usd = None
					elif currency=='USD' and proj_name=='BOSS':
						usd = 'USD'
						inr = None
				except:
					inr = None
					usd = None

				cl_pricez = models.Client.objects.filter(proj_name='BOSS',id=x.client_id,currency_type='USD').first()				
				
				if client_name!='Poompuhar Shipping Corporation Limited' or client_name!='TNPGCL':
					#print '-----',total_vessel
					if total_vessel>12:
						print '-----greater'
						if x.client_id==64:
							if currency!='INR':								
								cl_price 					= models.Client.objects.filter(proj_name='BOSS',client_name=client_name,currency_type='USD').first()
								shell_price 				= cl_price.price
								invoice_details.price  		= shell_price
								sums 						= cl_price.rate*cl_price.price*total_vessel
								usd_amt 					= cl_price.price*total_vessel
							else:							
								sums 						= client.rate*client.price*total_vessel
								usd_amt 					= client.price*total_vessel
								invoice_details.price  		= client.price
								invoice_details.voyage_no   = ''
						else:						
							if x.client_id!=112:
								cl_price 					= models.Client.objects.filter(proj_name='BOSS',id='63',currency_type='USD').first()
								get_price 					= cl_price.price
								invoice_details.price  		= get_price
								sums 						= client.rate*cl_price.price*total_vessel
								usd_amt 					= cl_price.price*total_vessel
							else:
								get_price 					= cl_pricez.price
								invoice_details.price  		= get_price								
								if bill_day>29:
									cl_pricex = cl_pricez.price
								else:
									cl_pricex = 15*(bill_day)
								invoice_details.qty 		= bill_day
								sums 						= cl_pricex*total_vessel
								usd_amt 					= cl_pricex*total_vessel

					elif total_vessel<12:
						print '___smaller'						
						if currency!='INR':
							cl_price 					= models.Client.objects.filter(proj_name='BOSS',client_name=client_name,currency_type='USD').first()
							shell_price 				= cl_price.price
							invoice_details.price  		= cl_price.price
							sums 						= cl_price.rate*cl_price.price*total_vessel							
							usd_amt 					= cl_price.price*total_vessel
							invoice_details.voyage_no  	= ''
						else:
							sums 						= client.rate*client.price*total_vessel
							invoice_details.price  		= client.price	
							usd_amt 					= client.price*total_vessel	
					else:									
						sums 							= client.rate*client.price*total_vessel					
						invoice_details.price  			= client.price
						usd_amt 						= client.price*total_vessel
						invoice_details.voyage_no   	= ''

				else:
					eroute		= ship_name #.split('/')
					#print '--------------eeee',ship_name				
					passage 	= eroute[2]
					#print '-------',passage				
					check_cost 	= models.cost_per_route.objects.filter(route__icontains=passage,client__client_name='Poompuhar Shipping Corporation Limited')
					for v in check_cost:																
						invoice_details.price  	= v.cost
						sums 					= v.cost*total_vessel
						usd_amt 				= v.cost*total_vessel
					invoice_details.voyage_no   = eroute[3]		

				invoice_details.proj_name 		= 'BOSS'
				invoice_details.today	 		= update_invox_date #datetime.now().date()
				invoice_details.client_id   	= x.client_id				
				invoice_details.invoice_no 		= invoice_no
				invoice_details.month       	= start_date_for	
				invoice_details.inr   			= inr
				invoice_details.usd   			= usd
				invoice_details.vessel_type 	= ship_type
				invoice_details.client_address  = client_address				
				invoice_details.total_amount 	= sums
				invoice_details.usd_amount 		= usd_amt		
				delx  							= ship_name.split('/')				
				invoice_details.rate  			= client.rate
				format_month_name 				= datetime.strptime(start_date_for, "%Y-%m-%d").strftime('%B')
				invoice_details.month_name 		= format_month_name
				invoice_details.invoice_date 	= update_invox_date
				try:		
					invoice_details.last_port 		= bill_dayx.port_name
					invoice_details.last_noon_date 	= bill_dayx.noon_date
				except:
					invoice_details.last_port 		= ''
					invoice_details.last_noon_date 	= ''
				
				try:
					invoice_details.account_type = ship_type	
				except:
					invoice_details.account_type = None

				try:
					invoice_details.voyage_no   = delx[3] #ship['Report ID']
				except:
					invoice_details.voyage_no   = ''

				try:
					invoice_details.deadwt   = delx[2] #ship['Passage']
				except:
					invoice_details.deadwt   = 0
				invoice_details.save()

				
			
		in_no 	  = update_invox_date	
		currency  = curr_types
		context={
			'invoice_date' : in_no,
			'currency' 	   : currency,
			'proj_name'    : 'BOSS',
			'msg'		   : 'done'
		}

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def generate_invoice_boss_select(request):
	selected_details = models.vessel_combined_invoice.objects.all()
	select_array 	 = []
	for x in selected_details:
		if x:
			price 		  = x.client.price
			rate  		  = x.client.rate
			amount 		  = price*rate
			bluewater     = models.BlueWater.objects.all().order_by('-id').first()
			check_address = models.Ship.objects.filter(ship_name=x.ship_name).count()
			if check_address>0:
				alert 	= ''
				color 	= ''
				disable = ''
				href 	= ''
			else:
				alert   = 'Please Fill up address of '+str(x.ship_name)
				color   = 'red'
				disable = 'disabled'
				href    = '/it/address_entry/'

			select_array.append({
				'ship_name'    : x.ship_name,
				'invoice_no'   : x.invoice_no,
				'proj_name'    : 'BOSS',
				'client_name'  : x.client.client_name,
				'invoice_date' : datetime.now().date(),
				'colors'	   : color,
				'href'  	   : href,
				'price' 	   : price,
				'rate' 		   : rate,
				'amount' 	   : amount,
				'month'		   : x.month,
				'vm_name'	   : x.vm_name,
				'voyage_no'    : x.voyage_no,
				})
	context={
	'select_array' : select_array,
	'gstin'		   : bluewater.tin_number,
	}
	return render_to_response("invoice_display/boss/generate_invoice_boss_select.html",context)

@csrf_exempt
def submit_invoice_boss_selected(request):
	description  = json.loads(request.POST['items'])
	invoice_no   = json.loads(request.POST['invoice_no'])
	invoice_date = json.loads(request.POST['invoice_date'])
	client_name  = json.loads(request.POST['client_name'])
	counter 	 = len(description)
	for x in description:
		client 			= models.Client.objects.filter(client_name=client_name).first()
		ship_details 	= models.Ship.objects.filter(client_id=client.id,ship_name=x['Vessel']).first()
		ship_name  		= x['Vessel']
		invoice_no 		= invoice_no
		check = models.invoice.objects.filter(ship_name=x['Vessel'],invoice_no=invoice_no).count()
		if check>0:
			submit_invoice = models.invoice.objects.filter(ship_name=x['Vessel'],invoice_no=invoice_no).first()
		else:
			submit_invoice = models.invoice()
		submit_invoice.ship_name  	  = ship_name
		submit_invoice.invoice_no 	  = invoice_no
		try:
			address = ship_details.address
		except:
			address = ''
		submit_invoice.client_address = address
		submit_invoice.proj_name      = 'BOSS'
		submit_invoice.month 		  =	x['Months']
		submit_invoice.counter 		  = counter
		submit_invoice.vm_name 		  = x['VM Name']
		submit_invoice.client_id      = client.id
		submit_invoice.voyage_no 	  = x['Voyage No']
		submit_invoice.save()

	return HttpResponse(json.dumps('done'))


def boss_chm_tracker(request):
	invoice_details  = models.invoice.objects.all().order_by('invoice_no')
	invoice_list     = []
	list_arr 		 = []

	for x in invoice_details:
		if x.invoice_no not in list_arr:
			list_arr.append(x.invoice_no)

	shhip_list 	 = []
	client_arr   = []
	client_list  = []

	for i in list_arr:		
		invoices  = models.invoice.objects.filter(invoice_no=i).order_by('-id').first()
		ship_name = invoices.ship_name
		counter   = models.invoice.objects.filter(invoice_no=i).count()
		chm_amt 		  = 0
		chm_sums  		  = 0
		boss_amt 		  = 0
		boss_sums 		  = 0
		label_chm 		  = ''
		label_boss 		  = ''
		single_chm_amt 	  = 0
		single_chm_sums   = 0
		single_boss_amt   = 0
		single_boss_sums  = 0
		igst_chm  		  = 0
		igst_boss 		  = 0
		total_igst_boss   = 0
		total_igst_chm    = 0
		period 			  = ''
		invoice_calc 	  = 0
		total_amount 	  = 0
		sum_boss = 0
		if counter>1:
			voyage_no = ''
			if invoices.vessel_type!='None' and invoices.vessel_type!=None and invoices.vessel_type!='Shell NWE':
				ship_name = str(invoices.vessel_type)+' Fleet'
			else:
				ship_name = ''


			# if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR':
			# 	try:
			# 		boss_amt = invoices.price*invoices.rate*invoices.qty
			# 	except:
			# 		boss_amt = 0				
			# 	label_boss = 'INR '
			# elif invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD':
			# 	boss_amt   = invoices.price*invoices.qty
			# 	label_boss = 'USD '

			if invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
				chm_amt   = invoices.price*invoices.rate*invoices.qty
				label_chm = 'INR '
			elif invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
				chm_amt   = invoices.price*invoices.qty
				label_chm = 'USD '

			#if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
			if invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
				invoice_calc = models.invoice.objects.filter(invoice_no=invoices.invoice_no)
				for x in invoice_calc:
					try:
						boss_sums+=x.qty*x.price*x.rate
					except:
						boss_sums=0
					tax_boss_amount = ((boss_sums*18/100)+boss_sums)
					try:
						chm_sums+=x.qty*x.price*x.rate
					except:
						chm_sums=0
					tax_chm_amount = ((chm_sums*18/100)+chm_sums)
			#elif invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD' or invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
			elif invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':			
				invoice_calc = models.invoice.objects.filter(invoice_no=invoices.invoice_no)
				for x in invoice_calc:
					boss_sums+=x.price*x.qty
					tax_boss_amount =boss_sums
					chm_sums+=x.qty*x.price
					tax_chm_amount = chm_sums

			# for e in xrange(1,counter+1):
			# 	if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
			# 		boss_sums+=invoices.price*invoices.rate*invoices.qty
			# 		tax_boss_amount = ((boss_sums*18/100)+boss_sums)
			# 		chm_sums+=chm_amt
			# 		tax_chm_amount = ((chm_sums*18/100)+chm_sums)
			# 	elif invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD' or invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
			# 		boss_sums+=boss_amt
			# 		tax_boss_amount =boss_sums
			# 		chm_sums+=chm_amt
			# 		tax_chm_amount = chm_sums


			if invoices.proj_name=='CHM':
				total_amount = str(label_chm)+str(round(tax_chm_amount,0))
			# elif invoices.proj_name=='BOSS':
			# 	total_amount = str(label_boss)+str(round(tax_boss_amount,0))
				#print '_________',total_amount
		else:
			if counter==1:
				# if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR':
				# 	single_boss_amt = invoices.price*invoices.rate*invoices.qty
				# 	single_label_boss = 'INR '
				# elif invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD':
				# 	single_boss_amt = invoices.price*invoices.qty
				# 	single_label_boss = 'USD '

				if invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
					single_chm_amt = invoices.price*invoices.rate*invoices.qty
					single_label_chm = 'INR '
				elif invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
					single_chm_amt = invoices.price*invoices.qty
					single_label_chm = 'USD '

				for e in xrange(1,counter+1):
					#if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
					if invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
						single_boss_sums+=single_boss_amt
						tax_single_boss = ((single_boss_sums*18/100)+single_boss_sums)
						igst_boss = (single_boss_sums*18/100)
						single_chm_sums+=single_chm_amt
						tax_single_chm = ((single_chm_sums*18/100)+single_chm_sums)
						igst_chm = (single_chm_sums*18/100)

					#elif invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD' or invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
					elif invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
						single_boss_sums+=single_boss_amt
						tax_single_boss = single_boss_sums
						single_chm_sums+=single_chm_amt
						tax_single_chm = single_chm_sums

				if invoices.proj_name=='CHM':
					total_amount   = str(single_label_chm)+str(round(tax_single_chm,0))
					total_igst_chm = igst_chm

				# elif invoices.proj_name=='BOSS':
				# 	total_amount    = str(single_label_boss)+str(round(tax_single_boss,0))
				# 	total_igst_boss = igst_boss


			voyage_no = invoices.voyage_no
			ship_name = invoices.ship_name


		#if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
		if invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
			try:
				start_date_for = (invoices.disch_date).strftime('%b')
				period = '01-'+str(start_date_for)+'-'+(invoices.disch_date).strftime('%Y')
			except:
				month_split 	= invoices.month.split(',')
				disch_date_for  = datetime.strptime(month_split[0], "%Y-%m-%d").strftime('%d-%b-%Y')
				period 			= disch_date_for

		elif invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
			try:
				start_date_for  = (invoices.disch_date).strftime('%d-%b-%Y')
				period 			= start_date_for
			except:
				month_split 	= invoices.month.split(',')
				disch_date_for  = datetime.strptime(month_split[0], "%Y-%m-%d").strftime('%d-%b-%Y')
				period 			= disch_date_for

		try:
			client_name = invoices.client.client_name
		except:
			client_name = ''

		check_payment_status = models.invoice.objects.filter(payment_status="Paid",invoice_no=i).count()

		if check_payment_status>0:
			show_button = 'none'
		else:
			show_button = ''

		if invoices.cancel_invoice==0 and invoices.payment_status=="Paid":
			#print '______Paid'
			icons  = ''
			colors = 'green'
			show_button = 'none'
		elif invoices.cancel_invoice==1 and invoices.payment_status==None:
			#print '_______Cancel'
			icons  = 'fa-times-circle fa-1x'
			colors = 'red'
			show_button = 'none'
		elif invoices.cancel_invoice==0 and invoices.payment_status==None:
			#print '________No payment'
			icons  = ''
			colors = 'black'
			show_button = ''
		else:
			#print '______Default'
			icons  = 'fa-times-circle fa-1x'
			colors = 'red'
			show_button = 'none'

		# client = invoices.client.client_name		
		# if client not in client_arr:
		# 	client_arr.append(client)

		remarks = invoices.remark

		
		try:
			min_invoice_date = models.invoice.objects.all().aggregate(Min('invoice_date'))
			mi_date   = min_invoice_date['invoice_date__min']			
			#d 		  = datetime.today() - timedelta(days=30)						
			min_date  = '04/01/2019'#d.strftime('%m/%d/%Y')	 #mi_date.strftime('%m/%d/%Y')			
			max_date  = datetime.now().date().strftime('%m/%d/%Y')	 # #max_invoice_date['invoice_date__max']	
		except:
			max_date  = ""
			min_date  = ""
			
 
		invoice_list.append({
			'ship_name' 	 : ship_name,
			'voyage_no' 	 : voyage_no,
			'invoice_date' 	 : invoices.invoice_date,
			'invoice_amount' : invoices.invoice_amount,
			'recieved_date'  : invoices.received_date,
			'client_address' : invoices.client_address,
			'payment_status' : invoices.payment_status,
			'mail_to' 		 : invoices.mail_to,
			'mail_cc' 		 : invoices.mail_cc,
			'mail_from'      : invoices.mail_from,
			'disch_date'     : invoices.disch_date,
			'disch_port' 	 : invoices.disch_port,
			'inr' 			 : invoices.inr,
			'usd' 			 : invoices.usd,
			'cancel_invoice' : invoices.cancel_invoice,
			'vm_name' 		 : invoices.vm_name,
			'invoice_no' 	 : invoices.invoice_no,
			'client_name'  	 : client_name,
			'proj_name' 	 : invoices.proj_name,
			'period' 		 : period,
			'invoice_id' 	 : invoices.invoice_no,
			'show_button'    : show_button,
			'icons_cancel'   : icons,
			'colors' 		 : colors,
			'url_pdf'		 : invoices.url,
			'client_price'   : total_amount,
			'total_igst_chm' : total_igst_chm,
			'total_igst_boss': '',#total_igst_boss,
			'remarks' 		 : remarks,
			'max_date'       : str(max_date),
			'min_date'  	 : str(min_date),
			})

	# for cl in client_arr:
	# 	client_list.append({
	# 		'client_name' : cl,
	# 		})

	context={
	'invoice_list' : invoice_list,
	#'client_list'  : client_list,
	}

	#print '=====',invoice_list

	return render_to_response("invoice_display/boss_chm_tracker.html",context)


def check_uncheck_invoice(request):
	check 		   = request.GET['check']
	invoice_num    = json.loads(request.GET['invoice_num'])[0]
	if check=='checked':
		update_details = models.invoice.objects.filter(invoice_no=invoice_num)
		for x in update_details:
			x.cancel_invoice = 1
			x.received_date  = None
			x.invoice_amount = None
			x.payment_status = None
			x.save()
	return HttpResponse(json.dumps('done'))

def submit_dsr_invoice(request):
	if request.user.is_authenticated():
		merge 				= request.GET['merge']
		proj_name 			= request.GET['proj_name']
		vessel_type 		= json.loads(request.GET['vessel_type'])
		update_invoice_date = json.loads(request.GET['update_invoice_date'])
		invoice_details     = models.vessel_selected_invoice.objects.all().order_by('-id')
		currency_type 		= invoice_details[0].client.currency_type
		voy_array 			= []
		check_vessel        = models.vessel_selected_invoice.objects.all().count()
		#total_vessel	 	= json.loads(request.POST['tbodyRowCount'])
		
		# if total_vessel!=0:
		#total_vessel = total_vessel
		# else:
		# 	total_vessel = tbodyRowCount 

		if merge=='1':
			print '-======== hehehe main yaha hu'
			#voy ={}
			for i in invoice_details:
				# if len(i.ship_name)>1:
				# 	voy_array.append(i.voyage_no)
				# 	voyage_number = voy_array
				# else:
				# 	voyage_number = i.voyage_no

				format_disch_date = i.disch_date.strftime("%d-%b-%Y")
				#ship_list 	 = models.Ship.objects.filter(ship_name=i.ship_name).exclude(address=None).first()
				pool_details = models.pool_master.objects.filter(client_id=i.client_id,pool=i.account_type).first()
				client_name  = pool_details.client.client_name #ship_list.client.client_name
				client_price = pool_details.client.price #ship_list.client.price
				price_type   = pool_details.client.price_type #ship_list.client.price_type
				price_rate   = pool_details.client.rate #ship_list.client.rate
				try:
					client_addre = pool_details.address #ship_list.address==== 2021-07-15 # i.address
				except:
					client_addre = pool_details.addres
				#voy 	     = voyage_number
				#voyage_no    = ', '.join(sorted(voy))

				disch_date_for 	= datetime.strptime(format_disch_date, "%d-%b-%Y").strftime('%Y-%m-%d')
				check 			= models.invoice.objects.filter(ship_name=i.ship_name,voyage_no=i.voyage_no,payment_status=None).count()
				if check>0:
					return HttpResponse(json.dumps('error'))
				else:
					submit_invoice = models.invoice()

				client_del = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()
				if client_del.client_name=='stena bulk':
					if check_vessel>=1 and check_vessel<=2:
						prices  = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='stena bulk').first()
						i_price = prices.price #_1600_____1-2'
						price_typess = '1-2'
					elif check_vessel>=3 and check_vessel<=5:
						prices  = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='stena bulk').first()
						i_price =  prices.price # 1400 #______3-5'
						price_typess = '3-5'				
					elif check_vessel>=6 and check_vessel<=8:
						prices  = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
						i_price = prices.price # 1200#_______6-8'
						price_typess = '6-8'				
					elif check_vessel>=8:
						prices  = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
						i_price = prices.price # 1200
						price_typess = '6-8'

				elif client_del.client_name=='Stena Bulk Veg Oil':
					if check_vessel>=1 and check_vessel<=2:
						pricess = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
						i_price = pricess.price # 1700 #______1-2'
						price_typess = '1-2'
					elif check_vessel>=3 and check_vessel<=5:
						pricess = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
						i_price = pricess.price # 1500 # _____3-5'
						price_typess = '3-5'
					elif check_vessel>=6 and check_vessel<=8:
						pricess = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
						i_price = pricess.price # 1300# ______6-8'
						price_typess = '6-8'
					elif check_vessel>=8:
						pricess = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
						i_price = pricess.price  #1300
						price_typess = '6-8'

				elif client_del.client_name=='Ultranav':			
					if check_vessel>=1 and check_vessel<=4:
						pricess = models.Client.objects.filter(price_type='1-4',proj_name='CHM',client_name='Ultranav').first()
						i_price = pricess.price # 1700 #______1-2'
						price_typess = '1-4'
					elif check_vessel>=5 and check_vessel<=9:
						pricess = models.Client.objects.filter(price_type='5-9',proj_name='CHM',client_name='Ultranav').first()
						i_price = pricess.price # 1500 # _____3-5'
						price_typess = '5-9'
					elif check_vessel>=10:
						pricess = models.Client.objects.filter(price_type='ShortHaul',proj_name='CHM',client_name='Ultranav').first()
						i_price = pricess.price # 1300# ______6-8'
						price_typess = 'ShortHaul'

				elif client_del.client_name=='Litasco':			
					if check_vessel>=1 and check_vessel<=5:
						#print '-----------------',check_vessel
						pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco').first()
						i_price = pricess.price # 1700 #______1-2'
						price_typess = '1-5'
					elif check_vessel>=6 and check_vessel<=10:
						pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco').first()
						i_price = pricess.price # 1500 # _____3-5'
						price_typess = '6-10'
					elif check_vessel>=11:
						pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco').first()
						i_price = pricess.price # 1300# ______6-8'
						price_typess = '11 and Up'

				elif client_del.client_name=='Litasco_Dubai':			
					if check_vessel>=1 and check_vessel<=5:
						#print '-----------------',check_vessel
						pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco_Dubai').first()
						i_price = pricess.price # 1700 #______1-2'
						price_typess = '1-5'
					elif check_vessel>=6 and check_vessel<=10:
						pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco_Dubai').first()
						i_price = pricess.price # 1500 # _____3-5'
						price_typess = '6-10'
					elif check_vessel>=11:
						pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco_Dubai').first()
						i_price = pricess.price # 1300# ______6-8'
						price_typess = '11 and Up'
					
				else:
					i_price = i.client.price

				submit_invoice.ship_name 		= i.ship_name.strip()
				submit_invoice.voyage_no 		= voyage_no
				submit_invoice.invoice_date 	= update_invoice_date #datetime.now().date()
				submit_invoice.vm_name 			= i.vm_name
				submit_invoice.disch_date 		= str(disch_date_for)
				submit_invoice.disch_port 		= i.disch_port
				submit_invoice.client_id 		= i.client_id
				submit_invoice.client_address 	= client_addre
				submit_invoice.invoice_no 		= i.invoice_no
				submit_invoice.price 			= i_price #i.client.price
				submit_invoice.voyage_id 		= i.voyage_cancel


				try:
					submit_invoice.price_type 	= price_typess
				except:
					submit_invoice.price_type 	= None

				try:
					submit_invoice.vessel_type 	= vessel_type
				except:
					submit_invoice.vessel_type 	= None

				try:
					if i.client.currency_type=='INR' and i.client.proj_name=='CHM':
						inr = 'INR'
						usd = None
					elif i.client.currency_type=='USD' and i.client.proj_name=='CHM':
						inr = None
						usd = 'USD'
				except:
					inr = None
					usd = None

				if i.client.currency_type=='INR':
					submit_invoice.rate 		= i.client.rate
				elif i.client.currency_type=='USD':
					submit_invoice.rate 		= 1

				submit_invoice.proj_name 		= 'CHM'
				submit_invoice.inr 				= inr
				submit_invoice.usd 				= usd
				submit_invoice.month     		= datetime.now().date()
				submit_invoice.qty 				= i.qty
				#submit_invoice.account_type     = account_type
				submit_invoice.nomination_date  = i.nomination_date
				date_for_nominate 				= datetime.strptime(str(i.nomination_date), "%Y-%m-%d").strftime('%d %b %Y')
				#print '-------11',i.book_names
				if i.book_names!=None and i.book_names!='':
					submit_invoice.remark 		= str(i.book_names)+" / Enrolment Date: "+str(date_for_nominate)	
				else:
					submit_invoice.remark  		= "Enrolment Date: "+str(date_for_nominate)					
				submit_invoice.save()

		else:
			print '=======kaha chala gaya tu'
			for t in invoice_details:
				format_disch_date = t.disch_date.strftime("%d-%b-%Y")
				if t.client.client_name!='Shell':
					#ship_list 	 = models.Ship.objects.filter(ship_name=t.ship_name).first()
					pool_details = models.pool_master.objects.filter(client_id=t.client_id,pool=t.account_type).first()
				else:
					pool_details = models.pool_master.objects.filter(client_id=t.client_id,pool=t.account_type).first()
				try:
					client_name  	= pool_details.client.client_name #ship_list.client.client_name
					client_price 	= pool_details.client.price #ship_list.client.price
					price_type   	= pool_details.client.price_type #ship_list.client.price_type
					price_rate   	= pool_details.client.rate #ship_list.client.rate
					try:
						client_adre = pool_details.address #ship_list.address----- 2021-07-15
					except:
						client_adre = pool_details.address


					account_type 	= t.account_type
					disch_date_for 	= datetime.strptime(format_disch_date, "%d-%b-%Y").strftime('%Y-%m-%d')
					#voy 	   		= voyage_number
					#voyage_no 		= ', '.join(sorted(voy))
					check = models.invoice.objects.filter(ship_name=t.ship_name,voyage_no=t.voyage_no,payment_status=None).count()
					if check>0:
						return HttpResponse(json.dumps('error'))
					else:
						submit_invoice = models.invoice()

					client_del = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()
					try:
						if t.client.currency_type=='INR' and t.client.proj_name=='CHM':
							inr = 'INR'
							usd = None
						elif t.client.currency_type=='USD' and t.client.proj_name=='CHM':
							inr = None
							usd = 'USD'
					except:
						inr = None
						usd = None
					# if client_del.client_name=='stena bulk':
					# 	if check_vessel>=1 and check_vessel<=2:
					# 		t_price = 1600 # ______1-2'
					# 	elif check_vessel>=3 and check_vessel<=5:
					# 		t_price = 1400 #_______3-5'
					# 	elif check_vessel>=6 and check_vessel<=8:
					# 		t_price = 1200#'_______6-8'
					# 	elif check_vessel>=8:
					# 		t_price = 1200
					# elif client_del.client_name=='Stena Weco':
					# 	if check_vessel>=1 and check_vessel<=2:
					# 		t_price = 1700 # ______1-2'
					# 	elif check_vessel>=3 and check_vessel<=5:
					# 		t_price = 1500 #_______3-5'
					# 	elif check_vessel>=6 and check_vessel<=8:
					# 		t_price = 1300#'_______6-8'
					# 	elif check_vessel>=8:
					# 		t_price = 1300
					if client_del.client_name=='stena bulk':
						if check_vessel>=1 and check_vessel<=2:
							prices  	 = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='stena bulk').first()
							t_price 	 = prices.price #_1600_____1-2'
							price_typess = '1-2'
						elif check_vessel>=3 and check_vessel<=5:
							prices  	 = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='stena bulk').first()
							t_price 	 = prices.price # 1400 #______3-5'
							price_typess = '3-5'
						elif check_vessel>=6 and check_vessel<=8:
							prices   	 = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
							t_price  	 = prices.price # 1200#_______6-8'
							price_typess = '6-8'
						elif check_vessel>=8:
							prices  	 = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
							t_price 	 = prices.price  #1200
							price_typess = '6-8'
					elif client_del.client_name=='Stena Bulk Veg Oil':
						if check_vessel>=1 and check_vessel<=2:
							pricess 	 = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
							t_price 	 = pricess.price # 1700 #______1-2'
							price_typess = '1-2'
						elif check_vessel>=3 and check_vessel<=5:
							pricess 	 = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
							t_price 	 = pricess.price # 1500 # _____3-5'
							price_typess = '3-5'
						elif check_vessel>=6 and check_vessel<=8:
							pricess 	 = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
							t_price 	 = pricess.price # 1300# ______6-8'
							price_typess = '6-8'
						elif check_vessel>=8:
							pricess 	 = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
							t_price 	 = pricess.price  #1300
							price_typess = '6-8'
					elif client_del.client_name=='Ultranav':
						if check_vessel>=1 and check_vessel<=4:
							pricess 	 = models.Client.objects.filter(price_type='1-4',proj_name='CHM',client_name='Ultranav').first()
							t_price 	 = pricess.price # 1700 #______1-2'
							price_typess = '1-4'
						elif check_vessel>=5 and check_vessel<=9:
							pricess 	 = models.Client.objects.filter(price_type='5-9',proj_name='CHM',client_name='Ultranav').first()
							t_price 	 = pricess.price # 1500 # _____3-5'
							price_typess = '5-9'
						elif check_vessel>=10:
							pricess 	 = models.Client.objects.filter(price_type='ShortHaul',proj_name='CHM',client_name='Ultranav').first()
							t_price 	 = pricess.price # 1300# ______6-8'
							price_typess = 'ShortHaul'

					elif client_del.client_name=='Litasco':			
						if check_vessel>=1 and check_vessel<=5:						
							pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco').first()
							t_price = pricess.price # 1700 #______1-2'
							price_typess = '1-5'
						elif check_vessel>=6 and check_vessel<=10:
							pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco').first()
							t_price = pricess.price # 1500 # _____3-5'
							price_typess = '6-10'
						elif check_vessel>=11:
							pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco').first()
							t_price = pricess.price # 1300# ______6-8'
							price_typess = '11 and Up'

					elif client_del.client_name=='Litasco_Dubai':			
						if check_vessel>=1 and check_vessel<=5:						
							pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco_Dubai').first()
							t_price = pricess.price # 1700 #______1-2'
							price_typess = '1-5'
						elif check_vessel>=6 and check_vessel<=10:
							pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco_Dubai').first()
							t_price = pricess.price # 1500 # _____3-5'
							price_typess = '6-10'
						elif check_vessel>=11:
							pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco_Dubai').first()
							t_price = pricess.price # 1300# ______6-8'
							price_typess = '11 and Up'
					else:
						t_price = t.client.price



					submit_invoice.ship_name 		= t.ship_name
					submit_invoice.voyage_no 		= t.voyage_no
					submit_invoice.invoice_date 	= update_invoice_date #datetime.now().date()
					submit_invoice.vm_name 			= t.vm_name
					submit_invoice.disch_date 		= str(disch_date_for)
					submit_invoice.disch_port 		= t.disch_port
					submit_invoice.client_id 		= t.client_id
					submit_invoice.client_address 	= client_adre
					submit_invoice.invoice_no 		= t.invoice_no
					submit_invoice.price 			= t_price
					submit_invoice.inr 				= inr
					submit_invoice.usd 				= usd
					submit_invoice.account_type     = account_type
					submit_invoice.qty 				= t.qty
					submit_invoice.voyage_id 		= t.voyage_cancel
					try:
						submit_invoice.price_type 	= price_typess
					except:
						submit_invoice.price_type   = 5
					try:
						submit_invoice.vessel_type 	= vessel_type
					except:
						submit_invoice.vessel_type 	= 6

					if t.client.currency_type=='INR':
						submit_invoice.rate 		= t.client.rate
					elif t.client.currency_type=='USD':
						submit_invoice.rate 		= 1

					submit_invoice.proj_name 		= 'CHM'
					submit_invoice.month     		= datetime.now().date()
					submit_invoice.nomination_date  = t.nomination_date					#try:
					date_for_nominate 				= datetime.strptime(str(t.nomination_date), "%Y-%m-%d").strftime('%d %b %Y')

					#submit_invoice.remark 			= "Enrolment Date: "+str(date_for_nominate)
					#print '------------',"Nomination Date: "+str(date_for_nominate)
					#print '-------222',t.book_names
					if t.book_names!=None and t.book_names!='':
						submit_invoice.remark 		= str(t.book_names)+" / Enrolment Date: "+str(date_for_nominate)	
					else:
						submit_invoice.remark  		= "Enrolment Date: "+str(date_for_nominate)
					
					submit_invoice.save()
					
				except:
					return HttpResponse(json.dumps('no_address'))
		
		in_no 	  = update_invoice_date
		proj_name = proj_name
		currency  = currency_type
		context = {
		'invoice_date' : in_no,
		'currency' 	   : currency,
		'proj_name'    : 'CHM',
		}

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')


def generate_invoice_pdf(request):
	if request.user.is_authenticated():	
		from calendar import monthrange
		import calendar		
		calling_pdf    = models.vessel_combined_invoice.objects.all()
		client         = ''
		sums           = 0
		split_address1 = ''
		split_address2 = ''
		split_address3 = ''
		split_address4 = ''
		split_address5 = ''
		account_type   = ''
		p = 0
		fontsize = '12'
		addline  = '3'
		for x in calling_pdf:
			if x.client.proj_name=='BOSS':			
				ship_det = models.Ship.objects.filter(client_id=x.client_id).exclude(address='').first()
			elif x.client.proj_name=='CHM':
				ship_det = models.pool_master.objects.filter(client__client_name='Shell').first()
			else:
				ship_det = models.pool_master.objects.filter(client__client_name=x.client.client_name).first()
			
				
			client 		 = x.client.client_name
			invoice 	 = x.invoice_no
			invoicedate  = x.today
			month        = x.month
			vm_name      = x.vm_name
			currency     = x.client.currency_type
			if x.client.proj_name=='BOSS' and  x.client.currency_type=='INR' or x.client.proj_name=='CHM' and  x.client.currency_type=='INR':
				amount = x.client.price*x.client.rate
			elif x.client.proj_name=='BOSS' and  x.client.currency_type=='USD' or x.client.proj_name=='CHM' and  x.client.currency_type=='USD':
				amount = x.client.price
			sums+=amount
			
			try:
				customer_no  = x.client.tin_number
			except:
				customer_no = ''

			if x.client.proj_name:
				p+=1	

		try:
			clientaddress  = ship_det.address.split(',')
			split_address1 = clientaddress[0]
			split_address2 = clientaddress[1]
			split_address3 = clientaddress[2]
			split_address4 = clientaddress[3]
			split_address5 = clientaddress[4]

		except:
			split_address1 = split_address1
			split_address2 = split_address2
			split_address3 = split_address3
			split_address4 = split_address4
			split_address5 = split_address5

		client_name 		= client
		invoice_no  		= invoice
		total_amount 		= sums
		format_invoice_date = invoicedate.strftime("%d-%b-%Y")
		format_year 		= datetime.strptime(month, "%Y-%m-%d").strftime('%Y')
		format_month 		= datetime.strptime(month, "%Y-%m-%d").strftime('%b')
		int_month 			= datetime.strptime(month, "%Y-%m-%d").strftime('%m')
		get_month 			= monthrange(int(format_year),int(int_month))[1]
		
		#print '========'		
		if client_name=='Poompuhar Shipping Corporation Limited' or client_name=='TNPGCL':	
			arr = get_create_pdf_client_name(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,'BOSS','0','0',currency,total_amount,0,0,split_address3,split_address4,split_address5,fontsize,addline,0,0,0)	
			#apj.get_calling_for_excel(client_name,calling_pdf,0,0,0)
		#elif client_name=='Clearlake':		
		#	ct.get_calling_for_excel(client_name,calling_pdf,0,0,0)
		#elif client_name=='Oldendorff':
		#	otp.get_calling_for_excel_otp(client_name,calling_pdf,0,0,0)
		# elif client_name=='Ultranav':
		# 	dt.get_calling_for_excel_default(client_name,calling_pdf,0,0,0)
		
		#elif client=='Shell' or client_name=='Shell NWE':
			#if p<20:	
			#print ''	
				#phele get_create_pdf_client_name tha	
			#arr = get_create_pdf(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,'BOSS','0','0',currency,total_amount,0,0,split_address3,split_address4,split_address5)
			# elif p>20:
			# 	print '======Print in excel'
			# 	sh.get_calling_for_excel(client_name,calling_pdf,0,0,0)
		else:
			#print '=============',split_address4
			arr = get_create_pdf(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,'BOSS','0','0',currency,total_amount,0,0,split_address3,split_address4,split_address5,fontsize,addline,0,0,0,0)
			
		remove_splash_invoice_no = invoice_no.replace('/', '_')
		#extension_in_html 		 = remove_splash_invoice_no+'_'+client_name+".html"
		#extension_in_pdf  		 = remove_splash_invoice_no+'_'+client_name+".pdf"

		#try:
		extension_in_html 	 = remove_splash_invoice_no+'_'+client_name+'_'+x.vessel_type+".html"
		extension_in_pdf  	 = remove_splash_invoice_no+'_'+client_name+'_'+x.vessel_type+".pdf"
		#print '----------',extension_in_pdf
		# except:
		# 	extension_in_html 	 = remove_splash_invoice_no+'_'+client_name+'_'+x.client.currency_type+".html"
		# 	extension_in_pdf  	 = remove_splash_invoice_no+'_'+client_name+'_'+x.client.currency_type+".pdf"

		url_path  = "/static/pdf/"+client_name+"/"+extension_in_pdf

		context = {
		'url_path' : url_path
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')


def single_generate_invoice_pdf(request):
	from calendar import monthrange
	import calendar
	split_address1 = ''
	split_address2 = ''
	split_address3 = ''
	split_address4 = ''
	split_address5 = ''
	calling_pdf    = models.vessel_selected_invoice.objects.all()
	for x in calling_pdf:

		ship_det = models.Ship.objects.filter(client_id=x.client_id).first()
		client 		 = x.client.client_name
		invoice 	 = x.invoice_no
		invoice_date = x.today
		month        = x.month
		vm_name      = x.vm_name
		currency     = x.client.currency_type
		try:
			customer_no  = x.tin_number
		except:
			customer_no = ''
	#try:
	# 	client_address = ship_det.address.split(',')
	# 	split_address1 = client_address[0]
	# 	split_address2 = client_address[1]
	# 	split_address3 = client_address[2]
	# 	split_address4 = client_address[3]
	# 	split_address5 = client_address[4]
	# 	header  = split_address1
	# 	address = split_address2
	# 	address1 = split_address3
	# 	address2 = split_address4
	# 	address3 = split_address5
	# except:
	# 	header  = ''
	# 	address = ''
	# 	address1 = ''
	# 	address2 = ''
	# 	address3 = ''
	try:
		clientaddress  = ship_det.address.split(',')
		split_address1 = clientaddress[0]
		split_address2 = clientaddress[1]
		split_address3 = clientaddress[2]
		split_address4 = clientaddress[3]
		split_address5 = clientaddress[4]
		split_address6 = clientaddress[5]

	except:
		split_address1 = split_address1
		split_address2 = split_address2
		split_address3 = split_address3
		split_address4 = split_address4
		split_address5 = split_address5
		split_address6 = split_address6

	client_name 		= client
	invoice_no  		= invoice
	format_invoice_date = invoice_date.strftime("%d-%b-%Y")
	format_year 		= datetime.strptime(month, "%Y-%m-%d").strftime('%Y')
	format_month 		= datetime.strptime(month, "%Y-%m-%d").strftime('%b')
	int_month 			= datetime.strptime(month, "%Y-%m-%d").strftime('%m')
	get_month 			= monthrange(int(format_year),int(int_month))[1]
	if client_name=='Shell' or client_name=='Shell NWE':
		# phele get_create_pdf_client_name tha
		arr = get_create_pdf(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,'BOSS','0','0',currency,0,0,0,split_address3,split_address4,split_address5,split_address6,0,0,0,0,0)
	else:
		arr = get_create_pdf(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,'BOSS','0','0',currency,0,0,0,split_address3,split_address4,split_address5,split_address6,0,0,0,0,0)
	remove_splash_invoice_no = invoice_no.replace('/', '_')
	extension_in_html = remove_splash_invoice_no+'_'+client_name+".html"
	extension_in_pdf  = remove_splash_invoice_no+'_'+client_name+".pdf"

	url_path   = "/static/pdf/"+client_name+"/"+extension_in_pdf
	context = {
	'url_path' : url_path
	}

	return HttpResponse(json.dumps(context))

def chm_generate_invoice_pdf(request):
	from calendar import monthrange
	import calendar
	merge = request.GET['merge']
	calling_pdf    = models.vessel_selected_invoice.objects.all()
	check_vessel   = models.vessel_selected_invoice.objects.all().count()
	total_amt      = 0
	split_address1 = ''
	split_address2 = ''
	split_address3 = ''
	split_address4 = ''
	split_address5 = ''

	ch_array = []
	
	for x in calling_pdf:
		client_del = models.Client.objects.filter(id=x.client_id,proj_name='CHM').first()
		#ship_det  = models.Ship.objects.filter(client_id=x.client_id).exclude(address='').first()
		#if x.client.client_name!='Shell':
		ship_det = models.pool_master.objects.filter(client_id=x.client_id,pool=x.account_type,client__proj_name='CHM').first()
		
		#else:
			#ship_det = models.pool_master.objects.filter(client__client_name='Shell',pool=x.account_type).first()
			# client__client_name='Shell',pool=x.account_type,proj_name='CHM'
		client 		 = x.client.client_name
		invoice 	 = x.invoice_no
		invoice_date = x.today
		month        = x.month
		vm_name      = x.vm_name
		currency     = x.client.currency_type
		disch_port   = x.disch_port

		#print '---------',client_del.client_name
		
		if client_del.client_name=='stena bulk':
			if check_vessel>=1 and check_vessel<=2:
				prices  = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='stena bulk').first()
				t_price = prices.price #_1600_____1-2'
			elif check_vessel>=3 and check_vessel<=5:
				prices  = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='stena bulk').first()
				t_price = prices.price # 1400 #______3-5'
			elif check_vessel>=6 and check_vessel<=8:
				prices  = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
				t_price = prices.price # 1200#_______6-8'
			elif check_vessel>=8:
				prices  = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='stena bulk').first()
				t_price = prices.price  #1200
		elif client_del.client_name=='Stena Bulk Veg Oil':
			if check_vessel>=1 and check_vessel<=2:
				pricess = models.Client.objects.filter(price_type='1-2',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
				t_price = pricess.price # 1700 #______1-2'
			elif check_vessel>=3 and check_vessel<=5:
				pricess = models.Client.objects.filter(price_type='3-5',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
				t_price = pricess.price # 1500 # _____3-5'
			elif check_vessel>=6 and check_vessel<=8:
				pricess = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
				t_price = pricess.price # 1300# ______6-8'
			elif check_vessel>=8:
				pricess = models.Client.objects.filter(price_type='6-8',proj_name='CHM',client_name='Stena Bulk Veg Oil').first()
				t_price = pricess.price  #1300
		elif client_del.client_name=='Litasco':
			if check_vessel>=1 and check_vessel<=5:
				#print '-----------------',check_vessel
				pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco').first()
				t_price = pricess.price # 1700 #______1-2'
				#price_typess = '1-5'
			elif check_vessel>=6 and check_vessel<=10:
				pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco').first()
				t_price = pricess.price # 1500 # _____3-5'
				#price_typess = '6-10'
			elif check_vessel>=11:
				pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco').first()
				t_price = pricess.price # 1300# ______6-8'
				#price_typess = '11 and Up'

		elif client_del.client_name=='Litasco_Dubai':
			if check_vessel>=1 and check_vessel<=5:
				#print '-----------------',check_vessel
				pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco_Dubai').first()
				t_price = pricess.price # 1700 #______1-2'
				price_typess = '1-5'
				#print '-------',price_typess
			elif check_vessel>=6 and check_vessel<=10:
				pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco_Dubai').first()
				t_price = pricess.price # 1500 # _____3-5'
				price_typess = '6-10'
			elif check_vessel>=11:
				pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco_Dubai').first()
				t_price = pricess.price # 1300# ______6-8'
				price_typess = '11 and Up'
		else:
			t_price = x.client.price

		client_price = t_price
		rate 		 = x.client.rate

		if merge=="0":
			if x.client.proj_name=='BOSS' and x.client.currency_type=='INR' or x.client.proj_name=='CHM' and x.client.currency_type=='INR':
				amount = x.client.price*rate
				total_amt=amount

			if x.client.proj_name=='BOSS' and x.client.currency_type=='USD' or x.client.proj_name=='CHM' and x.client.currency_type=='USD':
				amount = t_price#x.client.price
				total_amt=amount

		elif merge=="1":
			if x.client.proj_name=='BOSS' and x.client.currency_type=='INR' or x.client.proj_name=='CHM' and x.client.currency_type=='INR':
				amount = x.client.price*rate
				total_amt=amount

			if x.client.proj_name=='BOSS' and x.client.currency_type=='USD' or x.client.proj_name=='CHM' and x.client.currency_type=='USD':
				amount = t_price#x.client.price
				total_amt=amount
		try:
			customer_no  = x.tin_number
		except:
			customer_no = ''
	
		try:			
			clientaddress  = x.address.split(',')
			split_address1 = clientaddress[0]
			split_address2 = clientaddress[1]
			split_address3 = clientaddress[2]
			split_address4 = clientaddress[3]
			split_address5 = clientaddress[4]
		except:
			split_address1 = split_address1
			split_address2 = split_address2
			split_address3 = split_address3
			split_address4 = split_address4
			split_address5 = split_address5

	client_name 		= client
	invoice_no  		= invoice
	format_invoice_date = invoice_date.strftime("%d-%b-%Y")
	format_year 		= datetime.strptime(month, "%Y-%m-%d").strftime('%Y')
	format_month 		= datetime.strptime(month, "%Y-%m-%d").strftime('%b')
	int_month 			= datetime.strptime(month, "%Y-%m-%d").strftime('%m')
	get_month 			= monthrange(int(format_year),int(int_month))[1]

	if x.client.proj_name=='BOSS' and x.client.currency_type=='INR' or x.client.proj_name=='CHM' and x.client.currency_type=='INR':
		total_amount = total_amt
	if x.client.proj_name=='BOSS' and x.client.currency_type=='USD' or x.client.proj_name=='CHM' and x.client.currency_type=='USD':
		total_amount = total_amt

	#print '==========.............',split_address1,'---',split_address2,'---',split_address3,'---',split_address4,'----',split_address5
	if client_name=='Shell' or client_name=='Shell NWE':
		#phele get_create_pdf_client_name tha
		arr = get_create_pdf(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,'CHM',merge,'0',currency,total_amount,0,0,split_address3,split_address4,split_address5,'12px',5,0,0,0,0,0)
		#vt.get_calling_for_vessel_template(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,merge,currency,total_amount,split_address3,split_address4,split_address5,check_vessel)
		#print '====1',arr,'====1',vt
	else:
		arr = get_create_pdf(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,'CHM',merge,'0',currency,total_amount,0,0,split_address3,split_address4,split_address5,'12px',5,0,0,0,0,0)
		#vt.get_calling_for_vessel_template(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,merge,currency,total_amount,split_address3,split_address4,split_address5,check_vessel)
		#print '====2',arr

	remove_splash_invoice_no = invoice_no.replace('/', '_')
	extension_in_html 		 = remove_splash_invoice_no+'_'+client_name+".html"
	extension_in_pdf  		 = remove_splash_invoice_no+'_'+client_name+".pdf"
	url_path 				 = "/static/pdf/"+client_name+"/"+extension_in_pdf
	
	context  = {
	'url_path' : url_path,	
	'invoice_no' : invoice_no
	}	
	return HttpResponse(json.dumps(context))


def payment_list(request):
	total_amount = 0
	display_for_disch_port = ''
	tag_logo = ''
	invoice_no 	   	= request.GET['invoice_no']
	proj_name 		= request.GET['proj_name']
	clientID 		= request.GET['clientID']
	invoice_details = models.invoice.objects.filter(invoice_no=invoice_no,client_id=clientID,proj_name=proj_name,cancel_invoice='0')
	counter 	   	= models.invoice.objects.filter(invoice_no=invoice_no,client_id=clientID,proj_name=proj_name).count()
	ct_qty          = models.invoice.objects.filter(invoice_no=invoice_no,client_id=clientID,proj_name=proj_name,cancel_invoice='0').aggregate(Sum('qty'))
	sum_qty 		= ct_qty['qty__sum']
	array 		   	= []
	sum_total 		= 0	

	pm=0
	for x in invoice_details:		
		try:
			if (x.client.currency_type=='INR' and x.client.proj_name=='BOSS') or (x.client.currency_type=='INR' and x.client.proj_name=='CHM'):
				tag_logo = 'INR'
			elif (x.client.currency_type=='USD' and x.client.proj_name=='BOSS') or (x.client.currency_type=='USD' and x.client.proj_name=='CHM'):
				tag_logo = 'USD'

			
			currency_type = x.client.currency_type
			client_price  = x.price
			client_rate   = x.rate
			client_qty    = x.qty
			price_type    = x.price_type
			client_id     = x.client.id
			proj_name 	  = x.proj_name
			tds	 		  = x.tds
			poom_price    = x.price			

			if tds==None:
				invoice_tds = 0.0
			else:
				invoice_tds = tds

			if proj_name=='BOSS':
				display_for_disch_port ='none'
			elif proj_name=='CHM':
				display_for_disch_port =''

			if counter>1:
				fleet = str(x.vessel_type)+' Fleet'
			else:
				fleet = x.voyage_no
		except:
			client_price = 0
			client_rate  = 0
			price_type   = 0
			client_id    = 0
			fleet        = ''

		if x.payment_status=='Paid' and x.cancel_invoice==1:
			button = 'Unpaid'
		elif x.cancel_invoice==1 and x.payment_status==None:
			button = 'Paid'
		elif x.payment_status==None and x.cancel_invoice==0:
			button = 'Submit'
		elif x.payment_status=="Paid" and x.cancel_invoice==0:
			button = 'Unpaid'
		else:
			button = 'Submit'

		try:
			get_image 	= models.image_uploader.objects.filter(invoice_no=invoice_no).first()
			split_img 	= str(get_image.image_file).split('/')
			first_img 	= '/'+str(split_img[6])+'/'+str(split_img[7])+'/'+str(get_image.file_name)
			image_link 	= first_img			
		except:
			image_link	= ''	




		array.append({
			'ship_name' 	: x.ship_name,
			'voyage_no' 	: x.voyage_no,
			'client_price' 	: client_price,
			'client_rate' 	: client_rate,
			'price_type' 	: price_type,
			'invoice_no'    : x.invoice_no,
			'vm_name'		: x.vm_name,
			'disch_port'    : x.disch_port,
			'client_id'     : client_id,
			'fleet'         : fleet,
			'button'		: button,
			'invoice_tds'   : invoice_tds,
			'proj_name'     : proj_name,
			'invoiceID'		: x.id,			
			})


		if proj_name=='BOSS' and currency_type=='INR' or proj_name=='CHM' and currency_type=='INR':
			if clientID!='125': # for poompuhar
				without_tax  = (client_price*client_rate*counter)
			else:
				hout_tax  = (poom_price*client_rate)				
				pm+=hout_tax
				without_tax = x.total_amount #pm				
			
			net_tax = (without_tax*18)/100
			sum_total+=(without_tax+net_tax)
			total_amount = x.total_amount			


		elif proj_name=='BOSS' and currency_type=='USD' or proj_name=='CHM' and currency_type=='USD':
			
			if clientID=='112':
				without_tax = x.usd_amount
			else:
				without_tax  = (client_price*client_qty*counter)
			
			net_tax 	 = (without_tax)
			sum_total+=net_tax
			total_amount = (sum_total)

	context={
	'array' 				 : array,
	'total_amount' 			 : total_amount,
	'display_for_disch_port' : display_for_disch_port,
	'tag_logo' 				 : tag_logo,
	'without_tax' 			 : without_tax,
	'image_link'			 : image_link,
	'user_name'				 : str(request.user),	
	}
	return HttpResponse(json.dumps(context))

def master_log_tracker(request):
	invoice_details = models.invoice.objects.filter(invoice_date=None,payment_status='Paid')
	invoice_list    = []
	list_arr 		= []
	for x in invoice_details:
		if x.invoice_no not in list_arr:
			list_arr.append(x.invoice_no)

	shhip_list 	  = []
	for i in list_arr:
		invoices  = models.invoice.objects.filter(invoice_no=i).order_by('-id').first()
		ship_name = invoices.ship_name

		try:
			start_date_for = (invoices.disch_date).strftime('%b')
			period = '01-'+str(start_date_for)+'-'+(invoices.disch_date).strftime('%Y')
		except:
			month_split 	= invoices.month.split(',')
			disch_date_for  = datetime.strptime(month_split[0], "%Y-%m-%d").strftime('%d-%b-%Y')
			period 			= disch_date_for

		try:
			client_name = invoices.client.client_name
		except:
			client_name = ''

		check_payment_status = models.invoice.objects.filter(payment_status="Paid",invoice_no=i).count()
		if check_payment_status>0:
			show_button = ''
		else:
			show_button = ''

		if invoices.cancel_invoice==0:
			icons  = ''
			colors = ''
		else:
			icons  = 'fa-times-circle fa-1x'
			colors = 'red'


		invoice_list.append({
			'ship_name' 	 : invoices.ship_name,
			'voyage_no' 	 : invoices.voyage_no,
			'invoice_date' 	 : invoices.invoice_date,
			'invoice_amount' : invoices.invoice_amount,
			'recieved_date'  : invoices.received_date,
			'client_address' : invoices.client_address,
			'payment_status' : invoices.payment_status,
			'mail_to' 		 : invoices.mail_to,
			'mail_cc' 		 : invoices.mail_cc,
			'mail_from'      : invoices.mail_from,
			'disch_date'     : invoices.disch_date,
			'disch_port' 	 : invoices.disch_port,
			'inr' 			 : invoices.inr,
			'usd' 			 : invoices.usd,
			'cancel_invoice' : invoices.cancel_invoice,
			'vm_name' 		 : invoices.vm_name,
			'invoice_no' 	 : invoices.invoice_no,
			'client_name'  	 : client_name,
			'proj_name' 	 : invoices.proj_name,
			'period' 		 : period,
			'invoice_id' 	 : invoices.invoice_no,
			'show_button'    : show_button,
			# 'icons_cancel'   : icons,
			# 'colors' 		 : colors,
			'url_pdf'		 : invoices.url,
			})
	context={
	'invoice_list' : invoice_list
	}
	return render_to_response("invoice_display/master_log_tracker.html",context)

def paid_invoice_list(request):
	invoice_no   	= request.GET['invoice_no']
	invoice_cancel  = request.GET['invoice_cancel']
	invoice_amount  = request.GET['invoice_amount']
	remark 			= request.GET['payment_status']
	rec_date 		= request.GET['rec_date']
	checkbutton		= request.GET['submit_id']
	received_inr    = request.GET['e_received_inr']
	bank_charges    = request.GET['e_bank_charges']
	invoice_tds 	= request.GET['e_tds']
	e_proj_name 	= request.GET['e_proj_namex']
	e_id 			= request.GET['e_id']
	client_id 		= request.GET['client_id']

	try:
		for_invoice_date  = datetime.strptime(rec_date, "%m/%d/%Y").strftime('%Y-%m-%d')
	except:
		for_invoice_date  = rec_date
	update_invoice  = models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_id,proj_name=e_proj_name)
	for x in update_invoice:
		x.received_inr= received_inr
		x.bank_charges= bank_charges
		x.payment_status= remark
		if invoice_tds:
			x.tds = float(invoice_tds)
		else:
			tds = 0.0

		x.received_date  = datetime.now().date()
		if invoice_cancel=='1':
			x.cancel_invoice = '1'
			x.payment_status = None
			x.received_date  = None
			x.invoice_amount = None
			msg    = 'cancel'
			button = 'Submit'

		if invoice_cancel=='0':
			x.cancel_invoice = '0'
			x.payment_status = 'Paid'
			x.received_date  = for_invoice_date
			x.invoice_amount = invoice_amount
			msg    = 'ok'
			button = 'Unpaid'

		get_client_id 	= models.Client.objects.filter(id=request.GET['client_id']).first()
		if get_client_id.currency_type=='USD':
			x.usd = 'USD'
		else:
			x.inr = 'INR'

		check = models.invoice.objects.filter(invoice_no=invoice_no).count()
		if check>0:
			show_button= 'none'
		else:
			show_button = ''

		if checkbutton=="Unpaid":
			x.cancel_invoice = 0
			x.payment_status = None
			x.received_date  = None
			x.invoice_amount = None
			msg = 'unpaid'
		x.save()

	context={
	'show_button' : show_button,
	'msg'     	  : msg,
	'checkbutton' : checkbutton,
	'caption'     : button,
	}

	return HttpResponse(json.dumps(context))

def get_create_pdf(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,proj_name,merge,editable,currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,fontset,addline,get_period,get_page,layouts,split_month,ntype):
	set_global_month = int(split_month)
	print '------->>>>>',client_name,'-----',invoice_no
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

	#print '=======',client_name
	
	#dir      = '/home/munish/Documents/Finance/Finance/Current/Finance/'+str(tag_name)+'/'+client_name+'/Online/'
	dir      = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/'	
	#print '----------',dir
	if not os.path.exists(dir):
		os.makedirs(dir)
	srcfile      = '/var/www/html/invoice/it/static/pdf/1.png'
	dstroot      = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/1.png'	
	#dstroot      = '/home/munish/Documents/Finance/Finance/Curr`ent/Finance/'+str(tag_name)+'/'+client_name+'/Online/1.png'
	#print  '----------------',dstroot
	copyfile(srcfile, dstroot)
	srcfile1     = '/var/www/html/invoice/it/static/pdf/rings.png'
	dstroot1     = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/rings.png'
	#dstroot1     = '/home/munish/Documents/Finance/Finance/Current/Finance/'+str(tag_name)+'/'+client_name+'/Online/rings.png'
	copyfile(srcfile1, dstroot1)
	srcfile2     = '/var/www/html/invoice/it/static/pdf/'+str(img_tag)
	dstroot2     = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag
	#dstroot2     = '/home/munish/Documents/Finance/Finance/Current/Finance/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag
	copyfile(srcfile2, dstroot2)
	srcfile3     = '/var/www/html/invoice/it/static/pdf/'+str(img_tag)
	dstroot3     = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag
	#dstroot3     = '/home/munish/Documents/Finance/Finance/Current/Finance/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag
	copyfile(srcfile3, dstroot3)
	#print '----------',proj_name,'-----',currency

	voy_array = []
	ves_details  = models.vessel_selected_invoice.objects.filter(proj_name='CHM')
	if merge=='1':
		voy ={}
		for i in ves_details:
			if len(i.ship_name)>1:
				voy_array.append(i.voyage_no)
				voyage_number = voy_array
			else:
				voyage_number = i.voyage_no
		voy 	  = voyage_number
		voyage_no = ','.join(voy)
	else:
		pass

	if proj_name=='CHM':
		border_no = '3px';
	else:
		border_no = '0px;'
	

	if proj_name=='BOSS':
		border_linez = '1px'


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
	split_address11 = ''
	split_address22 = ''
	split_address33 = ''
	split_address44 = ''
	split_address55 = ''
	split_address66 = ''
	aa = 0
	tt = 0
	for x in vessel_details:
		try:
			account_name = x.account_type #vessel_type
		except:
			account_name = ''

		aa+=x.client.price*x.client.rate
		remove_splash_invoice_no = x.invoice_no.replace('/', '_')
		if proj_name=='CHM':
			extension_in_html 	 = remove_splash_invoice_no+'_'+x.ship_name+'_'+x.voyage_no+'_'+x.account_type+".html"
			extension_in_pdf  	 = remove_splash_invoice_no+'_'+x.ship_name+'_'+x.voyage_no+'_'+x.account_type+".pdf"
		else:
			try:
				extension_in_html 	 = remove_splash_invoice_no+'_'+x.account_type+".html"
				extension_in_pdf  	 = remove_splash_invoice_no+'_'+x.account_type+".pdf"
			except:
				extension_in_html 	 = remove_splash_invoice_no+'_'+x.vessel_type+".html"
				extension_in_pdf  	 = remove_splash_invoice_no+'_'+x.vessel_type+".pdf"

		client_details 	  		 = models.Client.objects.filter(client_name=client_name).first()
		inr_usd 				 = client_details.currency_type
		try:
			for_invoice_dates    = x.invoice_date.strftime('%d-%b-%Y')
		except:
			for_invoice_dates    = x.today.strftime('%d-%b-%Y')

		try:
			ship_det = models.pool_master.objects.filter(client_id=x.client_id,pool=x.account_type,client__proj_name='CHM').first()
		except:
			#pass
			if x.vessel_type!=None:
				ship_det = models.api_client_data.objects.filter(account_tab=x.vessel_type,client_id=x.client_id).first()
			else:
				ship_det = models.pool_master.objects.filter(client_id=x.client_id,pool=x.vessel_type,client__proj_name='BOSS').first()
			#ship_det = models.pool_master.objects.filter(client_id=x.client_id,client__proj_name='CHM').first()
		
		try:
			if editable!="edit":
				clientaddress   = ship_det.address.split(',') #x.client_address.split(',')
			else:
				clientaddress   = x.client_address.split(',')

			#print '----------',split_address1

			split_address11 = clientaddress[0]
			split_address22 = clientaddress[1]
			split_address33 = clientaddress[2]
			split_address44 = clientaddress[3]
			split_address55 = clientaddress[4]
			split_address66 = clientaddress[5]
		except:
			split_address11 = split_address11
			split_address22 = split_address22
			split_address33 = split_address33
			split_address44 = split_address44
			split_address55 = split_address55
			split_address66 = split_address66

		Html_file = open("/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_html),"w")
		#print '--------',"/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_html
		# Html_file.write('<center>');
		#Html_file = open("/home/munish/Documents/Finance/Finance/Current/Finance/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_html,"w")
		Html_file.write('<center>');
		# Html_file.write('<meta charset="utf-8">');
		# Html_file.write('<meta name="pdfkit-page-size" content="A4">');
        #Html_file.write('<meta name="pdfkit-orientation" content="Landscape">');
		# Html_file.write('<table style="width: 898px;" border="0" cellspacing="0" cellpadding="0">');
		Html_file.write('<table style="height:1200px;width:100%; position: ; top: 0; bottom: 0; left: 0; right: 0;border-collapse: collapse;font-size:0px">');
		Html_file.write('<tbody>');
		Html_file.write('<style>');
		# Html_file.write('thead { display: table-header-group; }');
		Html_file.write('td{');
		# Html_file.write('font-family:Tahoma');
		#print '------------------', len(calling_pdf)
		#if proj_name=='BOSS':
			#if len(calling_pdf)>=14 and len(calling_pdf)<=145:
		Html_file.write('font-size: '+str(fontset)+'px;'); #jab count 30 ho tab font size 12px hoga
			#else:
			#	Html_file.write("");
		#else:
		#	pass
		#else:
		 #	Html_file.write('padding:2px;');
		# #ruben.araos@ultratank.com
		# Html_file.write('thead { display: table-header-group; }');
		# Html_file.write('tfoot { display: table-row-group; }');
		# Html_file.write('tr { page-break-inside: avoid; }');
		# Html_file.write('table, tr, td, th, tbody, thead, tfoot, td div { page-break-inside: avoid !important; }');
		# #

		Html_file.write('table { page-break-after: always !important; }');	
		Html_file.write('page-break-inside: avoid !important;');	
		# Html_file.write('thead { display: table-row-group; }')
		# Html_file.write('padding: 7px 0;margin: 7px 0 0 0;');
		Html_file.write('padding:2px;');
		Html_file.write('}');
		# Html_file.write('.hd{');
		# Html_file.write('font-weight:bold;');
		# Html_file.write('}');
		# Html_file.write('.style1 {');
		# Html_file.write('color: #c4c3c2;');
		# Html_file.write('font-weight: bold;');
		# Html_file.write('}');
		# Html_file.write('.style2 {');
		# Html_file.write('color: #c4c3c2;');
		# Html_file.write('font-weight: bold;');
		# Html_file.write('}');
		# Html_file.write('.style3 {');
		# Html_file.write('color: black;');
		# Html_file.write('font-weight: bold;');		
		# Html_file.write('}');
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
		Html_file.write('<td style="padding: 10px; border-top: '+str(border_no)+' double #c4c3c2; border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="1" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #c4c3c2">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		customer = "Customer"+"'s"
		Html_file.write('<td style="background: #CCCCCC;border:1px solid #c4c3c2" colspan="2"><span class="hd">'+customer+' name &amp; address:</span></td>');
		Html_file.write('<td rowspan="5" width="2%"  style="border:1px solid #c4c3c2">&nbsp;</td>');
		Html_file.write('<td style="background: #c4c3c2;border:1px solid #c4c3c2" width="22%"><span class="hd">Invoice No.</span>:</td>');
		Html_file.write('<td style="background: #CCCCCC;border:1px solid #c4c3c2" width="29%">'+x.invoice_no+'</td>');  # 
		Html_file.write('</tr>');
		Html_file.write('<tr style="border:1px solid #c4c3c2">');
								
						
		if editable!='edit':			
			# Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top"><strong>'+str(header)+'</strong><br />'+str(address)+'</td>');
			Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top"  style="border:1px solid #c4c3c2"><strong>'+str(split_address11)+'</strong><br>'+split_address22+'<br>'+split_address33+'<br>'+split_address44+'<br>'+split_address55+'<br>'+split_address66+'</td>');
		else:			
			# if client_name=='Petredec':
			# 	Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top" style="height:auto;border:0px"><b>'+str(x.ship_name)+'</b><br><b>'+'"'+str(x.ship_name)+'"'+'&nbsp;'+str(split_address1)+'</b><br>'+split_address2+'<br>'+split_address3+'<br>'+split_address4+'<br>'+split_address5+'<br>'+split_address6+'</td>');
			# else:
			Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top"  style="border:1px solid #c4c3c2"><strong>'+str(split_address11)+'</strong><br>'+split_address22+'<br>'+split_address33+'<br>'+split_address44+'<br>'+split_address55+'<br>'+split_address66+'</td>');

		Html_file.write('<td style="border:1px solid #c4c3c2">Date:</td>');
		# Html_file.write('<td><strong>'+str(format_invoice_date)+'</strong></td>');
		try:
			if get_page=='Please see Page 1':
				gt_pge = get_page
			else:
				gt_pge = datetime.strptime(get_page, "%Y-%m-%d").strftime('%d-%b-%Y')
		except:
			gt_pge = 'Please see Page 1'

		Html_file.write('<td style="border:1px solid #c4c3c2"><strong>'+str(for_invoice_dates)+'</strong></td>'); #Please see Page 1 '+str(for_invoice_dates)+'
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border:1px solid #c4c3c2">Our Ref.:</td>');
		Html_file.write('<td style="border:1px solid #c4c3c2"><strong>'+x.invoice_no+'</strong></td>'); #
		Html_file.write('</tr>');
		Html_file.write('<tr>');

		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and  currency=='INR':
			Html_file.write('<td width="21%" style="border:1px solid #c4c3c2">Customer GSTIN</td>');
			if editable!='edit':
				Html_file.write('<td width="28%" style="border:1px solid #c4c3c2">'+str(customer_no)+'</td>');
			else:
				Html_file.write('<td width="28%" style="border:1px solid #c4c3c2">'+str(customer_no)+'</td>');

			Html_file.write('<td style="border:1px solid #c4c3c2">Blue Water GSTIN:</td>');
			# Html_file.write('<td  style="border:1px solid #c4c3c2"><strong>05AACCB9907G2ZQ</strong></td>');
			#print '----------->>>>>>>>',client_name
			if client_name=='RELIANCE INDUSTRIES LIMITED (SEZ)':
				Html_file.write('<td style="border:1px solid #c4c3c2"><strong style="font-size:14px">05AACCB9907G2ZQ<br><b style="font-size:10px">LUT No: AD050324007341R</b></strong></td>');
			else:
				Html_file.write('<td style="border:1px solid #c4c3c2"><strong>05AACCB9907G2ZQ</strong></td>');
			Html_file.write('</tr>');

		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and  currency=='USD':
			print ''
		elif proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and  currency=='INR':
			Html_file.write('<td width="21%"  style="border:1px solid #c4c3c2">Customer GSTIN</td>');
			if editable!='edit':
				Html_file.write('<td width="28%"  style="border:1px solid #c4c3c2">'+str(customer_no)+'</td>');
			else:
				Html_file.write('<td width="28%"  style="border:1px solid #c4c3c2">'+str(customer_no)+'</td>');
			Html_file.write('<td style="border:1px solid #c4c3c2">Blue Water GSTIN:</td>');
			Html_file.write('<td style="border:1px solid #c4c3c2"><strong>05AACCB9907G2ZQ</strong></td>');
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

		Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Person Incharge:</td>');
		try:
			Html_file.write('<td  style="border:1px solid #c4c3c2"><strong>'+str(x.vm_name)+'</strong></td>');
		except:
			Html_file.write('<td  style="border:1px solid #c4c3c2"><strong></strong></td>');

		
		#print '-----',client_name
		if proj_name=='CHM' and currency=='INR' and client_name=='Reliance' and client_name=='Apeejay':
			#Html_file.write('<td class="hd">Disch Port,Disch Date</td>');
			Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2">Remarks</td>');
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
				Html_file.write('<td  style="border:1px solid #c4c3c2">'+str(ship_name)+',Voy No: ' +str(voy_no)+',Disch.Port: ' +str(disch_port)+'</td>');
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
				Html_file.write('<td style="border:1px solid #c4c3c2">'+str(merge_ship)+'</td>');


		if proj_name=='BOSS' and currency=='INR':			
			Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2">Invoice Period</td>');
		# if proj_name=='CHM' and currency=='INR':
		# 	if client_name=='Teekay':
			#Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2">Remarks:</td>');  # yeh wala hai teekay ka details 
		# 	else:
		# 		pass
			
			if editable=='edit':
				format_invoice_date = datetime.now().strftime("%d-%b-%Y")
				format_year 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%Y')
				format_month 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%b')
				int_month 			= datetime.strptime(x.month, "%Y-%m-%d").strftime('%m')
				get_month 			= monthrange(int(format_year),int(int_month))[1]
				format_year2 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%y')
				if get_period=='': #for keeping blank text
					remark = str(format_month)+'-'+str(format_year2) #'01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
				else:
					remark = get_period

				try:
					disch_port 		= x.disch_port
					for_disch_date 	= x.disch_date.strftime('%d-%b-%Y')
					merge_shipx		= str(disch_port)+','+str(for_disch_date)
				except:
					pass
				
				if client_name=='Teekay':
					Html_file.write('<td  style="border:1px solid #c4c3c2">'+str(merge_shipx)+'</td>');
				else:
					Html_file.write('<td  style="border:1px solid #c4c3c2">'+str(remark)+'</td>');
			else:
				remark = '01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
				Html_file.write('<td  style="border:1px solid #c4c3c2">'+str(remark)+'</td>');
		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			ship_name  = x.ship_name
			voy_no     = x.voyage_no
			if merge=='1':
				merge_ship = str(ship_name) +', '+str(voyage_no)
			else:
				try:
					voy_id = x.voyage_id
				except:
					voy_id = ''

				try:
					merge_ship = '<b style="font-size:11px">'+str(ship_name) +',Voy: '+str(voy_no)+'</b><b style="color:blue;font-size:11px"> (BW ID*: '+voy_id+')</b>'
				except:
					merge_ship = '<b style="font-size:11px">'+str(ship_name) +',Voy: '+str(voy_no)+'</b></b>'

			Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2">Your Ref.:</td>');
			if proj_name=='BOSS':
				if x.vessel_type!="0":					
					Html_file.write('<td style="border:1px solid #c4c3c2;;color:#00b6ed;font-weight:bold;font-size:12px">'+str(x.vessel_type)+' </td>');
				else:
					Html_file.write('<td style="border:1px solid #c4c3c2;;color:#00b6ed;font-weight:bold;font-size:12px">'+str(client_name)+' </td>');
			else:
				Html_file.write('<td style="border:1px solid #c4c3c2" >'+str(merge_ship)+'</td>');
		Html_file.write('</tr>');

		if proj_name=='BOSS' and currency=='INR': # yeh wala row sirf remark k liye hai jo INR mein aata hai
			Html_file.write('<tr>');
			Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Remarks:</td>');
			try:
				Html_file.write('<td style="border:1px solid #c4c3c2;font-size:12px">'+str(x.remark)+'</td>');
			except:
				Html_file.write('<td style="border:1px solid #c4c3c2"></td>');

			Html_file.write('<td class="hd" style="border:0px solid white"></td>');
			Html_file.write('<td class="hd" style="border:1px solid #c4c3c2"></td>');
			Html_file.write('<td class="hd" style="border:1px solid #c4c3c2"></td>');
			Html_file.write('</tr>');
		else:
		 	pass

		try:
			rem = "Enrolment Date:" +datetime.strptime(str(x.nomination_date),"%Y-%m-%d").strftime('%d %b %Y')
		except:
			rem = ''
		#print '--------->>>1111',rem

		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
			print ''
		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			Html_file.write('<tr>');
			if proj_name=='BOSS':
				Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Remarks:</td>');
				try:
					Html_file.write('<td style="border:1px solid #c4c3c2;color:#028ffa;font-weight:bold;font-size:12px">'+str(x.remark)+'</td>');
				except:
					Html_file.write('<td style="border:1px solid #c4c3c2;color:#028ffa;font-weight:bold"></td>');
				Html_file.write('<td style="border:1px solid #c4c3c2"></td>');
			else:
				Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Remarks</td>');
				try:
					Html_file.write('<td style="border:1px solid #c4c3c2;font-size:12px">'+str(x.remark)+'</td>');
				except:
					Html_file.write('<td style="border:1px solid #c4c3c2;font-size:12px">'+str(rem)+'</td>');
					
				Html_file.write('<td style="border:1px solid #c4c3c2">&nbsp;</td>');
			if proj_name=='BOSS':
				Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Invoice Period:</td>');
			else:
				Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2;font-size:14px">Disch Port, Est.Disch Date:</td>');


		if proj_name=='CHM' and currency=='USD':
			try:
				disch_port 		= x.disch_port
				for_disch_date 	= x.disch_date.strftime('%d-%b-%Y')
			except:
				disch_port      = ''
				for_disch_date  = ''
			Html_file.write('<td style="border:1px solid #c4c3c2">'+str(disch_port)+','+str(for_disch_date)+'</td>');
		elif proj_name=='BOSS' and currency=='USD':
			format_invoice_date = datetime.now().strftime("%d-%b-%Y")
			format_year 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%Y')
			format_month 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%b')
			int_month 			= datetime.strptime(x.month, "%Y-%m-%d").strftime('%m')
			format_year2 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%y')
			get_month 			= monthrange(int(format_year),int(int_month))[1]

			#print '--------',get_period
			if get_period!='':
				remarkx = get_period  #'Sep 2022 to Dec 2022'
			else:
				remarkx = str(format_month)+'-'+str(format_year2) #'01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
			Html_file.write('<td style="border:1px solid #c4c3c2;font-weight:normal">'+str(remarkx)+'</td>');


		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="padding: 10px; border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="1" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" style="background: #CCCCCC;border:1px solid #c4c3c2" colspan="2" align="center">Project Details</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" width="23%" style="border:1px solid #c4c3c2">Customer ID:</td>');
		service_type = 'Marine Services'
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
			elif client_name=='Adhart Shipping Pte. Ltd':
				customerID = 'Adhart/BW/'+str(proj_name)
			# elif client_name=='Adhart':
			# 	customerID   = str(client_name)+'/BW/'+str(proj_name)
			# 	service_type = 'Other Professional, Technical And Business Services'
			# 	span_type    = '[SAC Code: 998399]'			
			else:
				customerID = str(client_name)+'/BW/'+str(proj_name)

		elif proj_name=='CHM':
			if client_name=='Reliance':
				customerID   = 'RELIANCE/BW/CHM [Vendors/Business partner code : 3249511]'
				service_type = 'Other Professional, Technical And Business Services '
				span_type  	 = '[SAC Code: 998399]'			
			else:
				customerID   = str(client_name).upper()+'/BW/'+str(proj_name)
				service_type = 'Other Professional, Technical And Business Services'
				span_type    = ''


		if proj_name=='BOSS' and currency=='INR':
				displayz = ''
				col 	 = '7'
							
		# elif proj_name=='BOSS' and currency=='USD':
		# 	#if client_name!='Shell':
		# 	displayz = 'none'
		# 	col 	 = '6'
			# else:
			# 	displayz = 'none'
			# 	col 	 = '6'
		elif proj_name=='CHM' and currency=='INR':
			displayz = ''
			col 	 = '7'
						
		elif proj_name=='BOSS' and currency=='USD':
			#if client_name=='Shell':
				#displayz = 'none'
			#	col 	 = '6'
			#else:
			displayz = 'none'
			col 	 = '6'
						
		elif proj_name=='CHM' and currency=='USD':
			displayz = 'none'
			col 	 = '6'
					
		Html_file.write('<td width="77%"  style="border:1px solid #c4c3c2">'+str(customerID)+'</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Service Name:</td>');
		if proj_name=='BOSS' and currency=='INR' or proj_name=='BOSS' and currency=='USD':
			Html_file.write('<td style="border:1px solid #c4c3c2">Tech consultancy through BOSS</td>');
		elif  proj_name=='CHM' and currency=='INR' or proj_name=='CHM' and currency=='USD':
			if client_name=='Shell' or client_name=='Shell NWE':
				Html_file.write('<td style="border:1px solid #c4c3c2">Cargo Heating Management Services [Shell Contract No. DS65730] <b>'+str(account_name)+'</b> </td>')
			else:
				if client_name=='Ultranav':
					Html_file.write('<td style="border:1px solid #c4c3c2">Cargo Heating Management Services <b>['+str(x.account_type)+']</b></td>');
				else:
					Html_file.write('<td style="border:1px solid #c4c3c2">Cargo Heating Management Services</td>');

		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" style="border:1px solid #c4c3c2 !important">Service Type:</td>');
		Html_file.write('<td style="border:1px solid #c4c3c2">'+str(service_type)+' <span class="style3"><b>'+str(span_type)+'</b></span></td>');
		Html_file.write('</tr>');

		Html_file.write('<tr>');
		Html_file.write('<td class="hd" style="border:1px solid #c4c3c2 !important">Service Nature:</td>');
		#print '--------->>>>>>>>>>>>>>>>>>>>>>',client_name
		#if client_name=='Oceonix':
		#	Html_file.write('<td style="border:1px solid #c4c3c2">Weather Routing</td>');
		#else:
		#Html_file.write('<td style="border:1px solid #c4c3c2">Data base, data processing charges</td>');
		if ntype==0:
			Html_file.write('<td style="border:1px solid #c4c3c2">Data base, data processing charges</td>');
		else:
			Html_file.write('<td style="border:1px solid #c4c3c2">'+str(ntype)+'</td>');
		Html_file.write('</tr>');

		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="padding: 10px; border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		if client_name=='Ultranav' and proj_name=='BOSS':
			font_size = ''
		else:
			font_size = ''
		Html_file.write('<table border="0" width="100%" cellspacing="0" cellpadding="0" '+str(font_size)+'>');
		Html_file.write('<tbody>');
		Html_file.write('<tr style="border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2;">');
		# Html_file.write('<td style="background: #cccccc; border: 1px solid #c4c3c2; width: 94%;" colspan="'+str(col)+'">&nbsp;</td>');
		Html_file.write('</tr>');
		Html_file.write('<thead>');
		Html_file.write('<tr>');
		#
		if x.client.client_name=='Oceonix':
			month_label = 'Qty'
		elif x.client.client_name=='Oldendorff':
			month_label = 'Qty(Days)'
		elif x.client.client_name=='MM Solution':
			month_label = 'Days'
		elif x.client.client_name=='ALADIN EXPRESS (ALX) DMCC':
			month_label = 'Days'
		elif x.client.client_name=='MSEACAPITAL':
			month_label = 'Month'
		elif x.client.client_name=='Norvic Shipping International LLC':
			month_label = 'Days'
		elif x.client.client_name=='Tankers (UK) Agencies Limited London':
			month_label = 'Days'
		elif x.client.client_name=='LIGHTHOUSE NAVIGATION PTE LTD':
			month_label = 'Days'
		elif x.client.client_name=='Adhart Shipping Pte. Ltd':			
			month_label = 'Days'
		elif x.client.client_name=='White sea':
			month_label = 'Days'
		else:
			month_label = 'Qty'

		Html_file.write('<th style="background-color: #cccccc;border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 7%;" align="center" valign="middle;">S.No.</th>');
		Html_file.write('<th style="background-color: #cccccc;border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 36%;" align="center" valign="middle;">Service Details</th>');
		Html_file.write('<th style="background-color: #cccccc;border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;" align="center" valign="middle;">Vessel</th>');
		if client_name=='Oceonix':
			Html_file.write('<th style="background-color: #cccccc;border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;" align="center" valign="middle;">Entity</th>');
		else:
			pass
		
		Html_file.write('<th style="background-color: #cccccc;border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;" align="center" valign="middle;">'+str(month_label)+'</th>');
		Html_file.write('<th style="background-color: #cccccc;width: 20.3102%;border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2;border-top: 1px solid #c4c3c2;" align="center" valign="middle;">Rate</th>');
		
		if client_name=='Cliff Shipping':
			Html_file.write('<th width="14%" align="center" valign="middle" style="background-color: #cccccc;width: 20.3102%;border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2;border-top: 1px solid #c4c3c2;white-space:nowrap;">Conv. Rate</th>');
		else:
			Html_file.write('<th width="14%" align="center" valign="middle" style="background-color: #cccccc;width: 20.3102%;border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2;border-top: 1px solid #c4c3c2;display:'+str(displayz)+';white-space:nowrap;">USD to INR Conv. Rate</th>');
		
		if proj_name=='CHM' or proj_name=='BOSS':
			if client_name=='Reliance':
				display = ''
			else:
				display = ''

		if proj_name=='BOSS':
			Html_file.write('<th style="background-color: #cccccc;border-bottom: 1px solid #c4c3c2;border-top:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;width: 10%;border-left: 1px solid #c4c3c2;;">Amount</th>');
		else:
			Html_file.write('<th style="background-color: #cccccc;border-bottom: 1px solid #c4c3c2;border-top:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;width: 10%;border-left: 1px solid #c4c3c2;;">Amount</th>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('</thead>');

		#print '------------',client_name,'=======',proj_name
		if currency=='USD':
			usd_tag = 'USD'
		else:
			usd_tag = ''

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

					elif client_del.client_name=='Litasco_Dubai':			
						if check_vessel>=1 and check_vessel<=5:						
							pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco_Dubai').first()
							i_price = pricess.price # 1700 #______1-2'
							#price_typess = '1-5'
						elif check_vessel>=6 and check_vessel<=10:
							pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco_Dubai').first()
							i_price = pricess.price # 1500 # _____3-5'
							#price_typess = '6-10'
						elif check_vessel>=11:
							pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco_Dubai').first()
							i_price = pricess.price # 1300# ______6-8'
							#price_typess = '11 and Up'
					else:
						i_price = x.client.price
						#print '=dfdfdsfdfdddddddddd'

					client_price = i_price*x.qty
					amount 		 = client_price
					amt 		 = amount
					total_amount = amount					
				except:				
					#price_list   = models.Client.objects.filter(proj_name='BOSS',id=112).first()	
					price_list   = models.Client.objects.filter(proj_name='BOSS',client_name=client_name).first()
					client_price = (price_list.price*x.qty)
					amount 		 = client_price
					amt 		 = client_price
					total_amount = client_price

			


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
			y 	= 1
			tx 	= 0
			for j in calling_pdf:
				#print '-------->>>>>>>>>>>>>>>>>>>>>>>>',set_global_month
				try:
					if j.heading!=None:
						heads = j.heading
					else:
						heads = 'Tech consultancy through BOSS'
				except:
					heads = 'Tech consultancy through BOSS'	

				
				#print '---------->>>>',	j.ship_name #,'----',j.rate,'---',j.price,'---',j.total_amount		
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 7%;font-weight:normal"><center>'+str(y)+'</center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 36%;white-space:nowrap;font-weight:normal"><b style="font-size:14px">'+str(heads)+'</b></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 16.9275%;white-space:nowrap;font-weight:normal"><b style="font-size:14px">'+j.ship_name+'</b></td>');
				if editable!='edit':
					if client_name=='Oceonix':
						Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 16.9275%;white-space:nowrap;font-weight:normal"><b style="font-size:14px">'+j.voyage_no+'</b></td>');
					else:
						print ''

					Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;font-weight:normal"><center><b style="font-size:14px">'+str(float(j.qty))+'</b></center></td>');
					Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;font-weight:normal"><center><b style="font-size:14px">'+str(float(j.client.price))+'</b></center></td>');
					
					if client_name=='Cliff Shipping':
						Html_file.write('<td style="border-left: solid #c4c3c2 1px;; border-bottom: solid #c4c3c2 1px;border-right: solid #c4c3c2 1px;font-weight:normal"><center><b style="font-size:14px">'+str(float(j.rate))+'</b></center></td>');
						
					else:
						Html_file.write('<td style="border-left: solid #c4c3c2 1px;; border-bottom: solid #c4c3c2 1px;border-right: solid #c4c3c2 1px;display:'+str(displayz)+';font-weight:normal"><center><b style="font-size:14px">'+str(float(j.client.rate))+'</b></center></td>');
					
					try:
						if j.client.day_calculate=='yes': #if client_name=='Oldendorff' or client_name=='MM Solution' or client_name=='ALADIN EXPRESS (ALX) DMCC' or client_name=='Adhart Shipping Pte. Ltd' or client_name=='Norvic Shipping Middle East DMCC' or client_name=='Tankers (UK) Agencies Limited London':
							get_days = models.merge_billing_day.objects.filter(ship_name=j.ship_name,client_name='Oldendorff').first()
							nday 	 = get_days.no_of_day
							cal_pay  = nday*j.client.price	
							get_mon  = str(j.today).split('-')
							monx 	 = get_mon[2][:2]
							amount 	 = cal_pay/set_global_month#30#int(monx)
							
						else:
							amount = round(amount,2)
							
					except:
						pass

					#print '-----',j.qty,'---',j.client.price,'---',j.client.rate,'---',amount	
					Html_file.write('<td style="border-left: solid #c4c3c2 1px;border-top: solid #c4c3c2 0px;border-right: solid #c4c3c2 1px;border-bottom: solid #c4c3c2 1px;font-weight:normal"><center><b style="font-size:14px">'+str(float(round(amount,2)))+'</b></center></td>');
				
				else:
					if client_name=='Oceonix':
						Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 16.9275%;white-space:nowrap;font-weight:normal"><b style="font-size:14px">'+j.voyage_no+'</b></td>');
					else:
						print ''

					Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;font-weight:normal"><center><b style="font-size:14px">'+str(float(j.qty))+'</b></center></td>');
					Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;font-weight:normal"><center><b style="font-size:14px">'+str(float(j.price))+'</b></center></td>');
					#Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: solid #c4c3c2 1px;display:'+str(displayz)+';font-weight:bold"><center>'+str(float(j.rate))+'</center></td>');
					if client_name=='Cliff Shipping':
						Html_file.write('<td style="border-left: solid #c4c3c2 1px;border-bottom: solid #c4c3c2 1px;border-right: solid #c4c3c2 0px;"><center><b style="font-size:14px">'+str(float(j.rate))+'</b></center></td>');
					else:	
						Html_file.write('<td style="border-left: solid #c4c3c2 1px;border-bottom: solid #c4c3c2 1px;border-right: solid #c4c3c2 0px;display:'+str(displayz)+'"><center><b style="font-size:14px">'+str(float(j.rate))+'</b></center></td>');

					# Html_file.write('<td></td>')
					if j.client.day_calculate!='yes':
					#if client_name!='Oldendorff' and client_name!='MM Solution' and client_name!='ALADIN EXPRESS (ALX) DMCC' and client_name!='Adhart Shipping Pte. Ltd' and client_name!='Norvic Shipping Middle East DMCC' and client_name!='Tankers (UK) Agencies Limited London':			
						if displayz=='none':
							#print '----heep'
							amtttt = (j.qty*j.price*j.rate)#j.total_amount #(j.qty*j.price*1)
						else:
							#print '-----jeep'
							amtttt = (j.qty*j.price*j.rate) #(j.qty*j.price*j.rate)/31
					else:
						try:
							get_month 	= str(j.invoice_date).split('-')
							monthx 		= get_month[2][:2]
							cal_payment = (j.price*j.qty)
							amtttt 		= cal_payment/set_global_month #30#int(monthx)
						except:
							amtttt 		= 0

					#print '---------->>>>',set_global_month
						

					#print '-------->>>//',amtttt
					#Html_file.write('<td style="border-top: solid #c4c3c2 1px;border-left: solid #c4c3c2 1px;border-right: solid #c4c3c2 1px;border-bottom: solid #c4c3c2 1px;font-weight:bold"><center>'+str(float(round(amtttt,2)))+'</center></td>');
					try:
						Html_file.write('<td style="border-top: solid #c4c3c2 0px;border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;width: 17%;font-weight:normal"><center><b style="font-size:14px">'+str(round(float(amtttt),1))+'</b></center></td>'); #str(round(float(amtttt/31),1)
					except:
						pass
					# Html_file.write('<div style="page-break-before:always"></div>');
				Html_file.write('</tr>');
				y+=1

			#print '----->>>>',addline
			if len(calling_pdf)<6:	
				max_length = 10
			else:
				max_length = int(addline)
			for c in range(1,max_length):
				Html_file.write('<tr>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 7%;white-space:nowrap">&nbsp;</td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 16.9275%;white-space:nowrap"></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 10%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2"><center></center></td>');
				if client_name=='Cliff Shipping':
					Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				else:
					pass

				if client_name=='Oceonix':
					Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2"><center></center></td>');
				else:
					pass
				if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
					Html_file.write('<td style="border-top: solid #c4c3c2 1px;border-left: solid #c4c3c2 1px; border-right: solid #c4c3c2 1px;"><center></center></td>');
				else:
					print ''
				Html_file.write('</tr>');



		amttt = 0
		total_sum = 0
		if proj_name=='CHM':
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 7%;"><center><strong>1</strong></center></td>');
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 36%;white-space:nowrap;"><strong>'+str(project)+'</strong></td>');
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 16.9275%;white-space:nowrap;"><strong>'+x.ship_name+'</strong></td>');
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

				elif client_del.client_name=='Litasco_Dubai':					
					if check_vessel>=1 and check_vessel<=5:						
						pricess = models.Client.objects.filter(price_type='1-5',proj_name='CHM',client_name='Litasco_Dubai').first()
						i_price = pricess.price # 1700 #______1-2'
						#price_typess = '1-5'
					elif check_vessel>=6 and check_vessel<=10:
						pricess = models.Client.objects.filter(price_type='6-10',proj_name='CHM',client_name='Litasco_Dubai').first()
						i_price = pricess.price # 1500 # _____3-5'
						#price_typess = '6-10'
					elif check_vessel>=11:
						pricess = models.Client.objects.filter(price_type='11 and Up',proj_name='CHM',client_name='Litasco_Dubai').first()
						i_price = pricess.price # 1300# ______6-8'
						#price_typess = '11 and Up'				
				else:
					i_price = x.client.price
				
				# if currency=='USD':
				# 	usd_tag = 'USD'
				# else:
				# 	usd_tag = ''
				if x.qty>=1.0:
					qtys = int(x.qty)
				else:
					qtys = x.qty 

				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;"><center><strong>'+str(qtys)+'</strong></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;"><center><strong>'+str(float(i_price))+'</strong></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2;display:'+str(displayz)+'"><center><strong> '+str(float(x.client.rate))+'</strong></center></td>');				
				Html_file.write('<td style="border-left: solid #c4c3c2 1px; border-top: solid #c4c3c2 0px; border-bottom: solid  #c4c3c2 1px; border-right: solid  #c4c3c2 1px;"><center><strong>'+str(usd_tag)+' '+str(float(round(amount,2)))+'</strong></center></td>');
				
				
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 7%;"><center></center></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 36%;white-space:nowrap"></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 16.9275%;white-space:nowrap"></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;"><center></center></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;"><center></center></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;"><center></center></td>');
				# Html_file.write('<td style="border-left: solid #c4c3c2 1px; border-top: solid #c4c3c2 1px; border-bottom: solid  #c4c3c2 1px; border-right: solid  #c4c3c2 1px;"><center></center></td>');


			else:
				if currency=='USD':
					usd_tag = 'USD'
				else:
					usd_tag = ''

				if x.qty==1.0:
					qtys = int(x.qty)
				else:
					qtys = x.qty 

				Html_file.write('<td style="border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2; width: 10%;"><center>'+str(qtys)+'</center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2; width: 17%;"><center><b>'+str(float(x.price))+'</b></center></td>');
				Html_file.write('<td style="border-left: solid #c4c3c2 1px;border-bottom: solid #c4c3c2 1px;border-right: solid #c4c3c2 1px;display:'+str(displayz)+'"><center><strong>'+str(float(x.rate))+'</strong></center></td>');
				if displayz=='none':
					amttt = (x.qty*x.price*1)
				else:
					amttt = (x.qty*x.price*x.rate)	

				

				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;width: 17%;border-top: 0px solid #c4c3c2;"><b style="white-space:nowrap">'+str(usd_tag)+' '+str(float(round(amttt,2)))+'</b></td>');

			Html_file.write('</tr>');


			for c in range(1,10):
				Html_file.write('<tr>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 7%;white-space:nowrap">&nbsp;</td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 16.9275%;white-space:nowrap"></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 10%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2"><center></center></td>');
				if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
					Html_file.write('<td style="border-top: solid #c4c3c2 1px;border-left: solid #c4c3c2 1px; border-right: solid #c4c3c2 1px;"><center></center></td>');
				else:
					print ''
				Html_file.write('</tr>');


		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
			if client_name=="RELIANCE INDUSTRIES LIMITED (SEZ)":
				tax_amount           = (total_amount*0)		 #(total_amount*0.18)
			else:
				tax_amount           = (total_amount*0.18)

			total_taxable_amount = (tax_amount+total_amount)
			round_off   		 = round(total_taxable_amount,0)
			in_words    		 = convert_money_to_text(round_off)
			#in_words  = num2words(round_off)			
			taxable     		 = 0
			tot_invoice 		 = 0
			#print '______>>>>',	in_words

		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			try:
				tax_amount = x.client.price*x.qty
			except:
				tax_amount = 0
			if editable!='edit':
				get_monthc 		= str(x.today).split('-')
				monthc 			= get_monthc[2][:2]
				qrty 			= 'SELECT sum(qty*price)/'+str(monthc)+' FROM invoice.it_invoice where invoice_no="'+str(invoice_no)+'"'
				cursor 			= connection.cursor()
				cursor.execute(qrty)
				tot_amt_details = cursor.fetchall()
				total_sum 		= tot_amt_details[0]
				
				if client_name=='Oldendorff':
					total_amount 	= round(total_sum[0],0)
					aa 				= round(total_amount,0)			
				else:	
					tt+=total_amount		
					if client_name=='Ultranav' and proj_name=='BOSS':
						aa 				= tt
						total_amount 	= tt
						tax_amount  	= tt
					else:
						total_amount 	= aa
						tax_amount  	= aa #total_amount	 #amount
						aa 				= total_amount
				

			else:
				get_mont 		= str(x.invoice_date).split('-')
				monthb 			= set_global_month #30#get_mont[2][:2]
				qrtxxy 			= 'SELECT sum(qty*price)/'+str(monthb)+' FROM it_invoice where invoice_no="'+str(invoice_no)+'"'
				cursor 			= connection.cursor()
				cursor.execute(qrtxxy)
				tot_amt_detas   = cursor.fetchall()
				total_sumcc     = tot_amt_detas[0]
				
				if client_name=='Oldendorff':
					total_amount 	= round(total_sumcc[0],0)
					aa 				= round(total_amount,0)
					tax_amount      = aa
				else:
					tax_amount  =  amttt

			if client_name=='Oldendorff':									
				try:
					db_amt 				= models.invoice.objects.filter(invoice_no=invoice_no,proj_name='BOSS',ship_name=x.ship_name).first()
					db_amt.total_amount = total_sum[0]
					db_amt.usd_amount   = total_sum[0]
					db_amt.save()
				except:
					db_amt 				= models.invoice.objects.filter(invoice_no=invoice_no,proj_name='BOSS',ship_name=x.ship_name).first()
					db_amt.total_amount = total_sumcc[0]
					db_amt.usd_amount   = total_sumcc[0]
					db_amt.save()

			# if client_name=='Oldendorff':
			# 	tax_amount = amount
			# 	round_off = round(tax_amount,4)
			# 	in_words = convert_money_to_text(round_off)
			# else:
			# 	tax_amount  =  aa
			# 	round_off = round(tax_amount,4)
			# 	in_words = convert_money_to_text(round_off)

			#print '==============',i_price
			if tax_amount!=0:
				total_taxable_amount = tax_amount #amount
			else:
				total_taxable_amount = amount
			
			if proj_name=='CHM':
				round_off 		 = round(amount,0) #round(total_amount,0)
			else:
				round_off 		 = round(total_amount,0) #round(total_amount,0)
			in_words 			 = convert_money_to_text(round_off)

		elif proj_name=='BOSS' and currency=='INR':
				#tax_amount = x.client.price*x.qty				
				tax_amount = total_amount*0.18
				total_taxable_amount = tax_amount
				round_off = round(total_taxable_amount,4)
				in_words = convert_money_to_text(round_off)

		# if proj_name=='BOSS' and currency=='USD':
		# 		total_taxable_amount = x.client.price
		# 		round_off = round(total_taxable_amount,0)
		# 		in_words  = num2words(round_off) +' only'
		#print '--------//',total_amount
		if editable!='edit':
			if client_name=='Shell' or client_name=='Shell NWE':
				due_date = x.today + timedelta(days=60)
			else:
				due_date = x.today + timedelta(days=30)
		else:
			if client_name=='Shell' or client_name=='Shell NWE':
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
			if client_name=='RELIANCE INDUSTRIES LIMITED (SEZ)':
				gst_label   = 'IGST Amount'
			else:
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

		if currency=='USD':
			if client_name=='Cliff Shipping':
				usd_tag = 'AED'
			else:
				usd_tag = 'USD'
		else:
			usd_tag = ''

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
			if client_name=='Oceonix':
				Html_file.write('<td '+str(e)+'></td>');
			else:
				pass
			  # colspan="2" for CHM
			if client_name=='Cliff Shipping':
				Html_file.write('<td '+str(e)+'></td>');
			else:
				pass

			if client_name=='Cliff Shipping':
				Html_file.write('<td '+str(d)+' '+str(colspan)+'><b>'+str(taxable)+'</b></td>');  # 
			else:
				Html_file.write('<td '+str(d)+' '+str(colspan)+'><b>'+str(taxable)+'</b></td>');

		
		#pricing = len(calling_pdf)*x.client.price
		

		if editable!='edit':
			#print '=========',total_amount
			if proj_name=='CHM':
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;border-top:1px solid #c4c3c2"><center><strong style="white-space:nowrap">'+str(usd_tag)+' '+str(float(round(amount,2)))+'</strong></center></td>'); # aa
			else:
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;border-top:1px solid #c4c3c2"><center><strong style="white-space:nowrap">'+str(usd_tag)+' '+str(float(round(aa,2)))+'</strong></center></td>'); # aa
		else:
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;border-top:1px solid #c4c3c2"><center><strong style="white-space:nowrap">'+str(usd_tag)+' '+str(float(round(total_amount,2)))+'</strong></center></td>'); # total_amount
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
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; border-right: 1px solid #c4c3c2;display:'+str(hide)+'"><strong>'+str(float(round(tax_amount,0)))+'</strong></td>');
		else:
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; border-right: 1px solid #c4c3c2;display:'+str(hide)+'"><strong>'+str(float(round(tax_amount,0)))+'</strong></td>');
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
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; border-right: 1px solid #c4c3c2;display:'+str(hide)+'"><strong>'+str(float(round(total_taxable_amount,0)))+'</strong></td>');
		else:
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; border-right: 1px solid #c4c3c2;display:'+str(hide)+'"><strong>'+str(float(round(total_taxable_amount,0)))+'</strong></td>'); #net_taxable_amount
		Html_file.write('<td style="display:'+str(hide)+'">&nbsp;</td>');
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="0" width="98%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		Html_file.write('<td style="; border-left: solid  #c4c3c2  1px; border-top: double #c4c3c2 1px;" width="86%">Total Invoice Amount Due (Rounded Off):</td>');
		if proj_name=='BOSS' and currency=='INR':
			if editable!='edit':
				Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(int(round(total_taxable_amount,0)))+'</strong></td>');
			else:
				Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(int(round(total_taxable_amount,0)))+'</strong></td>'); #net_taxable_amount
		elif proj_name=='BOSS' and currency=='USD':
			if client_name=='Cliff Shipping':
				currenc = 'AED'
			else:
				currenc = 'USD'
			# if client_name=='Shell':
			# 	Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(vnt))+'</strong></td>');
			# else:
			if editable!='edit':
				Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currenc)+' '+str(float(aa))+'</strong></td>');
			else:
				Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currenc)+' '+str(float(round(total_amount,0)))+'</strong></td>');
		elif proj_name=='CHM' and currency=='INR':
			currenc = 'INR'
			Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currenc)+' '+str(int(round(total_taxable_amount,0)))+'</strong></td>');
		elif proj_name=='CHM' and currency=='USD':
			if client_name=='Cliff Shipping':
				currenc = 'AED'
			else:
				currenc = 'USD'
			#if x.client.change_dollar!=1:
			Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currenc)+' '+str(float(amount))+'</strong></td>'); #amount
			#elif x.client.change_dollar==1:
			#	Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> SGD '+str(float(amount))+'</strong></td>');
			#else:
			#	Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(amount))+'</strong></td>');
		if client_name=='Cliff Shipping':
			currenc = 'AED'
		else:
			currenc = 'USD'

		if currency=='INR':
			currenct = 'INR'		
		else:
			currenct = 'USD'

		Html_file.write('</tr>');
		Html_file.write('<tr>');
		if client_name=='Cliff Shipping':
			Html_file.write('<td style="background: #CCCCCC; border: solid  #c4c3c2  1px;" colspan="2"> <strong style="text-transform: capitalize;">AED '+str(in_words)+'</strong></td>');
		else:
			Html_file.write('<td style="background: #CCCCCC; border: solid  #c4c3c2  1px;" colspan="2"> <strong style="text-transform: capitalize;">'+str(currenct)+' '+str(in_words)+'</strong></td>');

		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: solid  #c4c3c2  1px; border-bottom: solid  #c4c3c2  1px;" align="right" valign="middle">Payment Due Date</td>');
		try:
			if get_page=='Please see Page 1':
				get_pge = due_date_format
			else:
				get_pge = due_date_format #due_date_format
		except:
			get_pge = due_date_format

		Html_file.write('<td style="border-left: solid  #c4c3c2  1px; border-right: solid  #c4c3c2  1px; border-bottom: solid  #c4c3c2  1px;"><b>'+str(due_date_format)+'</b></td>'); #'+str(due_date_format)+'
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="0" width="99%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		Html_file.write('<td>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<td>Terms of payment:</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td>By wire transfer to our account "<b>BlueWater Trade Winds Pvt Ltd</b>" with-</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td>');
		Html_file.write('<table border="0" width="50%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');

		
		ct_dfc_bnk = models.bank_name.objects.filter(client_id=x.client_id,bank_name='HDFC Bank',client_id__proj_name=proj_name).count()
		#print '-------->>>>>>>>', x.client_id,'--------',ct_dfc_bnk
		
		if currency=='USD':
			if ct_dfc_bnk==0 and x.client_id==None:
				hdfc_bnk = models.bank_name.objects.filter(client_id=None,bank_name='HDFC Bank').first()			
				Html_file.write('<tr>');
				Html_file.write('<td><b>'+str(hdfc_bnk.bank_name)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td><b>'+str(hdfc_bnk.bank_address1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>SWIFT Code:<b>'+str(hdfc_bnk.swift_code1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');

				# Html_file.write('<tr>');
				# Html_file.write('<td>RTGS/NEFT IFSC Code:<b>'+str(hdfc_bnk.contact_no1)+'</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');

				Html_file.write('<td>Account Name:<b>'+str(hdfc_bnk.account_name1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Number:<b>'+str(hdfc_bnk.account_no1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				if hdfc_bnk.contact_no1!=None:
					Html_file.write('<td><b>'+str(hdfc_bnk.contact_no1)+'</b></td>');
				else:
					Html_file.write('<td><b></b></td>');
				Html_file.write('</tr>');

			elif ct_dfc_bnk!=0 and x.client_id==112:
				hdfc_bnk = models.bank_name.objects.filter(client_id=112,bank_name='HDFC Bank').first()
				Html_file.write('<tr>');
				Html_file.write('<td><b>'+str(hdfc_bnk.bank_name)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td><b>'+str(hdfc_bnk.bank_address1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>SWIFT Code:<b>'+str(hdfc_bnk.swift_code1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Name:<b>'+str(hdfc_bnk.account_name1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Number:<b>'+str(hdfc_bnk.account_no1)+'</b></td>');
				Html_file.write('</tr>');

				Html_file.write('<tr>');
				Html_file.write('<td></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td></td>');
				Html_file.write('</tr>');
				
			elif ct_dfc_bnk!=0 and x.client_id==15578:
				hdfc_bnk = models.bank_name.objects.filter(client_id=15578,bank_name='HDFC Bank').first()
				Html_file.write('<tr>');
				Html_file.write('<td><b>'+str(hdfc_bnk.bank_name)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td><b>'+str(hdfc_bnk.bank_address1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>SWIFT Code:<b>'+str(hdfc_bnk.swift_code1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Name:<b>'+str(hdfc_bnk.account_name1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Number:<b>'+str(hdfc_bnk.account_no1)+'</b></td>');
				Html_file.write('</tr>');

				Html_file.write('<tr>');
				Html_file.write('<td></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td></td>');
				Html_file.write('</tr>');

				# Html_file.write('<tr>');
				# Html_file.write('<td><b>Kindly route payment through:</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>BANK NAME: <b>'+str(hdfc_bnk.account_name2)+'</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>SWIFT CODE: <b>'+str(hdfc_bnk.swift_code2)+'</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(hdfc_bnk.account_no2)+'</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(hdfc_bnk.bank_address2)+'</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(hdfc_bnk.contact_no2)+'</b></td>');				
				# Html_file.write('</tr>');
				# 
			else:
				hdfc_bnk = models.bank_name.objects.filter(client_id=None,bank_name='HDFC Bank').first()			
				Html_file.write('<tr>');
				Html_file.write('<td><b>'+str(hdfc_bnk.bank_name)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td><b>'+str(hdfc_bnk.bank_address1)+'</b></td>');
				Html_file.write('</tr>');
				
				Html_file.write('<tr>');
				Html_file.write('<td>SWIFT Code:<b>'+str(hdfc_bnk.swift_code1)+'</b></td>');
				Html_file.write('</tr>');

				# Html_file.write('<tr>');
				# Html_file.write('<td>RTGS/NEFT IFSC Code:<b>'+str(hdfc_bnk.contact_no1)+'</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');

				Html_file.write('<tr>');
				Html_file.write('<td>Account Name:<b>'+str(hdfc_bnk.account_name1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Number:<b>'+str(hdfc_bnk.account_no1)+'</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				# if hdfc_bnk.contact_no1!=None:
				# 	Html_file.write('<td><b>'+str(hdfc_bnk.contact_no1)+'</b></td>');
				# else:
				# 	Html_file.write('<td><b></b></td>');
				Html_file.write('</tr>');
					# bank_address1
					# swift_code1
					# account_name1
					# account_no1
					# contact_no1
		else:
			hdfc_bnk = models.bank_name.objects.filter(client_id=None,bank_name='HDFC Bank').first()			
			Html_file.write('<tr>');
			Html_file.write('<td><b>'+str(hdfc_bnk.bank_name)+'</b></td>');
			Html_file.write('</tr>');
			Html_file.write('<tr>');
			Html_file.write('<td><b>'+str(hdfc_bnk.bank_address1)+'</b></td>');
			Html_file.write('</tr>');
			
			# Html_file.write('<tr>');
			# Html_file.write('<td>SWIFT Code:<b>'+str(hdfc_bnk.swift_code1)+'</b></td>');
			# Html_file.write('</tr>');


			Html_file.write('<tr>');
			Html_file.write('<td>RTGS/NEFT IFSC Code:<b>HDFC0000893</b></td>');
			Html_file.write('</tr>');
			Html_file.write('<tr>');

			Html_file.write('<tr>');
			Html_file.write('<td>Account Name:<b>'+str(hdfc_bnk.account_name1)+'</b></td>');
			Html_file.write('</tr>');
			Html_file.write('<tr>');
			Html_file.write('<td>Account Number:<b>'+str(hdfc_bnk.account_no1)+'</b></td>');
			Html_file.write('</tr>');
			Html_file.write('<tr>');
			# if hdfc_bnk.contact_no1!=None:
			# 	Html_file.write('<td><b>'+str(hdfc_bnk.contact_no1)+'</b></td>');
			# else:
			# 	Html_file.write('<td><b></b></td>');
			Html_file.write('</tr>');



		#print '-----------------------------,,.,.,',client_name
		#if client_name=='Stena Bulk Veg Oil':			
			#if proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD' or proj_name=='BOSS' and currency=='INR':
		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td><b>HDFC Bank</b></td>');
		# 	Html_file.write('</tr>');
		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td>56 Rajpur Road, Dehradun (UK), India</td>');
		# 	Html_file.write('</tr>');
		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td>SWIFT Code: <b>HDFCINBB</b></td>');
		# 	Html_file.write('</tr>');

		# 	if currency=='INR':
		# 		Html_file.write('<tr>');
		# 		Html_file.write('<td>RTGS/NEFT IFSC Code: <b>HDFC0000893</td>');
		# 		Html_file.write('</tr>');
		# 	else:
		# 		pass
			
		# 	Html_file.write('<tr>');
		# 	if client_name=='Oldendorff':
		# 		Html_file.write('<td>Account Number: <b>50200056415893</b></td>');
		# 	else:
		# 		Html_file.write('<td>Account Number: <b>02252560001213</b></td>');
		# 	Html_file.write('</tr>');
		# else:
						
		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td><b>HDFC Bank</b></td>');
		# 	Html_file.write('</tr>');
		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td>32, Arhat Bazar, Dehradun - 248001, Uttarakhand, INDIA</td>');
		# 	Html_file.write('</tr>');				
		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td>SWIFT Code: <b>HDFCINBB</b></td>');
		# 	Html_file.write('</tr>');				
		# 	if currency=='INR':
		# 		Html_file.write('<tr>');
		# 		Html_file.write('<td>RTGS/NEFT IFSC Code: <b>HDFC0000893</b></td>');
		# 		Html_file.write('</tr>');	
		# 	else:
		# 		pass	

		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td>Account Name: <b>BlueWater Trade Winds Pvt Ltd</b></td>');
		# 	Html_file.write('</tr>');
		# 	Html_file.write('<tr>');
			
		# 	if client_name=='Oldendorff':
		# 		Html_file.write('<td>Account Number: <b>50200056415893</b></td>');
		# 	else:
		# 		Html_file.write('<td>Account Number: <b>02252560001213</b></td>');
			

		# if client_name=='Sakhalin Energy':
		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td><br></td>');
		# 	Html_file.write('</tr>');
		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td><b>Kindly route payment through:</b></td>');
		# 	Html_file.write('</tr>');
		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td>BANK NAME: <b>J P MORGAN CHASE BANK, N.A.</b></td>');
		# 	Html_file.write('</tr>');

		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td>SWIFT CODE:<b>CHASUS33XXX</b></td>');
		# 	Html_file.write('</tr>');

		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td><b><div style="margin-left:50px">Detail:CHIPS ABA:0002</b></div></td>');
		# 	Html_file.write('</tr>');

		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td><b><div style="margin-left:50px">FEDWIRE ABA: 021000021</b></div></td>');
		# 	Html_file.write('</tr>');

		# 	Html_file.write('<tr>');
		# 	Html_file.write('<td><b><div style="margin-left:50px">CHIPS UID#354459</div></b></td>');
		# 	Html_file.write('</tr>');
		# 	Html_file.write('</tr>');
		# else:
		# 	pass
		#
				##########################
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; border-bottom: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
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
			Html_file.write('<td><div style="font-size:13px;text-align:left;color:blue;width:140%">* BW ID is the Voyage ID created when vessel/voyage is setup in BlueWater system. Please use BW ID in correspondence along with invoice number.</div></td>');

		# Html_file.write('<td></td>');
		#if proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD' or proj_name=='BOSS' and currency=='INR':
		Html_file.write('<td align="center" width="62%"><img src="/var/www/html/invoice/it/static/pdf/stamp.png" style="    margin-top: -213px;   margin-left: 300px;" width="185" height="195">');
		#else:
		#	Html_file.write('<td align="center" width="52%">');
		#Html_file.write('<p style="margin-top:-75px;margin-left:193px">For Blue Water Trade Winds Pvt Ltd</p>');
		Html_file.write('');
		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
			#Html_file.write('<p style="margin-top:-10px;margin-left: 197px">K. Gupta</p>');
			Html_file.write('');
		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			#Html_file.write('<p style="margin-top:-10px;margin-left: 197px">K Gupta</p>');
			Html_file.write('');

		#Html_file.write('<p style="margin-top:-10px;margin-left: 201px;">Authorized Signatory</p>');
		Html_file.write('');
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
		
		if proj_name=='CHM':		
			Html_file.write('<div style="margin-top:10px;border-top:0px solid grey;"><center style="font-family: arial; font-size: 9pt;">BlueWater Trade Winds Pvt. Ltd.</center><center style="font-family: arial; font-size: 8pt;">4, Siddarth Enclave, GMS Road, Ballupur, Dehradun - 248001 Uttarkhand INDIA<br /> Corporate Email: accounts@bwesglobal.com Website:www.bwesglobal.com</center><div> <div style="padding:6px;margin-bottom:0px;display:''" colspan="6" align="right"><img src="rings.png" width="95" height="36" style="float:right;margin-bottom:50px;margin-top:-44px;;margin-right:-26px;margin-right:27px" /><br /><span style="font-family: Arial, Helvetica, sans-serif; font-size: 7pt;float:right;margin-top:-29px;margin-right:-119px;">Visit us at : www.bwesglobal.com</span></div>');
				
		#else:
		 	#Html_file.write('<div style="margin-top:10px;"><center style="font-family: arial; font-size: 9pt;">Blue Water Trade Winds Pvt. Ltd.</center><center style="font-family: arial; font-size: 8pt;">4, Siddarth Enclave, GMS Road, Ballupur, Dehradun - 248001 Uttarkhand INDIA<br /> Tel:+91-135-2649301, 2649464 Corporate Email: info@bwesglobal.com Website:www.bwesglobal.com</center><div> <div style="padding:6px;margin-bottom:0px;display:''" colspan="6" align="right"><img src="rings.png" width="95" height="36" style="float:right;margin-bottom:50px;margin-top:-44px;;margin-right:-26px;margin-right:27px" /><br /><span style="font-family: Arial, Helvetica, sans-serif; font-size: 7pt;float:right;margin-top:-29px;margin-right:-119px;">Visit us at : www.bwesglobal.com</span></div>');
		 	#Html_file.write('<div style="margin-top:10px;border-top:0px solid grey;"><center style="font-family: arial; font-size: 9pt;">BlueWater Trade Winds Pvt. Ltd.</center><center style="font-family: arial; font-size: 8pt;">4, Siddarth Enclave, GMS Road, Ballupur, Dehradun - 248001 Uttarkhand INDIA<br /> Corporate Email: info@bwesglobal.com, accounts@bwesglobal.com Website:www.bwesglobal.com</center><div> <div style="padding:6px;margin-bottom:0px;display:''" colspan="6" align="right"><img src="rings.png" width="95" height="36" style="float:right;margin-bottom:50px;margin-top:-44px;;margin-right:-26px;margin-right:27px" /><br /><span style="font-family: Arial, Helvetica, sans-serif; font-size: 7pt;float:right;margin-top:-29px;margin-right:-119px;">Visit us at : www.bwesglobal.com</span></div>');
		Html_file.close()

		html  		= "/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_html)
		pdf 		= "/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_pdf)	
			
		if layouts=='asize':
			print '------------->>',layouts
		else:
			print '----->>',layouts
		 
		if proj_name=='BOSS':
			if layouts=='asize':
				options = {
					#'page-size':'A4',	    
					'margin-top':'0.1cm',
					'margin-bottom':'1.1cm',
					'margin-left':'0.1cm',
					'margin-right':'0.1cm',
					'encoding': "UTF-8",
					'footer-html':  '/var/www/html/invoice/it/templates/footer.html',	
					'enable-local-file-access': None,									
					'page-height': '390',
					'page-width': '200',
			}

			elif layouts=='afour':
				options = {
					'page-size':'A4',	    
					'margin-top':'0.1cm',
					'margin-bottom':'1.1cm',
					'margin-left':'0.1cm',
					'margin-right':'0.1cm',
					'encoding': "UTF-8",
					'footer-html':  '/var/www/html/invoice/it/templates/footer.html',	
					'enable-local-file-access': None,									
					#'page-height': '370',
					#'page-width': '200',
			}

			else:
				options = {
					'page-size':'A4',	    
					'margin-top':'0.1cm',
					'margin-bottom':'1.1cm',
					'margin-left':'0.1cm',
					'margin-right':'0.1cm',
					'encoding': "UTF-8",
					'footer-html':  '/var/www/html/invoice/it/templates/footer.html',	
					'enable-local-file-access': None,									
					#'page-height': '370',
					#'page-width': '200',
			}	

		else:
			options = {
				'page-size':'A4',
				#'enable-local-file-access': None,	
				
			}
	

		pdfkit.from_file([html],pdf,options=options)

		path_save  			= models.invoice.objects.filter(invoice_no=x.invoice_no).first()		
		path_save.pdf_path 	= pdf	
		path_save.save()		
		username   	= "BWTW059"
		password   	= "sandeep@123"
		clientname  = "OHMSERVER"
		servername  = "OHMSERVER"
		domain 	   	= 'WORKGROUP'
		ipaddress  	= "172.16.5.100"
		conn 	   	= SMBConnection(username,password,clientname,servername,domain,use_ntlm_v2=True, sign_options=2, is_direct_tcp=True)
		conn.connect(ipaddress,445)
		Shares 		= conn.listShares()
		#print '--------->>>><<',Shares[0].name
		share_name  = Shares[0].name
		
		if client_name=='Navig8 Chemical':
			path_name  = 'Finance/Current/Finance/HIM/Online/Navig8/Online/'
		if client_name=='Shell NWE':
			path_name  = 'Finance/Current/Finance/HIM/Online/Shell/Online/'				
		elif client_name =='Litasco':
			path_name  = 'Finance/Current/Finance/HIM/Online/Litasco/Online/'
		elif client_name =='Apeejay':
			path_name  = 'Finance/Current/Finance/BIM/Online/APJ/'	
		elif client_name =='Apeejay Shipping Limited':
			path_name  = 'Finance/Current/Finance/BIM/Online/APJ/'			
		elif client_name =='Clearlake LNG':
			path_name  = 'Finance/Current/Finance/BIM/Online/Clearlake/'	
		elif client_name =='Clearlake Spot':
			path_name  = 'Finance/Current/Finance/BIM/Online/Clearlake/'
		elif client_name=='Shell Bukom':
			path_name  = 'Finance/Current/Finance/BIM/Online/Shell/'
		elif client_name=='RELIANCE INTERNATIONAL LIMITED':
			path_name  = 'Finance/Current/Finance/BIM/Online/Reliance/'
		elif client_name=='Reliance Int Middle East':
		  	path_name  = 'Finance/Current/Finance/BIM/Online/Reliance/' #
		elif client_name=='RELIANCE INDUSTRIES LIMITED (SEZ)':
		  	path_name  = 'Finance/Current/Finance/BIM/Online/Reliance/' #
		elif client_name=='RELIANCE INDUSTRIES LIMITED (DTA)':
		  	path_name  = 'Finance/Current/Finance/BIM/Online/Reliance/' #
		elif client_name=='Reliance Industries (Middle East) DMCC':
		  	path_name  = 'Finance/Current/Finance/BIM/Online/Reliance/' #

		elif client_name=='MSEA Amber LLC':
		  	path_name  = 'Finance/Current/Finance/BIM/Online/MSEACAPITAL/' #

		  	
		else:			
			path_name  = 'Finance/Current/Finance/'+str(tag_name)+'/Online/'+str(client_name)+'/Online/'
			#print '--------',path_name
		sharedfiles = conn.listPath(share_name,path_name)
		#print '------------',path_name



		with open("/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_pdf), 'rb') as file:	
			if client_name=='Litasco':		  		
			 	conn.storeFile('Finance',"Finance/Current/Finance/HIM/Online/Litasco/Online/"+extension_in_pdf, file)
			 	#print '---...1'
			elif client_name=='Navig8 Chemical':
				conn.storeFile('Finance',"Finance/Current/Finance/HIM/Online/Navig8/Online/"+extension_in_pdf, file)
				#print '---...2'					
			elif client_name=='Apeejay':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/APJ/Online/"+extension_in_pdf, file)
				#print '---...3',file
			elif client_name=='Apeejay Shipping Limited':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/APJ/Online/"+extension_in_pdf, file)
				#print '---...3',file
			elif client_name=='Clearlake LNG':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Clearlake/Online/"+extension_in_pdf, file)
				#print '---...4',file
			elif client_name=='Clearlake Spot':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Clearlake/Online/"+extension_in_pdf, file)
				#print '---...5',file
			elif client_name=='Shell NWE':
				conn.storeFile('Finance',"Finance/Current/Finance/HIM/Online/Shell/Online/"+extension_in_pdf, file)
				#print '---...6',file
			elif client_name=='Shell Bukom':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Shell/Online/"+extension_in_pdf, file)

			elif client_name=='RELIANCE INTERNATIONAL LIMITED':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Reliance/Online/"+extension_in_pdf, file)

			elif client_name=='Reliance Int Middle East':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Reliance/Online/"+extension_in_pdf, file)
			
			elif client_name=='RELIANCE INDUSTRIES LIMITED (SEZ)':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Reliance/Online/"+extension_in_pdf, file)

			elif client_name=='RELIANCE INDUSTRIES LIMITED (DTA)':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Reliance/Online/"+extension_in_pdf, file)
				#print '---...7',file
			elif client_name=='Reliance Industries (Middle East) DMCC':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Reliance/Online/"+extension_in_pdf, file)

			elif client_name=='MSEA Amber LLC':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/MSEACAPITAL/Online/"+extension_in_pdf, file)
				#print '---...7',file

				
			else:
				conn.storeFile('Finance',"Finance/Current/Finance/"+str(tag_name)+"/Online/"+str(client_name)+"/Online/"+extension_in_pdf, file)	 
				#print '---...8',client_name			
		conn.close()

		url_path   = "/static/pdf/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_pdf
		#print '-------',url_path
		#url_path  = "/home/munish/Documents/Finance/Finance/Current/Finance/"+client_name+"/Online/"+extension_in_pdf
		url_details = models.invoice.objects.filter(invoice_no=x.invoice_no,client_id=x.client.id)
		for x in url_details:
			x.url = url_path
			x.save()
	return array


def get_create_pdf_client_name(calling_pdf,client_name,get_month,invoice_no,format_year,format_month,split_address1,split_address2,vm_name,format_invoice_date,customer_no,proj_name,merge,editable,currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,fontset,addline,get_period,get_page):
	set_global_month = 31
	#print '--------------------hello',client_name
	#print '____',split_address1,'____',split_address2,'___',split_address3,'___',split_address4,'___',split_address5,'---',invoice_no
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

	#print '=======',img_tag,'===',proj_name,'---',tag_name
	
	#dir      = '/home/munish/Documents/Finance/Finance/Current/Finance/'+str(tag_name)+'/'+client_name+'/Online/'
	dir      = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/'	
	#print '----------',dir
	if not os.path.exists(dir):
		os.makedirs(dir)
	srcfile      = '/var/www/html/invoice/it/static/pdf/1.png'
	dstroot      = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/1.png'	
	#dstroot      = '/home/munish/Documents/Finance/Finance/Current/Finance/'+str(tag_name)+'/'+client_name+'/Online/1.png'
	#print  '----------------',dstroot
	copyfile(srcfile, dstroot)
	srcfile1     = '/var/www/html/invoice/it/static/pdf/rings.png'
	dstroot1     = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/rings.png'
	#dstroot1     = '/home/munish/Documents/Finance/Finance/Current/Finance/'+str(tag_name)+'/'+client_name+'/Online/rings.png'
	copyfile(srcfile1, dstroot1)
	srcfile2     = '/var/www/html/invoice/it/static/pdf/'+str(img_tag)
	dstroot2     = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag
	#dstroot2     = '/home/munish/Documents/Finance/Finance/Current/Finance/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag
	copyfile(srcfile2, dstroot2)
	srcfile3     = '/var/www/html/invoice/it/static/pdf/'+str(img_tag)
	dstroot3     = '/var/www/html/invoice/it/static/pdf/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag
	#dstroot3     = '/home/munish/Documents/Finance/Finance/Current/Finance/'+str(tag_name)+'/'+client_name+'/Online/'+img_tag
	copyfile(srcfile3, dstroot3)
	#print '----------',proj_name,'-----',currency

	voy_array = []
	ves_details  = models.vessel_selected_invoice.objects.filter(proj_name='CHM')
	if merge=='1':
		voy ={}
		for i in ves_details:
			if len(i.ship_name)>1:
				voy_array.append(i.voyage_no)
				voyage_number = voy_array
			else:
				voyage_number = i.voyage_no
		voy 	  = voyage_number
		voyage_no = ','.join(voy)
	else:
		pass

	if proj_name=='CHM':
		border_no = '3px';
	else:
		border_no = '0px;'
	

	if proj_name=='BOSS':
		border_linez = '1px'


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
	split_address11 = ''
	split_address22 = ''
	split_address33 = ''
	split_address44 = ''
	split_address55 = ''
	split_address66 = ''
	aa = 0
	tt = 0
	for x in vessel_details:
		try:
			account_name = x.account_type#vessel_type
		except:
			account_name = ''

		aa+=x.client.price*x.client.rate
		remove_splash_invoice_no = x.invoice_no.replace('/', '_')
		if proj_name=='CHM':
			extension_in_html 	 = remove_splash_invoice_no+'_'+x.ship_name+'_'+x.voyage_no+".html"
			extension_in_pdf  	 = remove_splash_invoice_no+'_'+x.ship_name+'_'+x.voyage_no+".pdf"
		else:
			extension_in_html 	 = remove_splash_invoice_no+'_'+client_name+'_'+x.client.currency_type+".html"
			extension_in_pdf  	 = remove_splash_invoice_no+'_'+client_name+'_'+x.client.currency_type+".pdf"

		client_details 	  		 = models.Client.objects.filter(client_name=client_name).first()
		inr_usd 				 = client_details.currency_type
		try:
			for_invoice_dates    = x.invoice_date.strftime('%d-%b-%Y')
		except:
			for_invoice_dates    = x.today.strftime('%d-%b-%Y')

		try:
			ship_det = models.pool_master.objects.filter(client_id=x.client_id,pool=x.account_type,client__proj_name='CHM').first()
		except:
			#pass
			ship_det = models.pool_master.objects.filter(client_id=x.client_id,pool=x.vessel_type,client__proj_name='BOSS').first()
		#ship_det = models.pool_master.objects.filter(client_id=x.client_id,client__proj_name='CHM').first()
		
		try:
			if editable!="edit":
				clientaddress   = ship_det.address.split(',') #x.client_address.split(',')
			else:
				clientaddress   = x.client_address.split(',')
			split_address11 = clientaddress[0]
			split_address22 = clientaddress[1]
			split_address33 = clientaddress[2]
			split_address44 = clientaddress[3]
			split_address55 = clientaddress[4]
			split_address66 = clientaddress[5]
		except:
			split_address11 = split_address11
			split_address22 = split_address22
			split_address33 = split_address33
			split_address44 = split_address44
			split_address55 = split_address55
			split_address66 = split_address66

		Html_file = open("/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_html),"w")
		#print '--------',"/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_html
		# Html_file.write('<center>');
		#Html_file = open("/home/munish/Documents/Finance/Finance/Current/Finance/"+str(tag_name)+"/"+client_name+"/Online/"+extension_in_html,"w")
		Html_file.write('<center>');
		# Html_file.write('<meta charset="utf-8">');
		# Html_file.write('<meta name="pdfkit-page-size" content="A4">');
        #Html_file.write('<meta name="pdfkit-orientation" content="Landscape">');
		# Html_file.write('<table style="width: 898px;" border="0" cellspacing="0" cellpadding="0">');
		Html_file.write('<table style="height:1200px;width:100%; position: ; top: 0; bottom: 0; left: 0; right: 0;border-collapse: collapse;font-size:0px">');
		Html_file.write('<tbody>');
		Html_file.write('<style>');
		# Html_file.write('thead { display: table-header-group; }');
		#Html_file.write('td{');
		#Html_file.write('font-family:Tahoma');
		#Html_file.write('font-size: '+str(fontset)+'px;');
		# #
		# Html_file.write('thead { display: table-header-group; }');
		# Html_file.write('tfoot { display: table-row-group; }');
		# Html_file.write('tr { page-break-inside: avoid; }');
		# Html_file.write('table, tr, td, th, tbody, thead, tfoot, td div { page-break-inside: avoid !important; }');
		# #

		# Html_file.write('table { page-break-after:always }');		
		# Html_file.write('thead { display: table-row-group; }')
		# Html_file.write('padding: 7px 0;margin: 7px 0 0 0;');



		#Html_file.write('padding:0px;');
		#Html_file.write('}');
		# Html_file.write('.hd{');
		# Html_file.write('font-weight:bold;');
		# Html_file.write('}');
		# Html_file.write('.style1 {');
		# Html_file.write('color: #c4c3c2;');
		# Html_file.write('font-weight: bold;');
		# Html_file.write('}');
		# Html_file.write('.style2 {');
		# Html_file.write('color: #c4c3c2;');
		# Html_file.write('font-weight: bold;');
		# Html_file.write('}');
		# Html_file.write('.style3 {');
		# Html_file.write('color: black;');
		# Html_file.write('font-weight: bold;');		
		# Html_file.write('}');
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
		Html_file.write('<td style="padding: 10px; border-top: '+str(border_no)+' double #c4c3c2; border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="1" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #c4c3c2">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		customer = "Customer"+"'s"
		Html_file.write('<td style="background: #CCCCCC;border:1px solid #c4c3c2" colspan="2"><span class="hd">'+customer+' name &amp; address:</span></td>');
		Html_file.write('<td rowspan="5" width="2%"  style="border:1px solid #c4c3c2">&nbsp;</td>');
		Html_file.write('<td style="background: #c4c3c2;border:1px solid #c4c3c2" width="22%"><span class="hd">Invoice No.</span>:</td>');
		Html_file.write('<td style="background: #CCCCCC;border:1px solid #c4c3c2" width="29%">'+x.invoice_no+'</td>');  # 21%
		Html_file.write('</tr>');
		Html_file.write('<tr style="border:1px solid #c4c3c2">');
								
						
		if editable!='edit':			
			# Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top"><strong>'+str(header)+'</strong><br />'+str(address)+'</td>');
			Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top"  style="border:1px solid #c4c3c2"><strong>'+str(split_address11)+'</strong><br>'+split_address22+'<br>'+split_address33+'<br>'+split_address44+'<br>'+split_address55+'<br>'+split_address66+'</td>');
		else:			
			# if client_name=='Petredec':
			# 	Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top" style="height:auto;border:0px"><b>'+str(x.ship_name)+'</b><br><b>'+'"'+str(x.ship_name)+'"'+'&nbsp;'+str(split_address1)+'</b><br>'+split_address2+'<br>'+split_address3+'<br>'+split_address4+'<br>'+split_address5+'<br>'+split_address6+'</td>');
			# else:
			Html_file.write('<td colspan="2" rowspan="2" align="left" valign="top"  style="border:1px solid #c4c3c2"><strong>'+str(split_address11)+'</strong><br>'+split_address22+'<br>'+split_address33+'<br>'+split_address44+'<br>'+split_address55+'<br>'+split_address66+'</td>');

		Html_file.write('<td style="border:1px solid #c4c3c2">Date:</td>');
		#Html_file.write('<td><strong>'+str(format_invoice_date)+'</strong></td>');
		if get_page=='Please see Page 1':
			gt_pge = get_page
		else:
			gt_pge = datetime.strptime(get_page, "%Y-%m-%d").strftime('%d-%b-%Y')
			
		Html_file.write('<td style="border:1px solid #c4c3c2"><strong>'+str(for_invoice_dates)+'</strong></td>'); # Please see Page 1'+str(for_invoice_dates)+' //By Sandeep Mookerjee on 10-Nov-2022
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border:1px solid #c4c3c2">Our Ref.:</td>');
		Html_file.write('<td style="border:1px solid #c4c3c2"><strong>'+x.invoice_no+'</strong></td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');

		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and  currency=='INR':
			Html_file.write('<td width="21%" style="border:1px solid #c4c3c2">Customer GSTIN</td>');
			if editable!='edit':
				Html_file.write('<td width="28%" style="border:1px solid #c4c3c2">'+str(customer_no)+'</td>');
			else:
				Html_file.write('<td width="28%" style="border:1px solid #c4c3c2">'+str(customer_no)+'</td>');

			Html_file.write('<td style="border:1px solid #c4c3c2">Blue Water GSTIN:</td>');
			Html_file.write('<td  style="border:1px solid #c4c3c2"><strong>05AACCB9907G2ZQ</strong></td>');
			Html_file.write('</tr>');

		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and  currency=='USD':
			print ''
		elif proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and  currency=='INR':
			Html_file.write('<td width="21%"  style="border:1px solid #c4c3c2">Customer GSTIN</td>');
			if editable!='edit':
				Html_file.write('<td width="28%"  style="border:1px solid #c4c3c2">'+str(customer_no)+'</td>');
			else:
				Html_file.write('<td width="28%"  style="border:1px solid #c4c3c2">'+str(customer_no)+'</td>');
			Html_file.write('<td style="border:1px solid #c4c3c2">Blue Water GSTIN:</td>');
			Html_file.write('<td style="border:1px solid #c4c3c2"><strong>05AACCB9907G2ZQ</strong></td>');
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
		#Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2;"></td>'); #poompuhar k liye
		Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2;">Person Incharge:</td>');
		try:
			#Html_file.write('<td  style="border:1px solid #c4c3c2"><strong></strong></td>');
			Html_file.write('<td  style="border:1px solid #c4c3c2"><strong style="font-size:12px">'+str(x.vm_name)+'</strong></td>');
		except:
			Html_file.write('<td  style="border:1px solid #c4c3c2"><strong></strong></td>');
		if proj_name=='CHM' and currency=='INR' and client_name=='Reliance' and client_name=='Apeejay':
			#Html_file.write('<td class="hd">Disch Port,Disch Date</td>');
			Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2">Remarks</td>');
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
				Html_file.write('<td  style="border:1px solid #c4c3c2">'+str(ship_name)+',Voy No: ' +str(voy_no)+',Disch.Port: ' +str(disch_port)+'</td>');
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
				Html_file.write('<td style="border:1px solid #c4c3c2">'+str(merge_ship)+'</td>');


		if proj_name=='BOSS' and currency=='INR' or client_name=='Reliance':			
			Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2">Invoice Period</td>');
			if editable=='edit':
				format_invoice_date = datetime.now().strftime("%d-%b-%Y")
				format_year 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%Y')
				format_month 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%b')
				int_month 			= datetime.strptime(x.month, "%Y-%m-%d").strftime('%m')
				get_month 			= monthrange(int(format_year),int(int_month))[1]

				if get_period=='': #for keeping blank text
					remark = '01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
				else:
					remark = get_period
				#remark = '01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
				Html_file.write('<td  style="border:1px solid #c4c3c2">'+str(remark)+'</td>');
			else:
				remark = '01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
				Html_file.write('<td  style="border:1px solid #c4c3c2">'+str(remark)+'</td>');
		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			ship_name  = x.ship_name
			voy_no     = x.voyage_no
			if merge=='1':
				merge_ship = str(ship_name) +', '+str(voyage_no)
			else:
				merge_ship = str(ship_name) +',Voy: '+str(voy_no)

			Html_file.write('<td class="hd"  style="border:1px solid #c4c3c2">Your Ref.:</td>');
			if proj_name=='BOSS':
				if x.vessel_type!="0":					
					Html_file.write('<td style="border:1px solid #c4c3c2">'+str(x.vessel_type)+' Fleet</td>');
				else:
					Html_file.write('<td style="border:1px solid #c4c3c2">'+str(client_name)+' Fleet</td>');
			else:
				Html_file.write('<td style="border:1px solid #c4c3c2" >'+str(merge_ship)+'</td>');
		Html_file.write('</tr>');
		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
			print ''
		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			Html_file.write('<tr>');
			if proj_name=='BOSS':
				Html_file.write('<td class="hd" style="border:1px solid #c4c3c2"></td>');
				Html_file.write('<td style="border:1px solid #c4c3c2">&nbsp;</td>');
				Html_file.write('<td style="border:1px solid #c4c3c2">&nbsp;</td>');
			else:
				Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Agent Hub</td>');
				Html_file.write('<td style="border:1px solid #c4c3c2">&nbsp;</td>');
				Html_file.write('<td style="border:1px solid #c4c3c2">&nbsp;</td>');
			if proj_name=='BOSS':
				Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Invoice Period:</td>');
			else:
				Html_file.write('<td class="hd" style="border:1px solid #c4c3c2;font-size:10px">Disch Port, Est.Disch Date:</td>');


		if proj_name=='CHM' and currency=='USD':
			try:
				disch_port 		= x.disch_port
				for_disch_date 	= x.disch_date.strftime('%d-%b-%Y')
			except:
				disch_port      = ''
				for_disch_date  = ''
			Html_file.write('<td style="border:1px solid #c4c3c2">'+str(disch_port)+','+str(for_disch_date)+'</td>');
		elif proj_name=='BOSS' and currency=='USD':
			format_invoice_date = datetime.now().strftime("%d-%b-%Y")
			format_year 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%Y')
			format_month 		= datetime.strptime(x.month, "%Y-%m-%d").strftime('%b')
			int_month 			= datetime.strptime(x.month, "%Y-%m-%d").strftime('%m')
			get_month 			= monthrange(int(format_year),int(int_month))[1]
	 		remarkx 			= '01-'+str(format_month)+' to '+str(get_month)+'-'+str(format_month)+'-'+str(format_year)
			Html_file.write('<td style="border:1px solid #c4c3c2;color:#00b6ed;font-weight:bold">'+str(remarkx)+'</td>');

		elif proj_name=='BOSS' and currency=='INR': # yeh wala row sirf remark k liye hai jo INR mein aata hai
			Html_file.write('<tr>');
			Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Remarks:</td>');
			try:
				Html_file.write('<td style="border:1px solid #c4c3c2;font-size:12px" colspan="4" >'+str(x.remark)+'</td>');
			except:
				Html_file.write('<td style="border:1px solid #c4c3c2"></td>');

			# Html_file.write('<td class="hd" style="border:0px solid white"></td>');
			# Html_file.write('<td class="hd" style="border:1px solid #c4c3c2"></td>');
			# Html_file.write('<td class="hd" style="border:1px solid #c4c3c2"></td>');
			Html_file.write('</tr>');
		


		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="padding: 10px; border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="1" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" style="background: #CCCCCC;border:1px solid #c4c3c2" colspan="2" align="center">Project Details</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" width="23%" style="border:1px solid #c4c3c2">Customer ID:</td>');
		service_type = 'Marine Services'
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
				customerID   = str(client_name).upper()+'/BW/'+str(proj_name)
				service_type = 'Other Professional, Technical And Business Services'
				span_type    = ''


		if proj_name=='BOSS' and currency=='INR':
				displayz = ''
				col 	 = '7'
							
		# elif proj_name=='BOSS' and currency=='USD':
		# 	#if client_name!='Shell':
		# 	displayz = 'none'
		# 	col 	 = '6'
			# else:
			# 	displayz = 'none'
			# 	col 	 = '6'
		elif proj_name=='CHM' and currency=='INR':
			displayz = ''
			col 	 = '7'
						
		elif proj_name=='BOSS' and currency=='USD':
			#if client_name=='Shell':
				#displayz = 'none'
			#	col 	 = '6'
			#else:
			displayz = 'none'
			col 	 = '6'
						
		elif proj_name=='CHM' and currency=='USD':
			displayz = 'none'
			col 	 = '6'
					
		Html_file.write('<td width="77%" style="border:1px solid #c4c3c2">'+str(customerID)+'</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" style="border:1px solid #c4c3c2">Service Name:</td>');
		if proj_name=='BOSS' and currency=='INR' or proj_name=='BOSS' and currency=='USD':
			Html_file.write('<td style="border:1px solid #c4c3c2">Tech consultancy through BOSS</td>');
		elif  proj_name=='CHM' and currency=='INR' or proj_name=='CHM' and currency=='USD':
			if client_name=='Shell' or client_name=='Shell NWE':
				Html_file.write('<td style="border:1px solid #c4c3c2">Cargo Heating Management Services [Shell Contract No. DS65730] <b>'+str(account_name)+'</b> </td>')
			else:
				Html_file.write('<td style="border:1px solid #c4c3c2">Cargo Heating Management Services</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td class="hd" style="border:1px solid #c4c3c2 !important">Service Type:</td>');
		Html_file.write('<td style="border:1px solid #c4c3c2">'+str(service_type)+' <span class="style3">'+str(span_type)+'</span></td>');
		Html_file.write('</tr>');

		Html_file.write('<tr>');
		Html_file.write('<td class="hd" style="border:1px solid #c4c3c2 !important">Service Nature:</td>');
		Html_file.write('<td style="border:1px solid #c4c3c2">Data base, data processing charges</td>');
		Html_file.write('</tr>');

		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="padding: 10px; border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="0" width="100%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		Html_file.write('<tr style="border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2;">');
		# Html_file.write('<td style="background: #cccccc; border: 1px solid #c4c3c2; width: 94%;" colspan="'+str(col)+'">&nbsp;</td>');
		Html_file.write('</tr>');
		Html_file.write('<thead>');
		Html_file.write('<tr>');
		Html_file.write('<th style="background-color: #cccccc;border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 7%;" align="center" valign="middle;">S.No.</th>');
		Html_file.write('<th style="background-color: #cccccc;border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 36%;" align="center" valign="middle;">Service Details</th>');
		Html_file.write('<th style="background-color: #cccccc;border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;" align="center" valign="middle;">Vessel</th>');
		Html_file.write('<th style="background-color: #cccccc;border-left: 1px solid #c4c3c2; border-top: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;" align="center" valign="middle;">Passage</th>');
		Html_file.write('<th style="background-color: #cccccc;width: 20.3102%;border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2;border-top: 1px solid #c4c3c2;" align="center" valign="middle;">Report ID</th>');
		Html_file.write('<th style="background-color: #cccccc;width: 20.3102%;border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2;border-top: 1px solid #c4c3c2;" align="center" valign="middle;">Rate</th>');
		Html_file.write('<th style="background-color: #cccccc;width: 20.3102%;border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2;border-top: 1px solid #c4c3c2;" align="center" valign="middle;"><center style="margin-left:12px">Qty&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</center></th>');
		Html_file.write('<th width="14%" align="center" valign="middle" style="background-color: #cccccc;width: 20.3102%;border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2;border-top: 1px solid #c4c3c2;white-space:nowrap;">Total Amount (Rs.)</th>');
		
		if proj_name=='CHM' or proj_name=='BOSS':
			if client_name=='Reliance':
				display = ''
			else:
				display = ''

		# if proj_name=='BOSS':
		# 	Html_file.write('<th style="background-color: #cccccc;border-bottom: 1px solid #c4c3c2;border-top:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;width: 10%;border-left: 1px solid #c4c3c2;;">Amount</th>');
		# else:
		# 	Html_file.write('<th style="background-color: #cccccc;border-bottom: 1px solid #c4c3c2;border-top:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;width: 10%;border-left: 1px solid #c4c3c2;;">Amount</th>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('</thead>');



		#print '------------',client_name,'=======',proj_name

		if x.proj_name=='BOSS' and currency=='INR' or x.proj_name=='CHM' and currency=='INR':
			if editable=='edit':
				try:
					amount = x.price*x.rate*x.qty
					amt=amount		
				except:
					amt = 1	
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
					total_amount = amount					
				except:				
					#price_list   = models.Client.objects.filter(proj_name='BOSS',id=112).first()	
					price_list   = models.Client.objects.filter(proj_name='BOSS',client_name=client_name).first()
					client_price = price_list.price*x.qty
					amount 		 = client_price
					amt 		 = client_price
					total_amount = client_price					


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
			tx = 0
			de = 0
			for j in calling_pdf:
				#print '----------->>>>....',j.voyage_no
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 7%;font-weight:normal"><center>'+str(y)+'</center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 36%;white-space:nowrap;font-weight:normal">'+str(project)+'</td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 16.9275%;white-space:nowrap;font-weight:normal">'+j.ship_name+'</td>');
				if editable!='edit':
					if client_name=='Poompuhar Shipping Corporation Limited' or client_name=='TNPGCL' or client_name=='Adhart':
						route 		= j.voyage_no
						report_id 	= int(j.voyage_id)						
						Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;font-weight:normal"><center>'+str(route)+'</center></td>');
						Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;font-weight:normal"><center>'+str(int(report_id))+'</center></td>');
					else:
						route 		= ''
						report_id 	= ''
						Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;font-weight:normal"><center>'+str(j.qty)+'</center></td>');
						Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;font-weight:normal"><center>'+str(float(j.price))+'</center></td>');
					
					try:
						Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;font-weight:normal"><center>'+str(float(j.price))+'</center></td>');
					except:
						Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;font-weight:normal"><center>'+str(float(j.client.price))+'</center></td>');

					try:
						Html_file.write('<td style="border-left: solid #c4c3c2 1px;; border-bottom: solid #c4c3c2 1px;border-right: solid #c4c3c2 1px;display:'+str(displayz)+';font-weight:normal"><center>'+str(int(j.rate))+'</center></td>');
					except:
						Html_file.write('<td style="border-left: solid #c4c3c2 1px;; border-bottom: solid #c4c3c2 1px;border-right: solid #c4c3c2 1px;display:'+str(displayz)+';font-weight:normal"><center>'+str(int(j.client.rate))+'</center></td>');


					if client_name=='Oldendorff':
						get_days = models.merge_billing_day.objects.filter(ship_name=j.ship_name,client_name='Oldendorff').first()
						nday 	 = get_days.no_of_day
						cal_pay  = nday*j.client.price	
						get_mon  = str(j.today).split('-')
						monx 	 = get_mon[2][:2]				
						amount 	 = cal_pay/int(monx)
					else:
						try:
							amount = float(j.price) #amount
						except:
							amount = 0
						de+=amount
					pms_total = de
					

					#print '-----',j.qty,'---',j.client.price,'---',j.client.rate,'---',amount
					Html_file.write('<td style="border-left: solid #c4c3c2 1px;border-top: solid #c4c3c2 0px;border-right: solid #c4c3c2 1px;border-bottom: solid #c4c3c2 1px;font-weight:normal"><center>'+str(float(round(amount,2)))+'</center></td>');
				
				else:
					if client_name=='Poompuhar Shipping Corporation Limited' or client_name=='TNPGCL' or client_name=='Adhart':
						route 		= j.voyage_no
						report_id 	= int(j.deadwt)
					else:
						route 		= ''
						report_id 	= ''					
					
					Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;font-weight:normal"><center style="white-space:nowrap">'+str(route)+'</center></td>');
					try:
						pr = j.price
					except:
						pr = 1
					Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;font-weight:normal"><center>'+str(report_id)+'</center></td>');
					#Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: solid #c4c3c2 1px;display:'+str(displayz)+';font-weight:bold"><center>'+str(float(j.rate))+'</center></td>');
					Html_file.write('<td style="border-left: solid #c4c3c2 1px;border-bottom: solid #c4c3c2 1px;border-right: solid #c4c3c2 0px;display:'+str(displayz)+'"><center>'+str(float(pr))+'</center></td>');
					# Html_file.write('<td></td>')
					if client_name!='Oldendorff':
						if displayz=='none':
							amtttt = (j.qty*j.price*1)
						else:
							try:
								amtttt = (j.qty*j.price*j.rate)
							except:
								amtttt = 1
					else:
						try:
							get_month 	= str(j.invoice_date).split('-')
							monthx 		= get_month[2][:2]
							cal_payment = (j.price*j.qty)
							amtttt 		= cal_payment/int(monthx)
						except:
							amtttt 		= 0

					de+=j.price					
						

					Html_file.write('<td style="border-top: solid #c4c3c2 0px;border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;width: 17%;font-weight:normal"><center>1</center></td>');
					Html_file.write('<td style="border-top: solid #c4c3c2 1px;border-left: solid #c4c3c2 1px;border-right: solid #c4c3c2 1px;border-bottom: solid #c4c3c2 1px;font-weight:normal"><center>'+str(float(round(amtttt,2)))+'</center></td>');
					# Html_file.write('<div style="page-break-before:always"></div>');
				pms_total = de
				Html_file.write('</tr>');
				y+=1


			if len(calling_pdf)<5:
				max_length = 5			
			else:
				max_length = int(addline)

			for c in range(1,max_length):
				Html_file.write('<tr>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 7%;white-space:nowrap">&nbsp;</td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 16.9275%;white-space:nowrap"></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 10%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2"><center></center></td>');
				if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
					Html_file.write('<td style="border-top: solid #c4c3c2 1px;border-left: solid #c4c3c2 1px; border-right: solid #c4c3c2 1px;"><center></center></td>');
				else:
					print ''
				Html_file.write('</tr>');



		amttt 		= 0
		total_sum 	= 0
		#print '--------',pms_total
		if proj_name=='CHM':
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 7%;"><center><strong>1</strong></center></td>');
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 36%;white-space:nowrap;"><strong>'+str(project)+'</strong></td>');
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 16.9275%;white-space:nowrap;"><strong>'+x.ship_name+'</strong></td>');
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
				

				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;"><center><strong>'+str(x.qty)+'</strong></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;"><center><strong>'+str(float(i_price))+'</strong></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2;display:'+str(displayz)+'"><center><strong>'+str(float(x.client.rate))+'</strong></center></td>');
				Html_file.write('<td style="border-left: solid #c4c3c2 1px; border-top: solid #c4c3c2 0px; border-bottom: solid  #c4c3c2 1px; border-right: solid  #c4c3c2 1px;"><center><strong>'+str(float(round(amount,2)))+'</strong></center></td>');
				

				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 7%;"><center></center></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 36%;white-space:nowrap"></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 16.9275%;white-space:nowrap"></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 10%;"><center></center></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;"><center></center></td>');
				# Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; width: 17%;"><center></center></td>');
				# Html_file.write('<td style="border-left: solid #c4c3c2 1px; border-top: solid #c4c3c2 1px; border-bottom: solid  #c4c3c2 1px; border-right: solid  #c4c3c2 1px;"><center></center></td>');


			else:
				Html_file.write('<td style="border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2; width: 10%;"><center><strong>'+str(x.qty)+'</strong></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2;border-bottom: 1px solid #c4c3c2; width: 17%;"><center><strong>'+str(float(x.price))+'</strong></center></td>');
				Html_file.write('<td style="border-left: solid #c4c3c2 1px;border-bottom: solid #c4c3c2 1px;border-right: solid #c4c3c2 1px;display:'+str(displayz)+'"><center><strong>'+str(float(x.rate))+'</strong></center></td>');
				if displayz=='none':
					amttt = (x.qty*x.price*1)
				else:
					amttt = (x.qty*x.price*x.rate)				
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;width: 17%;border-top: 0px solid #c4c3c2;"><center><strong>'+str(float(round(amttt,2)))+'</strong></center></td>');

			Html_file.write('</tr>');


			for c in range(1,10):
				Html_file.write('<tr>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 7%;white-space:nowrap">&nbsp;</td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 16.9275%;white-space:nowrap"></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 10%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2; width: 17%;"><center></center></td>');
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2"><center></center></td>');
				if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
					Html_file.write('<td style="border-top: solid #c4c3c2 1px;border-left: solid #c4c3c2 1px; border-right: solid #c4c3c2 1px;"><center></center></td>');
				else:
					print ''
				Html_file.write('</tr>');

		#pms_total =1
		if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
			if client_name=='Poompuhar Shipping Corporation Limited' or client_name=='TNPGCL' or client_name=='Adhart':
				tax_amount = pms_total*0.18
				total_taxable_amount = (tax_amount+pms_total)
				#print '-----',pms_total,'----',total_taxable_amount
			else:
				tax_amount = total_amount*0.18
				total_taxable_amount = (tax_amount+total_amount)
			#tax_amount           = (total_amount*0.18)			
			
			round_off   		 = round(total_taxable_amount,0)
			in_words    		 = convert_money_to_text(round_off)
			#in_words  = num2words(round_off)			
			taxable     		 = 0
			tot_invoice 		 = 0
			#print '______>>>>',	in_words

		elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
			try:
				tax_amount = x.client.price*x.qty
			except:
				tax_amount = 0
			if editable!='edit':
				get_monthc 		= str(x.today).split('-')
				monthc 			= get_monthc[2][:2]
				qrty 			= 'SELECT sum(qty*price)/'+str(monthc)+' FROM invoice.it_invoice where invoice_no="'+str(invoice_no)+'"'
				cursor 			= connection.cursor()
				cursor.execute(qrty)
				tot_amt_details = cursor.fetchall()
				total_sum 		= tot_amt_details[0]
				
				if client_name=='Oldendorff':
					total_amount 	= round(total_sum[0],0)
					aa 				= round(total_amount,0)					
				else:			
					aa 				= total_amount
					total_amount 	= aa
					tax_amount  	= aa #total_amount	 #amount	

			else:
				get_mont 		= str(x.invoice_date).split('-')
				monthb 			= get_mont[2][:2]
				qrtxxy 			= 'SELECT sum(qty*price)/'+str(monthb)+' FROM it_invoice where invoice_no="'+str(invoice_no)+'"'
				cursor 			= connection.cursor()
				cursor.execute(qrtxxy)
				tot_amt_detas   = cursor.fetchall()
				total_sumcc     = tot_amt_detas[0]
			
				if client_name=='Oldendorff':
					total_amount 	= round(total_sumcc[0],0)
					aa 				= round(total_amount,0)
					tax_amount      = aa
				else:
					tax_amount  =  amttt

			if client_name=='Oldendorff':									
				try:
					db_amt 				= models.invoice.objects.filter(invoice_no=invoice_no,proj_name='BOSS',ship_name=x.ship_name).first()
					db_amt.total_amount = total_sum[0]
					db_amt.usd_amount   = total_sum[0]
					db_amt.save()
				except:
					db_amt 				= models.invoice.objects.filter(invoice_no=invoice_no,proj_name='BOSS',ship_name=x.ship_name).first()
					db_amt.total_amount = total_sumcc[0]
					db_amt.usd_amount   = total_sumcc[0]
					db_amt.save()
				


			# if client_name=='Oldendorff':
			# 	tax_amount = amount
			# 	round_off = round(tax_amount,4)
			# 	in_words = convert_money_to_text(round_off)
			# else:
			# 	tax_amount  =  aa
			# 	round_off = round(tax_amount,4)
			# 	in_words = convert_money_to_text(round_off)

			#print '==============',i_price
			#pms_sum+=j.price
			if tax_amount!=0:
				total_taxable_amount = tax_amount #amount
			else:
				total_taxable_amount = amount
			
			round_off 			 = round(total_amount,0) #round(total_amount,0)
			in_words 			 = convert_money_to_text(round_off)
			
			#in_words  = num2words(round_off)


		elif proj_name=='BOSS' and currency=='INR':
			
			#tax_amount = x.client.price*x.qty
			if client_name=='Poompuhar Shipping Corporation Limited' or client_name=='TNPGCL' or client_name=='Adhart':
				tax_amount = pms_total*0.18
				#print ' -----yaha'
			else:
				tax_amount = total_amount*0.18
				#print '-----waha'
			total_taxable_amount = tax_amount
			round_off = round(total_taxable_amount,4)
			in_words = convert_money_to_text(round_off)

		# if proj_name=='BOSS' and currency=='USD':
		# 		total_taxable_amount = x.client.price
		# 		round_off = round(total_taxable_amount,0)
		# 		in_words  = num2words(round_off) +' only'
		#print '--------//',total_amount
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
			g 			= ''
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
			g 			= ''
			hide 		= 'none'
			colspan 	= ''
			currency 	= 'USD'
			gst_label   = ''
			tot_invoice = ''
			taxable     = 'Total'

		Html_file.write('<tr style="text-align: right;">');
		Html_file.write('<td '+str(a)+'>&nbsp;</td>');
		Html_file.write('<td '+str(b)+'>&nbsp;</td>');
		Html_file.write('<td '+str(c)+'>&nbsp;</td>');

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
			# Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="3"><b>'+str(taxable)+'</b></td>');  # colspan="2" for CHM
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

		
		#pricing = len(calling_pdf)*x.client.price
		

		if editable!='edit':
			if client_name=='Poompuhar Shipping Corporation Limited' or client_name=='TNPGCL' or client_name=='Adhart':
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;border-top:1px solid #c4c3c2"><center><strong>'+str(float(round(pms_total,2)))+'</strong></center></td>'); # amount 
			else:
				Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;border-top:1px solid #c4c3c2"><center><strong>'+str(float(round(aa,2)))+'</strong></center></td>'); # amount
		else:
			#print '=========',total_amount
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom:1px solid #c4c3c2;border-right: 1px solid #c4c3c2;border-top:1px solid #c4c3c2"><center><strong>'+str(float(round(total_amount,2)))+'</strong></center></td>'); # amount
		
		Html_file.write('<td style="display:'+str(hide)+'">&nbsp;</td>');
		Html_file.write('</tr>');

		Html_file.write('<tr style="text-align: right;">');
		Html_file.write('<td '+str(a)+'>&nbsp;</td>');
		Html_file.write('<td '+str(b)+'>&nbsp;</td>');
		Html_file.write('<td '+str(c)+'>&nbsp;</td>');

		if proj_name=='BOSS' and currency=='INR':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="3">'+str(gst_label)+'</td>'); # CHM colspan="2"
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
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; border-right: 1px solid #c4c3c2;display:'+str(hide)+'"><strong><center>'+str(float(round(tax_amount,0)))+'</center></strong></td>');
		else:
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; border-right: 1px solid #c4c3c2;display:'+str(hide)+'"><strong><center>'+str(float(round(tax_amount,0)))+'</center></strong></td>');
		Html_file.write('<td style="display:'+str(hide)+'">&nbsp;</td>');
		Html_file.write('</tr>');

		Html_file.write('<tr style="text-align: right;">');
		Html_file.write('<td '+str(a)+'>&nbsp;</td>');
		Html_file.write('<td '+str(b)+'>&nbsp;</td>');
		Html_file.write('<td '+str(c)+'>&nbsp;</td>');

		if proj_name=='BOSS' and currency=='INR':
			Html_file.write('<td '+str(e)+'></td>');
			Html_file.write('<td '+str(d)+' colspan="3">'+str(tot_invoice)+'</td>'); # colspan="2" for CHM
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
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; border-right: 1px solid #c4c3c2;display:'+str(hide)+'"><strong><center>'+str(float(round(total_taxable_amount,0)))+'</center></strong></td>');
		else:
			Html_file.write('<td style="border-left: 1px solid #c4c3c2; border-bottom: 1px solid #c4c3c2; border-right: 1px solid #c4c3c2;display:'+str(hide)+'"><strong><center>'+str(float(round(total_taxable_amount,0)))+'</center></strong></td>'); #net_taxable_amount
		Html_file.write('<td style="display:'+str(hide)+'">&nbsp;</td>');
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="0" width="98%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		Html_file.write('<td style="; border-left: solid  #c4c3c2  1px; border-top: double #c4c3c2 1px;" width="86%">Total Invoice Amount Due (Rounded Off):</td>');
		if proj_name=='BOSS' and currency=='INR':
			if editable!='edit':
				Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(int(round(total_taxable_amount,0)))+'</strong></td>');
			else:
				Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(int(round(total_taxable_amount,0)))+'</strong></td>'); #net_taxable_amount
		elif proj_name=='BOSS' and currency=='USD':
			# if client_name=='Shell':
			# 	Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(vnt))+'</strong></td>');
			# else:
			if editable!='edit':
				Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(aa))+'</strong></td>');
			else:
				Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(round(total_amount,0)))+'</strong></td>');
		elif proj_name=='CHM' and currency=='INR':
			Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(int(round(total_taxable_amount,0)))+'</strong></td>');
		elif proj_name=='CHM' and currency=='USD':
			#if x.client.change_dollar!=1:
			Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(amount))+'</strong></td>');
			#elif x.client.change_dollar==1:
			#	Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> SGD '+str(float(amount))+'</strong></td>');
			#else:
			#	Html_file.write('<td style="border-left: solid  #c4c3c2  1px; ; border-right: solid  #c4c3c2  1px; border-top: solid #c4c3c2 1px;" width="14%"><strong style="white-space:nowrap"> '+str(currency)+' '+str(float(amount))+'</strong></td>');

		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="background: #CCCCCC; border: solid  #c4c3c2  1px;" colspan="2"> <strong style="text-transform: capitalize;">'+str(in_words)+'</strong></td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: solid  #c4c3c2  1px; border-bottom: solid  #c4c3c2  1px;" align="right" valign="middle">Payment Due Date</td>');
		if get_page=='Please see Page 1':
			get_pge = get_page
		else:
			get_pge = due_date_format

		Html_file.write('<td style="border-left: solid  #c4c3c2  1px; border-right: solid  #c4c3c2  1px; border-bottom: solid  #c4c3c2  1px;"><strong>'+str(due_date_format)+'</strong></td>'); # Please see Page 1#due_date_format  By Sandeep Mookerjee
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
		Html_file.write('<table border="0" width="99%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		Html_file.write('<tr>');
		Html_file.write('<td>Terms of payment:</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td>By wire transfer to our account "<b>BlueWater Trade Winds Pvt Ltd</b>" with-</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td>');
		Html_file.write('<table border="0" width="50%" cellspacing="0" cellpadding="0">');
		Html_file.write('<tbody>');
		#print '-----------------------------,,.,.,Yahoo',client_name
		if client_name=='Stena Bulk Veg Oil':
			#print '-------------->>',client_name
			if proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD' or proj_name=='BOSS' and currency=='INR':
				Html_file.write('<tr>');
				Html_file.write('<td><b>HDFC Bank</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>56 Rajpur Road, Dehradun (UK), India</td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>SWIFT Code: <b>HDFCINBB</b></td>');
				Html_file.write('</tr>');
				if currency=='INR':
					Html_file.write('<tr>');
					Html_file.write('<td>RTGS/NEFT IFSC Code: <b>HDFC0000893</td>');
					Html_file.write('</tr>');
				else:
					pass
				Html_file.write('<tr>');
				Html_file.write('<td>Account Number: <b>02252560001213</b></td>');
				Html_file.write('</tr>');

				# Html_file.write('<tr>');
				# Html_file.write('<td><b>State Bank of India</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>(04207) PBB, Vasant Vihar, Dehradun - 248001</td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Bank Swift Code: SBININBB155</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Account Name: <b>Blue Water Trade Winds Pvt Ltd</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Bank Account:30512553698</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Bank Tel. # +91-135 276 5135 Fax # +91-135 276 1601&nbsp</td>');
				# Html_file.write('</tr>');
		else:
			#print '--------->>>>',client_name
			if proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD' or proj_name=='BOSS' and currency=='INR':
				# Html_file.write('<tr>');
				# Html_file.write('<td><b>State Bank of India</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>(04207) PBB, Vasant Vihar, Dehradun - 248001</td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Bank Swift Code: SBININBB155</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Account Name: <b>Blue Water Trade Winds Pvt Ltd</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Bank Account:30512553698</b></td>');
				# Html_file.write('</tr>');
				# Html_file.write('<tr>');
				# Html_file.write('<td>Bank Tel. # +91-135 276 5135 Fax # +91-135 276 1601&nbsp</td>');
				# Html_file.write('</tr>');
				##########################
				Html_file.write('<tr>');
				Html_file.write('<td><b>HDFC Bank</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>32, Arhat Bazar, Dehradun - 248001, Uttarakhand, INDIA</td>');
				Html_file.write('</tr>');				
				# Html_file.write('<tr>');
				# Html_file.write('<td>SWIFT Code: <b>HDFCINBB</b></td>');
				# Html_file.write('</tr>');
				
				if currency=='INR':
					Html_file.write('<tr>');
					Html_file.write('<td>RTGS/NEFT IFSC Code: <b>HDFC0000893</td>');
					Html_file.write('</tr>');
				else:
					pass

				Html_file.write('<tr>');
				Html_file.write('<td>Account Name: <b>BlueWater Trade Winds Pvt Ltd</b></td>');
				Html_file.write('</tr>');
				Html_file.write('<tr>');
				Html_file.write('<td>Account Number: <b>02252560001213</b></td>');
				Html_file.write('</tr>');
				##########################
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('</tbody>');
		Html_file.write('</table>');
		Html_file.write('</td>');
		Html_file.write('</tr>');
		Html_file.write('<tr>');
		Html_file.write('<td style="border-left: '+str(border_no)+' double #c4c3c2; border-right: '+str(border_no)+' double #c4c3c2; border-bottom: '+str(border_no)+' double #c4c3c2; width: 698px;" colspan="2" align="center" valign="middle">');
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
		# if proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD' or proj_name=='BOSS' and currency=='INR':
		# 	Html_file.write('<td align="center" width="52%"><img src="/var/www/html/invoice/it/static/pdf/stamp.png" style="margin-top: -224px;margin-left:215px" width="170" height="170">');
		# else:
		# 	Html_file.write('<td align="center" width="52%">');
		# Html_file.write('<p style="margin-top:-75px;margin-left:193px">For Blue Water Trade Winds Pvt Ltd</p>');
		# if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
		# 	Html_file.write('<p style="margin-top:-10px;margin-left: 197px">K. Gupta</p>');
		# elif proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
		# 	Html_file.write('<p style="margin-top:-10px;margin-left: 197px">K Gupta</p>');

		# Html_file.write('<p style="margin-top:-10px;margin-left: 201px;">Authorized Signatory</p>');
		if proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD' or proj_name=='BOSS' and currency=='INR':
			Html_file.write('<td align="center" width="52%"><img src="/var/www/html/invoice/it/static/pdf/stamp.png" style="margin-top: -224px;margin-left:215px" width="185" height="195">');
		else:
			Html_file.write('<td align="center" width="52%">');
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
		if proj_name=='CHM':		
		 	Html_file.write('<div style="margin-top:10px;border-top:0px solid grey;"><center style="font-family: arial; font-size: 9pt;">BlueWater Trade Winds Pvt. Ltd.</center><center style="font-family: arial; font-size: 8pt;">4, Siddarth Enclave, GMS Road, Ballupur, Dehradun - 248001 Uttarkhand INDIA<br /> Tel:+91-135-2649301, 2649464 Corporate Email: info@bwesglobal.com, accounts@bwesglobal.com Website:www.bwesglobal.com</center><div> <div style="padding:6px;margin-bottom:0px;display:''" colspan="6" align="right"><img src="rings.png" width="95" height="36" style="float:right;margin-bottom:50px;margin-top:-44px;;margin-right:-26px;margin-right:27px" /><br /><span style="font-family: Arial, Helvetica, sans-serif; font-size: 7pt;float:right;margin-top:-29px;margin-right:-119px;">Visit us at : www.bwesglobal.com</span></div>');
		# else:
		# 	Html_file.write('<div style="margin-top:10px;"><center style="font-family: arial; font-size: 9pt;">Blue Water Trade Winds Pvt. Ltd.</center><center style="font-family: arial; font-size: 8pt;">4, Siddarth Enclave, GMS Road, Ballupur, Dehradun - 248001 Uttarkhand INDIA<br /> Tel:+91-135-2649301, 2649464 Corporate Email: info@bwesglobal.com Website:www.bwesglobal.com</center><div> <div style="padding:6px;margin-bottom:0px;display:''" colspan="6" align="right"><img src="rings.png" width="95" height="36" style="float:right;margin-bottom:50px;margin-top:-44px;;margin-right:-26px;margin-right:27px" /><br /><span style="font-family: Arial, Helvetica, sans-serif; font-size: 7pt;float:right;margin-top:-29px;margin-right:-119px;">Visit us at : www.bwesglobal.com</span></div>');

		Html_file.close()

		html  		= "/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_html)
		pdf 		= "/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_pdf)	

	
		
		if proj_name=='BOSS':
			options = {
				# 'page-width'     			: '216mm',
				# 'page-height'     			: '279mm',
				'dpi'             			: '96',		
				'margin-top'				: '0.1cm',
				'margin-bottom'				: '1.1cm',
				'margin-left'				: '0.1cm',
				'margin-right' 				: '0.1cm',
				'encoding'					: "UTF-8",
				'footer-html'				: '/var/www/html/invoice/it/templates/footer.html',
				'no-outline'				: None,						
				'enable-local-file-access' 	: None,
				'page-height': '380',
				'page-width': '250',
				
				# 'page-height': a,
				# 'page-width': '200',				
			}
		else:
			options = {
				'page-size':'A4',
				
			}

		
		
		pdfkit.from_file([html],pdf,options=options)

		path_save  			= models.invoice.objects.filter(invoice_no=x.invoice_no).first()		
		path_save.pdf_path 	= pdf	
		path_save.save()		
		username   	= "BWTW059"
		password   	= "sandeep@123"
		clientname  = "OHMSERVER"
		servername  = "OHMSERVER"
		domain 	   	= 'WORKGROUP'
		ipaddress  	= "172.16.5.100"
		conn 	   	= SMBConnection(username,password,clientname,servername,domain,use_ntlm_v2=True, sign_options=2, is_direct_tcp=True)
		conn.connect(ipaddress,445)
		Shares 		= conn.listShares()
		share_name  = Shares[0].name
		#print 'Second for Poompuhar, TNPGCL',tag_name

		
		if client_name=='Navig8 Chemical':
			path_name  = 'Finance/Current/Finance/HIM/Online/Navig8/Online/'
		if client_name=='Shell NWE':
			path_name  = 'Finance/Current/Finance/HIM/Online/Shell/Online/'				
		elif client_name =='Litasco':
			path_name  = 'Finance/Current/Finance/HIM/Online/Litasco/Online/'
		elif client_name =='Apeejay':
			path_name  = 'Finance/Current/Finance/BIM/Online/APJ/'
		elif client_name =='Apeejay Shipping Limited':
			path_name  = 'Finance/Current/Finance/BIM/Online/APJ/'
		elif client_name=='Poompuhar Shipping Corporation Limited':
			path_name  = 'Finance/Current/Finance/BIM/Online/Poompar/'

		elif client_name=='Clearlake LNG':
			path_name  = 'Finance/Current/Finance/BIM/Online/Clearlake/'
		elif client_name=='Clearlake Spot':
			path_name  = 'Finance/Current/Finance/BIM/Online/Clearlake/'

		else:			
			path_name  = 'Finance/Current/Finance/'+str(tag_name)+'/Online/'+str(client_name)+'/Online/'
		sharedfiles = conn.listPath(share_name,path_name)	

		with open("/var/www/html/invoice/it/static/pdf/"+str(tag_name)+"/"+str(client_name)+"/Online/"+str(extension_in_pdf), 'rb') as file:	
			if client_name=='Litasco':		  		
			 	conn.storeFile('Finance',"Finance/Current/Finance/HIM/Online/Litasco/Online/"+extension_in_pdf, file)
			 	print '---...1'
			elif client_name=='Navig8 Chemical':
				conn.storeFile('Finance',"Finance/Current/Finance/HIM/Online/Navig8/Online/"+extension_in_pdf, file)
				print '---...2'					
			elif client_name=='Apeejay':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/APJ/Online/"+extension_in_pdf, file)
				print '---...3',file
			elif client_name=='Apeejay Shipping Limited':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/APJ/Online/"+extension_in_pdf, file)
				print '---...3',file
				
			elif client_name=='Shell NWE':
				conn.storeFile('Finance',"Finance/Current/Finance/HIM/Online/Shell/Online/"+extension_in_pdf, file)
			elif client_name=='Poompuhar Shipping Corporation Limited':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Poompar/Online/"+extension_in_pdf, file)

			elif client_name=='Clearlake LNG':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Clearlake/Online/"+extension_in_pdf, file)
			elif client_name=='Clearlake Spot':
				conn.storeFile('Finance',"Finance/Current/Finance/BIM/Online/Clearlake Spot/Online/"+extension_in_pdf, file)

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


def edit_invoice_details(request):
	if request.user.is_authenticated():
		if 'invoice_no' in request.GET:
			invoice_no 		= request.GET['invoice_no']
			client_name 	= request.GET['client_name']
			vessel_type     = request.GET['vessel_type']
			invoiceID       = request.GET['id']	
			login_user 		= request.user			


			#print '------',vessel_type
			#change_dollar 	= request.GET['change_dollar']	
			payment_status  = 0
			chk_type = models.invoice.objects.filter(invoice_no=invoice_no,id=invoiceID).first()
			if client_name== "Shell" and chk_type.proj_name=='BOSS':
				invoice_details = models.invoice.objects.filter(invoice_no=invoice_no,client__client_name=client_name,vessel_type=vessel_type,proj_name='BOSS',usd='USD')			
			
			if client_name== "Shell" and chk_type.proj_name=='CHM':
				invoice_details = models.invoice.objects.filter(invoice_no=invoice_no,client__client_name=client_name,vessel_type=vessel_type,proj_name='CHM',usd='USD')
			else:
				invoice_details = models.invoice.objects.filter(invoice_no=invoice_no,client__client_name=client_name,vessel_type=vessel_type)

			
			ship_array 				= []
			amount 					= 0
			hide   					= 'none'
			total_amount    		= 0
			currency        		= 0
			currency_tag    		= ''
			tag_show    			= ''
			customer_no     		= 0
			hidden 					= ''
			stena_array 			= ''
			weco_array  			= ''
			price_types 			= ''
			select_price 			= ''
			invoice_currency_type 	= ''
			invoice_nos 			= ''
			mix_invoice_no 			= ''
			ultra_array 			= []
			address 				= ''
			cl_array 				= []
			single_array 			= []
			acc_array 				= []
			account_l_array 		= []
			
			voyage_nos 				= ''
			show_row 				= 'none'
			pms_total = 0
			calsx = 0
			for x in invoice_details:
				if x.proj_name=='BOSS':
					caption = 'BlueWater Optimum Speed Services (BOSS)'
				elif x.proj_name=='CHM':
					caption = 'Cargo Heating Management Services (CHM)'

				rate 	 	= x.client.rate
				if x.client.client_name!='Poompuhar Shipping Corporation Limited':
					price 	= x.client.price
				else:
					price   = x.price

				currency 	= x.client.currency_type
				vm_name  	= x.vm_name
				client_name = x.client.client_name
				customer_no = x.client.tin_number

				if x.client.client_name=='Oldendorff':
					qty = x.qty
				else:
					qty = x.qty
				
				if x.client.client_name!='Poompuhar Shipping Corporation Limited':
					invoice_price = x.price
				else:
					invoice_price = x.price

				#print '--------->>>',qty

				
				invoice_rate  = x.rate

				if currency=='INR' and currency!='USD':
					invoice_currency_type = currency
					max_invoice_no 	 = models.invoice.objects.filter(inr='INR').order_by('-id').first()
					invoice_ns 		 = max_invoice_no.invoice_no
					no_split 		 = invoice_ns.split('/')
					invoice_no_first = int(no_split[0])+1
					invoce_no_sec 	 = '/'+(str(no_split[1]))
					mix_invoice_no   = str(invoice_no_first)+str(invoce_no_sec)
				elif currency!='INR' and currency=='USD':
					invoice_currency_type = currency
					max_invoice_no 	 = models.invoice.objects.filter(usd='USD').order_by('-id').first()
					invoice_ns 		 = max_invoice_no.invoice_no
					try:
						no_split 	 = invoice_ns.split('/')
					except:
						no_split 	 = invoice_ns.split('/')
					
					try:
						invoice_no_first = int(no_split[0])+1
						invoce_no_sec 	 = '/'+(str(no_split[1]))
						mix_invoice_no   = str(invoice_no_first)+str(invoce_no_sec)
					except:
						pass
				
				# if ty==0:
				# 	qty = 1
				# else:
				#qty = ty

				if x.proj_name=='CHM':
					tag_show = ''
				elif x.proj_name=='BOSS':
					tag_show = 'none'

				if x.proj_name=='BOSS' and currency=='USD' or x.proj_name=='CHM' and currency=='USD':
					#amount  = price*qty
					if x.client.client_name=='Oldendorff':
						year 				= datetime.strptime(x.month, "%Y-%m-%d").strftime('%Y')
						month_number        = datetime.strptime(str(x.month), "%Y-%m-%d").strftime('%m')	
						month_no 			= 12 #int(month_number)-1
						if month_no<10:
							month_str = "0"+str(month_no)
						else:
							month_str = month_no

						get_month   = monthrange(int(year),int(month_str))[1]
						split_day = (x.client.price)/(get_month)

						if qty>29:
							amount = x.client.price
						else:
							amount = qty*split_day
					else:
						amount   = invoice_price*qty
					rate 	 = 'nil'
					hide     = ''
					currency = x.client.currency_type
					if x.client_address:
						add_call_details = models.pool_master.objects.filter(pool=x.account_type,client__client_name='Shell',client__proj_name='BOSS').first()
						try:
							address = x.client_address
							#print '_____1111',x.account_type
						except:						
							address = add_call_details.address
							#print '_____222'			
					else:
						try:
							add_call_details = models.pool_master.objects.filter(pool=x.account_type,client__client_name='Shell',client__proj_name='BOSS').first()										
							address = add_call_details.address
							#print '_____3333'
						except:
							address = x.client_address	
							#print '_____444'					

				elif x.proj_name=='BOSS' and currency=='INR' or x.proj_name=='CHM' and currency=='INR':				
					if x.client.client_name=='Poompuhar Shipping Corporation Limited' or x.client.client_name=='TNPGCL':
						try:
							amount  = (invoice_price*qty)
							
						except:
							amount  = 0
						hide = ''
					else:
						try:
							amount  = (invoice_price*invoice_rate*qty)
						except:
							amount  = 0
							
						hide = ''

					
					currency = x.client.currency_type
					if x.client_address:
						address = x.client_address
					else:
						ship_details = models.Ship.objects.filter(ship_name=x.ship_name).first()					
						address     = x.client_address

				if x.proj_name=='BOSS' and currency=='USD' or x.proj_name=='CHM' and currency=='USD':
					
					#amount  	 = x.total_amount
		 			amount 	 = x.rate*x.price*x.qty
		 			total_amount+=amount
		 			currency_tag = 'USD'
		 		elif x.proj_name=='BOSS' and currency=='INR' or x.proj_name=='CHM' and currency=='INR':
		 			try:
			 			amount  = x.total_amount		 			
			 			total_amount+=amount
			 			currency_tag = 'INR'
		 			except:
		 				amount = 0
		 				total_amount = 0
		 				currency_tag = 'INR'

		 			#print '---==',amount

		 		if x.vessel_type:
		 			vessel_type = x.vessel_type
		 		else:
		 			vessel_type = None

		 		try:
			 		customer_no = x.client.tin_number
			 	except:
			 		customer_no = ''

		 		url = x.url
		 		invoice_date = x.invoice_date.date()

		 		if x.cancel_invoice==1:
		 			box_checked = 'checked'
		 			logo = 'Cancelled'
		 		else:
		 			box_checked = 'unchecked'
		 			logo = ''

		 		if x.remark:
		 			remark_details = x.remark
		 		else:
		 			remark_details = ''

		 		if x.invoice_amount==None and x.received_date==None:
		 			amt_checked =  'checked'
		 		else:
		 			amt_checked =  'unchecked'
		 		payment_status = x.payment_status

		 		stena_array = []
		 		weco_array  = []
		 		ultra_array = []
		 		other_array = []

		 		if client_name=='stena bulk':
			 		price_details = models.Client.objects.filter(client_name='stena bulk',proj_name='CHM').order_by('price_type')
			 		for z in price_details:
			 			stena_array.append({
			 				'price' 	 : z.price,
			 				'price_type' : z.price_type,
			 				})
			 	elif client_name=='Stena Bulk Veg Oil':
			 		price_details_weco = models.Client.objects.filter(client_name='Stena Bulk Veg Oil',proj_name='CHM').order_by('price_type')
			 		for zz in price_details_weco:
			 			weco_array.append({
			 				'price'  	 : zz.price,
			 				'price_type' : zz.price_type,
			 				})

			 	elif client_name=='Ultranav':
			 		price_details_ultra = models.Client.objects.filter(client_name='Ultranav',proj_name='CHM').order_by('price_type')
			 		for zzz in price_details_ultra:
			 			ultra_array.append({
			 				'price' 	 : zzz.price,
			 				'price_type' : zzz.price_type,
			 				})
			 	elif client_name=='Litasco':
			 		price_details_other = models.Client.objects.filter(client_name='Litasco',proj_name='CHM').order_by('price_type')
			 		for zoz in price_details_other:
			 			other_array.append({
			 				'price' 	 : zoz.price,
			 				'price_type' : zoz.price_type,
			 				})
			 	else:
			 		hidden = 'none'


		 		client_lists = models.Client.objects.filter(proj_name='BOSS',status=1)
		 		for c in client_lists:		 			
		 			if c.client_name not in cl_array:
		 				cl_array.append(c.client_name)

		 		for l in cl_array:
		 			single_array.append(l)


		 		account_lists = models.pool_master.objects.filter(client_id=64)
		 		for c1 in account_lists:		 			
		 			if c1.pool not in acc_array:
		 				acc_array.append(c1.pool)

		 		for l1 in acc_array:
		 			account_l_array.append(l1)
		 			


			 	price_types  = x.price_type
			 	select_price = x.price
			 	
			 	if x.client.day_calculate!='yes':
			 	#if client_name!='Oldendorff' and client_name!='MM Solution' and client_name!='MM Solution' and client_name!='ALADIN EXPRESS (ALX) DMCC' and client_name!='Adhart Shipping Pte. Ltd' and client_name!='Norvic Shipping Middle East DMCC' and client_name!='Tankers (UK) Agencies Limited London':# and client_name!='Oceonix':
			 		try:
				 		tot_amount 	 = x.rate*x.price*x.qty
				 		total_amount = tot_amount
				 		calsx+= tot_amount
				 	except:
				 		calsx = 0
			 		#print '---------',client_name
			 	else:			 		
			 		#splt_mnth  = str(x.invoice_date).split('-')
			 		splt_mnth  = str(x.month).split('-')
			 		split_yrs  = splt_mnth[0][2:]	
			 		get_month  = splt_mnth[1][:2]		
			 		last_mnth  = monthrange(int(split_yrs),int(get_month))[1]
			 		print '====',splt_mnth[0][2:],'----',last_mnth
			 		#print '-------',last_mnth
			 		cals 	   = (qty*x.price)/last_mnth
			 		tot_amount = cals
			 		calsx+=cals



			 	if x.client_id==15576 or x.client_id==83:
			 		voyage_nos = x.voyage_no
			 		show_row   = ''
			 	else:
			 		voyage_no  = ''
			 		show_row   = 'none'

			 	try:
			 		account_lis = x.account_type
			 	except:
			 		account_lis = x.vessel_type

			 	if x.heading!=None:
			 		heading = x.heading
			 	else:
			 		heading = 'Tech consultancy through BOSS'

			 	try:
			 		get_period = str(x.month)
			 	except:
			 		get_period = ""

			 	if x.nature_type!=None:
			 		nature_types = x.nature_type
			 	else:
			 		nature_types = "Data base, data processing charges"

			 	try:			 		
			 		get_last_month = x.month
			 	except:
			 		get_last_month = ""

			 	try:
			 		split_m = x.month.split('-')
			 		g_month = split_m[2]
			 		gt_last_mname = g_month
			 	except:
			 		gt_last_mname = ""

				ship_array.append({
					'ship_name'    : x.ship_name,
					'voyage_no'    : x.voyage_no,
					'caption' 	   : caption,
					'rate' 		   : rate,
					'price' 	   : price,
					'currency' 	   : currency,
					'amount'       : amount,
					'hide'		   : hide,
					'address'      : address,
					'invoice_no'   : x.invoice_no,
					'proj_name'    : x.proj_name,
					'vm_name'      : vm_name,
					'month_wise'   : x.month,
					'vessel_type'  : vessel_type,
					'client_name'  : client_name,
					'disch_port'   : x.disch_port,
					'disch_date'   : x.disch_date,
					'url'    	   : url,
					'invoice_date' : invoice_date,
					'qty'  		   : qty,
					'customer_no'  : customer_no,
					'invoice_price': invoice_price,
					'invoice_rate' : invoice_rate,
					'invoiceID'	   : x.id,
					'box_checked'  : box_checked,
					'logo'         : logo,
					'remark_det'   : remark_details,
					'amt_checked'  : amt_checked,
					'billing_flag' : x.client_flag,
					'total_amount' : tot_amount, #x.total_amount,
					'voyage_nos'   : voyage_nos,
					'show_row'	   : show_row,
					'heading' 	   : heading,
					'get_period'   : get_period,
					'nature_types' : nature_types,
					'last_months'  : get_last_month,
					'gt_last_name' : gt_last_mname,

					})
				#print '--------',gt_last_mname

			
			bluewater   = models.BlueWater.objects.all().order_by('-id').first()
			# inv_split   = invoice_no.split('/')
			# first_split = str(inv_split[0])+'_'+str(inv_split[1])

			if client_name=='Litasco_Dubai' or client_name=='HELLENIQ ENERGY HOLDINGS S.A.' or client_name=='Litasco':
				do_hide = ''
			else:
				do_hide = 'none'
			
			context={
				'ship_array'   			: ship_array,
				'bluewater'   			: bluewater.tin_number,
				'total_amount' 			: calsx,
				'tt_amt'				: calsx,
				'currency'     			: currency,
				'currency_tag' 			: currency_tag,
				'customer_no'  			: customer_no,
				'tag_show'     			: tag_show,
				'stena_array'  			: stena_array,
				'weco_array'   			: weco_array,
				'ultra_array'  			: ultra_array,
				'hidden'       			: hidden,
				'price_typex'  			: price_types,
				'select_price' 			: select_price,
				'invoice_currency_type' : invoice_currency_type,
				'invoice_nos'  			: mix_invoice_no,
				'status'				: payment_status,
				'other_array'			: other_array,
				'login_user' 			: login_user,	
				'client_list'			: single_array,
				'account_lis'  			: account_lis,		
				'account_l_array' 		: account_l_array,
				'do_hide'				: do_hide,
				'select_price' 			: select_price,
				}

			return render_to_response('invoice_display/edit_invoice_template.html',context)
		else:
			context={
				'ship_array'   			: 0,
				'bluewater'    			: 0,
				'total_amount' 			: 0,
				'currency'     			: 0,
				'currency_tag' 			: '',
				'customer_no'  			: 0,
				'tag_show'	   			: '',
				'stena_array'  			: 0,
				'weco_array'   			: 0,
				'hidden'       			: 0,
				'price_typex'  			: '',
				'select_price' 			: '',
				'invoice_currency_type' : '',
				'invoice_nos'  			: '',
				'status' 				: '',
				'other_array' 			: 0,
				'login_user' 			: 0,
				'client_list' 			: 0,		
				'select_price'			: 0
			}
			return render_to_response("invoice_display/edit_invoice_template.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')


@csrf_exempt
def get_invoice_template(request):
	invoice_no 		= json.loads(request.POST['invoice_no'])[0]
	invoice_details = models.invoice.objects.filter(invoice_no=invoice_no)
	ship_array 		= []
	amount 			= 0
	hide   			= 'none'
	total_amount    = 0
	for x in invoice_details:
		if x.proj_name=='BOSS':
			caption = 'BlueWater Optimum Speed Services (BOSS)'
		elif x.proj_name=='CHM':
			caption = 'Cargo Heating Management Services (CHM)'

		try:
			rate 	 = x.client.rate
			price 	 = x.client.price
			if x.proj_name=='BOSS' and x.usd=='USD' or x.proj_name=='CHM' and x.usd=='USD':
				amount = price
				hide   = 'none'
				currency = x.client.currency_type

			elif x.proj_name=='BOSS' and x.inr=='INR' or x.proj_name=='CHM' and x.inr=='INR':
				amount = (price*rate)
				hide   = ''
				currency = x.client.currency_type
		except:
			rate 	 = 0.0
			price 	 = 0.0
			currency = ''
			amount   = 0.0

		total_amount+=amount

		ship_array.append({
			'ship_name' : x.ship_name,
			'voyage_no' : x.voyage_no,
			'caption' 	: caption,
			'rate' 		: rate,
			'price' 	: price,
			'currency' 	: currency,
			'amount'    : amount,
			'hide'		: hide,
			})
	bluewater   = models.BlueWater.objects.all().order_by('-id').first()
	context={
	'ship_array' : ship_array,
	'bluewater'  : bluewater.tin_number,
	'total_amount' : total_amount,
	'currency'     : currency,
	}

	return HttpResponse(json.dumps(context))

def generator(request):
	if request.user.is_authenticated():
		login_user 	= request.user
		app_url 	= request.path		
		split_url 	= app_url.split('/')
		url_nme 	= split_url[2].capitalize()
			
		context={
			'login_user' : login_user,	
			'app_url'    : app_url,	
		}

		IST 			= pytz.timezone('Asia/Kolkata') 
		datetime_ist 	= datetime.now(IST)		 
		now_date 		= datetime_ist.strftime('%Y-%m-%d %H:%M:%S')
		InID 			= models.log_sessions()
		InID.date  		= now_date 
		InID.user_name  = login_user
		InID.url_name   = url_nme
		InID.save()	
		print '-------',now_date
		return render_to_response("invoice_display/generator.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')



def get_proj_name_list(request):
	if request.user.is_authenticated():
		proj_name   = request.GET['proj_name']
		#print '______>>>>>>>>>>>',proj_name
		client_ship = 0
		boss_ship   = 0
		# if proj_name=='BOSS':
		# 	client_ship    = []
		# 	client_details_boss = models.Client.objects.filter(proj_name='BOSS')


		# elif proj_name=='CHM':
		# 	ship_arr	 = []
		# 	client_arr   = []
		# 	chm_array = models.Client.objects.filter(proj_name='CHM')
		# 	for ch in chm_array:
		# 		if ch.client_name not in ship_arr:
		# 			ship_arr.append(ch.client_name)
		boss_ship = []
		try:
			if proj_name=='CHM':
				chm_arr = []
				cl_details = client_details(proj_name)			
				#chm_array = models.Client.objects.filter(proj_name='CHM')
				for i in cl_details:
					chm_arr.append({
						'client_name' : i['client_name'],
						'proj_name'   : i['proj_name'],
						})

			elif proj_name=='BOSS':
				cl_details = client_details(proj_name)
				for c in cl_details:
					#print '===========',c
				# client_details_boss = models.Client.objects.filter(proj_name='BOSS')
				# for x in client_details_boss:
					boss_ship.append({
						'client_name' : c['client_name'],
						'proj_name'   : c['proj_name'],
						})
		except:
			pass

		if proj_name=='BOSS':
			context={
			'client_name_boss' : boss_ship,
			'client_name_chm'  : 0,
			}
		elif proj_name=='CHM':
			context={
			'client_name_boss' : 0,
			'client_name_chm'  : chm_arr,
			}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def get_pool_list(request):
	if request.user.is_authenticated():
		client_list  = request.GET['client_list']
		proj_name    = request.GET['proj_name']
		#api_url 	 = "https://bossv2.bwesglobal.com/api/get_data_boss/"
		# api_url 	 = "http://0.0.0.0:8004/api/get_data_boss/"
		# api_method   = "GET"			
		# parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'name': client_list}
		# response     = requests.get(api_url, params=parameters,verify=False)		
		# ship_array   = json.loads(response.content)
		# ship_array   = ship_array['sh_array']
		# pool_chm_arr = 0
		# db_array     = []

		# for vv in ship_array:
		# 	if vv['account_name'] not in db_array:
		# 		db_array.append(vv['account_name'])
			
		# for ee in db_array:
		# 	check_array = models.pool_master.objects.filter(client_id='64',pool=ee).count()
		# 	if check_array>0:
		# 		db = models.pool_master.objects.filter(client_id='64',pool=ee).first()
		# 	else:
		# 		db = models.pool_master()
		# 	db.client_id = '64'
		# 	if ee!='':
		# 		db.pool  = ee
		# 		db.save()
		
		if proj_name=='BOSS':
			clientw   	 	 = models.Client.objects.filter(client_name=client_list,proj_name='BOSS').first()
			last_invoice 	 = models.invoice.objects.filter(client_id=clientw.id,proj_name='BOSS').order_by('month').first()
			prev_date 		 = datetime.now()-timedelta(days=30)
			format_prev_date = prev_date.strftime('%m/%d/%Y')		
			try:
				start_date   = last_invoice.disch_date
				end_date  	 = datetime.now()
				start_format = start_date.strftime('%m/%d/%Y')
				end_format   = end_date.strftime('%m/%d/%Y')
			except:
				start_format = format_prev_date
				end_format   = datetime.now().date().strftime('%m/%d/%Y')
			
			client_ship    = []
			pool_boss_arr  = []

			if client_list=='Shell':
				boss_array = models.pool_master.objects.filter(client_id='64',client__proj_name='BOSS')			
			else:
				boss_array = models.pool_master.objects.filter(client__proj_name='BOSS')			

			for sh in boss_array:				
				#if sh.client.proj_name=='BOSS':			
				if sh.client.client_name==client_list:					
					if sh.pool not in pool_boss_arr:
						if sh.pool!='null' and sh.pool!='':						
							pool_boss_arr.append(sh.pool)																		


		elif proj_name=='CHM':
			clientw   	 	 = models.Client.objects.filter(client_name=client_list,proj_name='CHM').first()
			last_invoice 	 = models.invoice.objects.filter(client_id=clientw,proj_name='CHM').order_by('disch_date').first()
			prev_date 		 = datetime.now()-timedelta(days=30)
			format_prev_date = prev_date.strftime('%m/%d/%Y')
			try:
				start_date   = last_invoice.disch_date
				end_date  	 = datetime.now()
				start_format = format_prev_date#'11/01/2020'#start_date.strftime('%m/%d/%Y')
				end_format   = end_date.strftime('%m/%d/%Y')
			except:
				start_format = format_prev_date
				end_format   = datetime.now().date().strftime('%m/%d/%Y')

			pool_chm_arr = []
			chm_array 	 = models.pool_master.objects.all()
			for sh in chm_array:
				try:
					if sh.client.proj_name=='CHM':				
						if sh.client.client_name==client_list:
							if sh.pool not in pool_chm_arr:
								if sh.pool!='null':
									pool_chm_arr.append(sh.pool)
				except:
					pass
	    			
			#for ch in pool_chm_arr:
				#if ch['client_name']==client_list:
					#if ch['pool_name'] not in pool_chm_arr:
				#pool_chm_arr.append(ch)


		if proj_name=='BOSS':
			ship_pool_boss = []
			for x in pool_boss_arr:
				client_details_boss = models.Client.objects.filter(client_name=client_list,proj_name='BOSS').first()
				if client_details_boss:
					client_rate = client_details_boss.rate
					if client_details_boss.proj_name=='BOSS' and client_details_boss.currency_type=='INR':
						proj_name= 'BOSS'
						curr_type = 'INR'
					elif client_details_boss.proj_name=='BOSS' and client_details_boss.currency_type=='USD':
						proj_name= 'BOSS'
						curr_type = 'USD'
				else:
					client_rate = 1.0
				if x!=None:
					ship_pool_boss.append({
						'ship_class'  		: x,
						'client_rate_boss' 	: client_rate,
						'proj_name' 		: proj_name,
						'curr_type' 		: curr_type,
						})

		elif proj_name=='CHM':
			ship_pool_chm = []
			curr_type 	  = ''
			for v in pool_chm_arr:
				client_details_chm = models.Client.objects.filter(client_name=client_list,proj_name='CHM').first()
				if client_details_chm:
					if client_details_chm.proj_name=='CHM' and client_details_chm.currency_type=='INR':
						client_rate = client_details_chm.rate
						proj_name = 'CHM'
						curr_type = 'INR'
					elif client_details_chm.proj_name=='CHM' and client_details_chm.currency_type=='USD':
						client_rate = 1
						proj_name = 'CHM'
						curr_type = 'USD'
				else:
					client_rate = 1.0

				ship_pool_chm.append({
					'pool_name'   		: v,
					'client_rate_chm' 	: client_rate,
					'proj_name' 		: proj_name,
					'curr_type' 		: curr_type,
					})



		if proj_name=='BOSS':		
			context={
			'ship_pool_boss' : ship_pool_boss,
			'ship_pool_chm'  : 0,
			'chm_end_date' 	 : 0,
			'chm_start_date' : 0,
			'boss_date' 	 : str(start_format),		
			}

		if proj_name=='CHM':
			context={
			'ship_pool_boss' : 0,
			'ship_pool_chm'  : ship_pool_chm,
			'chm_end_date' 	 : str(end_format),
			'chm_start_date' : str(start_format),
			'boss_date' 	 : 0,		
			}

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def client_details(proj_name):
	if proj_name=='BOSS':
		client_list = models.Client.objects.filter(proj_name=proj_name,status=1).order_by('client_name')
	elif proj_name=='CHM':
		client_list = models.Client.objects.filter(proj_name=proj_name,status=1).order_by('client_name')
	cl_arr = []
	cl_append  = []
	for cl in client_list:
		if cl.client_name not in cl_append:
			cl_append.append(cl.client_name)

	for c in cl_append:
		cl_arr.append({
		'client_name' : c,
		'proj_name'   : proj_name,
		})

	context={
	'cl_arr' : cl_arr
	}
	return cl_arr

@csrf_exempt
def get_data(request):
	if request.user.is_authenticated():
		name  	   = json.loads(request.POST['client_name'])
		start_date = json.loads(request.POST['start_date'])
		end_date   = json.loads(request.POST['end_date'])
		bill_type  = json.loads(request.POST['bill_type'])
		vessel_typ = json.loads(request.POST['vessel_type'])
		#print("Hello\nWorld!")


		if name!="Reliance" or name!="Clearlake":
			ship_type  = json.loads(request.POST['vessel_type'])
		else:
			ship_type = ""
		proj_name  = json.loads(request.POST['proj_name'])

		chm_array = 0
		try:
			month_name        = datetime.strptime(start_date,"%m/%d/%Y").strftime('%b')
			year_name 		  = datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y')
			month_number      = datetime.strptime(start_date,"%m/%d/%Y").strftime('%m')
			start_date_format = datetime.strptime(start_date,"%m/%d/%Y").strftime('%B')
			start_format 	  = datetime.strptime(start_date,"%m/%d/%Y").strftime('%B')
			get_month 	 	  = monthrange(int(year_name),int(month_number))[1]
			try:
				get_month1 	  = monthrange(int(year_name),int(month_number)-1)[1]
			except:
				get_month1    = 30
			
			try:
				if proj_name=='BOSS':
					start_date_format = str(year_name)+'-'+str(month_number)+'-01'
					end_date_format   = str(year_name)+'-'+str(month_number)+'-'+str(get_month)
					select_month      = start_format
					
				elif proj_name=='CHM':
					start_date_format = datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y-%m-%d')
					end_date_format   = datetime.strptime(end_date,"%m/%d/%Y").strftime('%Y-%m-%d')
					select_month      = ''
					#print '---------',start_date_format,'-----',end_date_format
			except:
				start_date_format = datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y-%m-%d')
				end_date_format   = datetime.strptime(end_date,"%m/%d/%Y").strftime('%Y-%m-%d')
				select_month 	  = ''
		except:
			pass

		#print '---------',start_date_format,'------',end_date_format
		## Fething the data from API	
		clientID  = models.Client.objects.filter(client_name=name,proj_name='BOSS').first()
		try:
			if name == 'TNPGCL':
				get_client_id  = 113
			elif name == 'Reliance':
				get_client_id  = 66
			elif name=='Ultranav':
				get_client_id  = 59
			elif name=='Poompuhar Shipping Corporation Limited':
				get_client_id  = 83
			elif name=='Sakhalin Energy':
				get_client_id  = 120
			elif name=='Central Mare':
				get_client_id  = 121
			elif name=='Dynagas Ltd':
				get_client_id  = 128
			elif name=='Chevron':
				get_client_id  = 17
			elif name=='Clearlake LNG':
				get_client_id  = 136
			elif name=='MMS Tokyo':
				get_client_id  = 131	
			elif name=='Shell LNG':
				get_client_id  = 135		

			else:
				get_client_id  = clientID.id
		except:
			pass		

		if proj_name=='BOSS':			
			get_date 		   = datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y-%m-%d')			
			get_month 		   = datetime.strptime(start_date,"%m/%d/%Y").strftime('%m')				
			api_url 		   = "https://aboss.bwesglobal.com/api/get_ship_to_be_billed/"
			#api_url 		   = "http://0.0.0.0:8004/api/get_data_boss/"
			api_method         = "GET"			
			parameters         = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'client_id': get_client_id,'billing_type':bill_type,'billing_date':(get_date)}
			response           = requests.get(api_url, params=parameters,verify=False)		
			boss_array         = json.loads(response.content)					
			#print '-----------',response
			
			voyage_array_pum   = []
			voyage_array_boss  = []
			voyage_array_apj   = []
			voyage_array_clear = []
			ship_details  	   = []
			whole_details 	   = []	
			single_data 	   = []
			
			route_array 	   = []
			client_det   	   = models.Client.objects.filter(client_name=name,proj_name=proj_name).first()
			pool_lisx 	 	   = models.pool_master.objects.filter(client_id=client_det).first() #,pool=ship_types	
			
			
			if vessel_typ==0:
				all_vessels    = models.merge_billing_day.objects.filter(client_name=name)				
			else:
			 	all_vessels    = models.merge_billing_day.objects.filter(client_name=name,account_tab=vessel_typ)
			 	
			check_all_vessels  = models.merge_billing_day.objects.filter(client_name=name).count()
			

			no_of_day = 0
			dtate 				= get_date
			year_name			= datetime.strptime(str(dtate), "%Y-%m-%d").strftime('%Y')
			month_number        = datetime.strptime(str(dtate), "%Y-%m-%d").strftime('%m')
			day_number          = datetime.strptime(str(dtate), "%Y-%m-%d").strftime('%d')
			month_no 			= int(month_number) #int(month_number)-1
			
			if month_no<10:
				month_str = "0"+str(month_no)
			else:
				month_str = month_no

			start_date  = year_name+'-'+str(month_str)+'-01'		
			get_month   = monthrange(int(year_name),int(month_str))[1]
			amt 		= 0
			#print '---------',get_month1
			for r in all_vessels:
				if bill_type=='monthly_flat':
					try:
						ship_name  = r.ship_name				
						no_of_dayx = r.no_of_day
					except:
						ship_name  = ''
						no_of_dayx = ''

					if r.account_tab:
						acc_tab = r.account_tab
					else:
						acc_tab = ""

					remove_space_vessel = ship_name.replace(' ','_')							
					if no_of_dayx>get_month1:						
					 	no_day= get_month1
					else:
					 	no_day = no_of_dayx
					
					#if no_day>2:
					#	split_price = client_det.price/int(get_month)
						#if no_of_dayx>28:
						#	amt = "{:.2f}".format(client_det.price)
						#else:
					#amt = "{:.2f}".format(int(no_of_dayx)*client_det.price)/28
					amt = round((int(no_of_dayx)*client_det.price)/(get_month1),1)
					# else:
					# 	amt = 0	

					#print '=======',r.ship_name,'----',no_of_dayx,'---',no_day,'---',split_price
					whole_details.append({
						'ship_name'    : ship_name,
						'port_name1'   : r.port_name,
						'port_name2'   : 'Port 2',
						'start_date'   : 'Start3',
						'end_date'	   : str(r.noon_date),	
						'space_vessel' : remove_space_vessel,
						'report_id'    : acc_tab,	
						'vm_name'	   : 'Vm Name5',	
						'billing_days' : (no_day),
						'billing_amt'  : amt,
						'url' 		   : 'URL',
						'account_tab'  : acc_tab,
						'bill_type'    : bill_type,
						'none'		   : 'none'								
					})
			
			v = 0		
			for c in boss_array:
				if get_client_id==113:
					get_cl = 15576
				else:
					get_cl = get_client_id 
				#get_api_data = models.api_client_data.objects.filter(ship_name=c['Ship Name'],client_id=64).first()
				# try:
				# 	acc_tab = get_api_data.account_tab
				# except:
				# 	acc_tab = None	

				# if get_client_id==64:
				# 	report_id = acc_tab					
				# else:
				# 	pass				
				 			
				if bill_type=='voyage_eop':
					url 				= 'https://aboss.bwesglobal.com/vast/monitoringDashboard/?voy_id='+str(c['voyage_id'])
					join_port 			= str(c['First Port'])+'-'+str(c['Last Port'])
					try:
						get_price 		= models.cost_per_route.objects.filter(client_id_id=get_cl,route__icontains=join_port).first()
						get_cost 		= get_price.cost
					except:
						get_price       = ""
						get_cost 		= ""
					#print '---------',join_port,'----',get_cost			
					remove_space_vessel = c['Ship Name'].replace(' ','_')
					whole_details.append({
						'ship_name'    : c['Ship Name'],
						'port_name1'   : c['First Port'],
						'port_name2'   : c['Last Port'],
						'start_date'   : '',
						'end_date'	   : '',	
						'space_vessel' : remove_space_vessel,
						'report_id'    : c['voyage_id'],	
						'vm_name'	   : '',	
						'billing_days' : '',	
						'billing_amt'  : get_cost, #c['billing_amt'],	
						'url' 		   : '',
						'account_tab'  : url,
						'bill_type'    : bill_type,						
					})

				if bill_type=='monthly_prorated':
					url = 'https://aboss.bwesglobal.com/vast/monitoringDashboard/?voy_id='+str(c['voyage_id'])	
					remove_space_vessel = c['Ship Name'].replace(' ','_')
					#if c['No. of Days']!=1:           
						
					start_datex = datetime.strptime(str(c['Start Date']),"%d %b %Y").strftime('%Y-%m-%d')	
					end_datex 	= datetime.strptime(str(c['End Date']),"%d %b %Y").strftime('%Y-%m-%d')							
						
					whole_details.append({
						'ship_name'    : c['Ship Name'],
						'port_name1'   : c['First Port'],
						'port_name2'   : c['Last Port'],
						'start_date'   : str(c['Start Date']),
						'end_date'	   : str(c['End Date']),
						'space_vessel' : remove_space_vessel,
						'report_id'    : c['voyage_id'],
						'vm_name'	   : '',
						'billing_days' : c['No. of Days'],
						'billing_amt'  : '', #c['billing_amt'],
						'url' 		   : url,
						'account_tab'  : '',
						'bill_type'    : bill_type,
					})

		elif proj_name=='CHM':
			#start_date_formatx = '2022-01-01'
			#end_date_formatx = '2022-01-31'	
			#api_url 	    = "http://0.0.0.0:8003/hb/get_chm_data/"
			api_url 	    = "https://chm.bwesglobal.com/hb/get_chm_data/"
			api_method      = "GET"
			parameters      = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'name': name,'ship_type':ship_type,'start_date':str(start_date_format),'end_date': str(end_date_format)}
			#parameters      = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'name': name,'ship_type':ship_type,'start_date':str(start_date_format)}
			response        = requests.get(api_url, params=parameters,verify=False)
			ch_array        = json.loads(response.content)
			ch_array        = ch_array['finance_array']
			
			chm_array       = []
			s_no 		    = 1
			ship_name       = 0
			voyage_no       = 0
			disch_port      = 0
			disch_date      = 0
			vm_name 	    = 0
			voyage_id       = 0
			s_no            = 0
			address 	    = 0
			color           = 0
			href            = 0
			active          = 0
			clientid        = 0
			alert_ship_name = ''
			#print '----------',	ship_type		
			#models.generate_dsr.objects.filter(client_name=name).delete()
			f_invoice_no 		= models.financial_invoice_no.objects.all().order_by('-id').first()
			get_fin_invoice_no  = f_invoice_no.fin_invoice_no
			
			for t in ch_array:
				try:
					_dht_date 		= t['last_dht_date'][:10]
					last_dht_date 	= datetime.strptime(_dht_date, "%Y-%m-%d").strftime('%d-%b-%Y')
				except:
					last_dht_date   = ''
				#print '-----------',t['vm_name'],'----',t['ship_name'],'----',t['voyage_no']
				
				if t['finance_date']>=start_date_format and t['finance_date']<=end_date_format:
				#if last_dht_date>=start_date_format and last_dht_date<=end_date_format:
					clientx   	 = models.Client.objects.filter(client_name=name,proj_name='CHM').first()
					pool_lisx 	 = models.pool_master.objects.filter(client_id=clientx.id,pool=ship_type).first()			
					ship_details = models.Ship.objects.filter(ship_name=t['ship_name']).first()
					#print '-------',ship_type
					try:
						missing_ship  = ship_details.ship_name
						missing_color = 'black'
					except:
						missing_ship  = t['ship_name']
						missing_color = 'black' #
					
					if t['account_tab']!=None:
						account_slab = t['account_tab']
					else:
						account_slab = ''

					if ship_type!='0':
						# print '0909090909090-0---'						
						if t['pool_namex']!=pool_lisx.pool:
							remove_space_vessel = t['ship_name'].replace(' ', '_')
							ship_name  = t['ship_name']
							voyage_no  = t['voyage_no']
							disch_port = t['disch_port']
							try:
								disch_date = datetime.strptime(t['finance_date'], "%Y-%m-%d").strftime('%d-%b-%Y') #t['disch_date']
							except:
								disch_date = ''
								
							vm_name    = t['vm_name']
							voyage_id  = t['voyage_id']					
							s_no 	   = s_no
							address    = t['account_address'] #pool_lisx.address #ship_details.address
							color 	   = ''
							href 	   = '#'
							active 	   = 'style="pointer-events: none;cursor: default;"'
							clientid   = clientx.id
							accoun_tab = account_slab
							
							try:
								format_fin_date = datetime.strptime(t['finance_date'], "%Y-%m-%d").strftime('%d-%b-%Y')
							except:
								format_fin_date = ''

							try:
								format_disch_date = datetime.strptime(t['disch_dates'], "%Y-%m-%d").strftime('%d-%b-%Y')
							except:
								format_disch_date = ''

							#print '------------',t['ship_name'],'----',t['voyage_no']

							try:
								check_cancel     = models.invoice.objects.filter(ship_name=t['ship_name'],voyage_no=t['voyage_no'],payment_status='Cancel',cancel_invoice='1',vessel_type=ship_type).first()
								cancel_vessel    = check_cancel.ship_name
								cancel_voyage_no = check_cancel.voyage_no
								cancelo 		 = check_cancel.cancel_invoice
							except:
								cancel_vessel    = ''
								cancel_voyage_no = ''
								cancelo  		 = '0'

					
							try:
								if t['ref_name']!=None:
									other_book_name  = t['ref_name']
								else:
									other_book_name  = ''
							except:
								other_book_name  = ''
							#print '--------yeh toh hoga shayad',t['ref_name']

							try:
								edit_reasons 	= 	t['edit_reasons']
							except:
								edit_reasons 	= 	''


							# db 				 = models.generate_dsr()
							# db.ship_name 		 = t['ship_name']
							# db.voyage_no 		 = t['voyage_no']
							# db.vm_name 		 = t['vm_name']
							# db.discharge_port  = t['disch_port']
							# db.discharge_eta 	 = str(t['finance_date'])
							# db.client_name 	 = name
							# db.proj_name		 = 'CHM'
							# db.voyage_id		 = t['voyage_id']
							# db.save()
							

							chm_array.append({
								'ship_name'       : t['ship_name'],
								'voyage_no'       : t['voyage_no'],
								'disch_port'      : t['disch_port'],
								#'disch_date'      : str(disch_date),#t['disch_date'],
								'vm_name' 	      : t['vm_name'],
								'client_id'       : clientx.id,
								'voyage_id'       : t['voyage_id'],
								's_no' 		      : s_no,
								'alert_color'     : color,
								'alert_ship_name' : alert_ship_name,
								'alert_href' 	  : href,
								'alert_active'    : active,
								'disch_date'	  : format_disch_date, #format_fin_date,
								'missing_ship'    : missing_ship,
								'missing_color'   : missing_color,
								'mix_vessel'	  : remove_space_vessel,
								'cancel_vessel'   : cancel_vessel,
								'cancel_voyage_no': cancel_voyage_no,
								'cancelo'  		  : cancelo,
								'account_slab'    : accoun_tab,
								'format_fin_date' : format_fin_date,
								'other_book_name' : other_book_name,
								'edit_reasons'	  : edit_reasons,
								'last_dht_date'   : last_dht_date,
								
								})
							s_no+=1
						else:
							#print '-- yaha hai kya ?'
							if t['account_tab']!=None:
								account_slab = t['account_tab']
							else:
								account_slab = ''

							clien_x    = models.Client.objects.filter(client_name=name,proj_name='CHM').first()
							pool_lisx  = models.pool_master.objects.filter(client_id=clien_x.id).first()
							if t['client_name']==name:
								ship_details = models.Ship.objects.filter(ship_name=t['ship_name']).first()
								try:
									missing_ship  = ship_details.ship_name
									missing_color = 'black'
								except:
									missing_ship  = t['ship_name']
									missing_color = 'black'

								remove_space_vessel = t['ship_name'].replace(' ', '_')
								ship_name           = t['ship_name']
								voyage_no           = t['voyage_no']
								disch_port          = t['disch_port']
								try:
									disch_date = datetime.strptime(t['finance_date'], "%Y-%m-%d").strftime('%d-%b-%Y') #t['disch_date']
								except:
									disch_date = ''

								try:
									format_disch_date = datetime.strptime(t['disch_dates'], "%Y-%m-%d").strftime('%d-%b-%Y')
								except:
									format_disch_date = ''

								#disch_date          = t['disch_date']
								vm_name             = t['vm_name'],
								voyage_id           = t['voyage_id']
								s_no 	            = s_no
								address             = t['account_address'] #pool_lisx.address
								color 	            = ''
								href 	            = '#'
								active 	            = 'style="pointer-events: none;cursor: default;"'
								clientid            = clientx.id


								try:
									format_fin_date = datetime.strptime(t['finance_date'], "%Y-%m-%d").strftime('%d-%b-%Y')
								except:
									format_fin_date = ''


								try:
									check_cancel     = models.invoice.objects.filter(ship_name=t['ship_name'],voyage_no=t['voyage_no'],payment_status='Cancel',cancel_invoice='1').first()
									cancel_vessel    = check_cancel.ship_name
									cancel_voyage_no = check_cancel.voyage_no
									cancelo 		 = check_cancel.cancel_invoice
								except:
									cancel_vessel    = ''
									cancel_voyage_no = ''
									cancelo  		 = '0'

								db 					 = models.generate_dsr()
								db.ship_name 		 = t['ship_name']
								db.voyage_no 		 = t['voyage_no']
								db.vm_name 			 = t['vm_name']
								db.discharge_port 	 = t['disch_port']
								db.discharge_eta 	 = t['finance_date']
								db.client_name 		 = name
								db.proj_name		 = 'CHM'
								db.voyage_id		 = t['voyage_id']								
								db.save()

								try:
									other_book_name  = t['ref_name']
								except:
									other_book_name  = ''

								#print '========<<<<',t['ref_name']
								try:
									edit_reasons 	= 	t['edit_reasons']
								except:
									edit_reasons 	= 	''

								try:
									_dht_date 		= t['last_dht_date'][:10]	
									last_dht_date 	= datetime.strptime(_dht_date, "%Y-%m-%d").strftime('%d-%b-%Y')
								except:
									last_dht_date   = ''




								chm_array.append({
									'ship_name'       : t['ship_name'],
									'voyage_no'       : t['voyage_no'],
									'disch_port'      : t['disch_port'],
									#'disch_date'      : disch_date,  #t['disch_date'],
									'vm_name' 	      : t['vm_name'],
									'client_id'       : clientx.id,
									'voyage_id'       : t['voyage_id'],
									's_no' 		      : s_no,
									'alert_color'     : color,
									'alert_ship_name' : alert_ship_name,
									'alert_href' 	  : href,
									'alert_active'    : active,
									'disch_date'	  : format_disch_date,#format_fin_date,
									'cancel_vessel'   : cancel_vessel,
									'cancel_voyage_no': cancel_voyage_no,
									'cancelo'  		  : cancelo,
									'missing_ship'    : missing_ship,
									'missing_color'   : missing_color,
									'mix_vessel'	  : remove_space_vessel,
									'account_slab'    : account_slab,
									'format_fin_date' : format_fin_date,
									'other_book_name' : other_book_name,
									'edit_reasons'	  : edit_reasons,
									'last_dht_date'   : last_dht_date,
									})
								s_no+=1

		
		if proj_name=='BOSS':
			context={
			'ship_details'       : ship_details,
			'chm_array'          : 0,			
			'whole_details'      : whole_details,
			'check_all_vessels'	 : check_all_vessels
			}
		elif proj_name=='CHM':
			context={
			'ship_details' 		 : 0,
			'chm_array'    		 : chm_array,			
			'whole_details'		 : 0,
			}
		#print '--------',ship_details	

		return HttpResponse(json.dumps(context))
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')

@csrf_exempt
def vaild_apeejay_invoice_details(request):
	if request.user.is_authenticated():
		ship_name  			= json.loads(request.POST['vessel_name'])
		start_dtt    		= json.loads(request.POST['start_dtt'])	
		format_month_name   = datetime.strptime(start_dtt, "%m/%d/%Y").strftime('%B')
		format_year_name    = datetime.strptime(start_dtt, "%m/%d/%Y").strftime('%Y')
		client_name  		= json.loads(request.POST['client_name'])
		remove_vessel_space = ship_name.replace('_', ' ')		 	
		client_details 		= models.Client.objects.filter(client_name=client_name,proj_name='BOSS').first()
		vessel_name 		= remove_vessel_space.strip()
		
		try:
			qry    = "SELECT * FROM it_invoice where proj_name='BOSS' and month_name='"+str(format_month_name)+"' and ship_name='"+str(vessel_name)+"' and cancel_invoice="'0'" and Year(month)='"+str(format_year_name)+"'"
			#print qry
			cursor = connection.cursor()
			cursor.execute(qry)
			invoice_details = cursor.fetchall()
			for x in invoice_details:
				if x>0:
					display_button = 'none'
					shipname       = ship_name
				else:
					display_button = ''
					shipname       = ship_name

			context={
			'display_button' : display_button,
			'shipname'   	 : shipname,		
			}			
		except:
			context={
			'display_button' : '',
			'shipname'   	 : '',
			}


		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')



@csrf_exempt
def vaild_poompuhar_invoice_details(request):
	if request.user.is_authenticated():
		ship_name 			= json.loads(request.POST['ship_name'])
	 	client_name 		= json.loads(request.POST['client_name'])
		voyage_id  			= json.loads(request.POST['voyage_id'])
		start_dtt  			= json.loads(request.POST['start_dtt'])	
		format_month_name   = datetime.strptime(start_dtt, "%m/%d/%Y").strftime('%B')
		format_year_name    = datetime.strptime(start_dtt, "%m/%d/%Y").strftime('%Y')
		remove_vessel_space = ship_name.replace('_', ' ')		 	
		client_details 		= models.Client.objects.filter(client_name=client_name,proj_name='BOSS').first()
		vessel_name 		= remove_vessel_space.strip()
		show 				= ''

		# qry    = "SELECT ship_name FROM it_invoice where proj_name='BOSS' and month_name='"+str(format_month_name)+"' and ship_name='"+str(vessel_name)+"' and voyage_no='"+str(voyage_id)+"' and cancel_invoice="'0'" and Year(month)='"+str(format_year_name)+"';"
		# cursor = connection.cursor()
		# cursor.execute(qry)
		# valid_details = cursor.fetchall()	
		
		# for x in valid_details:		
		# 	if x>0:
		# 		msg = 'yes'
		# 		ship_name  = x[0]
		# 		show = ''
		# 	else:
		# 		msg = 'no'
		# 		show = ''
		# 		ship_name = x[0]		
		 		
		# context={
		# 	'msg' : msg,
		# 	'show' : show,	
		# 	'shipname' : ship_name
		# }
		start_date_for = ''
		display_button = ''
		shipname 	   = ''
		qry    = "SELECT voyage_no FROM it_invoice where proj_name='BOSS' and month_name='"+str(format_month_name)+"' and ship_name='"+str(vessel_name)+"' and voyage_no='"+str(voyage_id)+"' and cancel_invoice="'0'" and Year(month)='"+str(format_year_name)+"';"
		
		cursor = connection.cursor()
		cursor.execute(qry)
		invoice_details = cursor.fetchall()
		for x in invoice_details:
			if x>0:
				display_button = 'none'
				shipname       = x[0]
			else:
				display_button = ''
				shipname       = x[0]
		
		context={
			'display_button' : display_button,
			'shipname'   	 : shipname,
		}	
		# except:
		# 	context={
		# 	'display_button' : '',
		# 	'shipname'   	 : '',
		# }
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')
	
@csrf_exempt
def update_invoice_template(request):
	invoice_no      = json.loads(request.POST['invoice_no'])[0]
	invoice_details = json.loads(request.POST['invoice_details'])
	modify_qty		= json.loads(request.POST['modify_qty'])
	tot_amt 		= json.loads(request.POST['total_amount'])
	modi_rate       = json.loads(request.POST['modify_rate'])
	modi_price      = json.loads(request.POST['modify_price'])	
	url_client_name = json.loads(request.POST['url_client_name'])[0]
	for_checking    = request.POST['for_checking']
	invoiceID       = json.loads(request.POST['id'])[0]
	change_dollar   = json.loads(request.POST['change_dollar'])
	flag_client 	= json.loads(request.POST['flag_client'])

	fot_set 		= json.loads(request.POST['font_set'])
	add_w 			= json.loads(request.POST['add_rw'])

	get_period      = json.loads(request.POST['get_period'])
	acc_name 		= json.loads(request.POST['acc_name'])
	get_page		= json.loads(request.POST['get_page'])
	gflat 			= request.POST['flag']
	layout 			= json.loads(request.POST['layout'])
	ntype 			= json.loads(request.POST['ntype'])
	#print '------------',invoice_no
	

	if fot_set!='' or fot_set!=0 or fot_set!='0':
		font_set = fot_set
	else:
		font_set = '14px'

	if add_w!='' or add_w!=0 or add_w!='0':
		add_line = add_w
	else:
		add_line = 10



	unpaid 			= request.POST['unpaid']
	customer_no     = request.POST['customer_no']
	remarks 		= request.POST['remarks']
	edit_invoice_no = request.POST['edit_invoice_no']
	proj_name 		= request.POST['proj_name']
	client_address  = request.POST['address']
	cancel_invoice  = request.POST['cancel_invoice']
	client_name 	= url_client_name.strip()	
	get_price_inv   = json.loads(request.POST['get_price'])
	net_price		= json.loads(request.POST['net_price'])

	customer_no 	= request.POST['customer_no']
	invoice_date 	= request.POST['invoice_date']
	currency 		= request.POST['currency']
	edit_vm_name    = request.POST['edit_vm_name']
	count_row 		= request.POST['rowCount']
	total_row_table = int(count_row)-2

	split_address1 = ''
	split_address2 = ''
	split_address3 = ''
	split_address4 = ''
	split_address5 = ''
	vm_name_editor = request.POST['edit_vm_name']
	#print '-----',currency
	
	# try:
	# 	modify_invoice_no  = models.invoice.objects.filter(id=invoiceID).first()
	# 	modify_invoice_no.invoice_no = str(edit_invoice_no)
	# 	modify_invoice_no.save()
	# 	print '=============',invoiceID,'======',edit_invoice_no
	# except:
	# 	pass
	#################################### for new row #############################################
	
	if for_checking=='25':
		check_invoice = models.invoice.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client__currency_type=currency).first()
		_new_row  = models.invoice()	
		for n in invoice_details:
			check = models.invoice.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client__currency_type=currency,ship_name=n['Description']).count()	
			
			if check!=0:
				print ''
			else:				
				_new_row.ship_name  	= n['Description']		
				_new_row.proj_name  	= proj_name
				_new_row.usd 	    	= currency
				_new_row.invoice_no 	= invoice_no
				_new_row.client_address = client_address
				_new_row.month 			= check_invoice.month
				_new_row.url 			= check_invoice.url
				_new_row.vessel_type    = check_invoice.vessel_type
				_new_row.client_id 		= check_invoice.client_id
				_new_row.month_name 	= check_invoice.month_name
				_new_row.vm_name 		= check_invoice.vm_name
				if currency=='USD':
					_new_row.rate = 1.0
				else:
					_new_row.rate = check_invoice.rate #n['total_cost']
				#_new_row.price 	  = check_invoice.price #str(n['unit_cost'])

				_new_row.save()				
	else:
		pass

	##############################################################################################

	status = 'paid'
	try:
		price_type 	= request.GET['price_type']
	except:
		price_type  = None

	try:
		select_type = models.Client.objects.filter(client_name=client_name,proj_name=proj_name,price=price_type).first()
	except:
		pass

	client_details 	= models.Client.objects.filter(client_name=url_client_name,proj_name=proj_name,currency_type=currency).first()
	chekc 			= models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_details,proj_name=proj_name).first()
	print '--------',client_details
	if chekc.client.proj_name=='BOSS':
		b_tin_number = customer_no
		clientID 	 = chekc.client.id
	elif chekc.client.proj_name=='CHM':
		b_tin_number = customer_no
		clientID     = chekc.client.id
	update_tin_num 	 			 = models.Client.objects.filter(id=clientID).first()
	update_tin_num.tin_number 	 = b_tin_number
	update_tin_num.change_dollar = change_dollar
	update_tin_num.save()
	
	if unpaid=='1':
		cancel_paid_details   = models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_details,proj_name=proj_name)
		t=0
		for cl in cancel_paid_details:
			vc = models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_details,proj_name=proj_name,ship_name=invoice_details[t]['Description']).first()
			#print '--------',invoice_details[t]['unit_cost']
			cl.invoice_amount = None
			cl.received_date  = None
			cl.payment_status = None
			cl.tds 		      = None
			cl.received_inr   = None
			cl.vm_name 		  = edit_vm_name
			cl.remark 		  = remarks
			cl.invoice_no 	  = edit_invoice_no			
			cl.rate 		  = modi_rate			
			cl.price 		  = invoice_details[t]['unit_cost'] #modi_price
			cl.client_flag 	  = flag_client
			cl.client_address = client_address
			cl.ship_name 	  = invoice_details[t]['Description']
			cl.heading 		  = invoice_details[t]['headings']
			try:
				cl.nature_type = ntype
			except:
				cl.nature_type = "Data base, data processing charges"

			if acc_name=="0":
				print ''
			else:
				cl.vessel_type    = acc_name
				cl.account_type   = acc_name

			if cancel_invoice=="1":
				cl.cancel_invoice = cancel_invoice
				cl.payment_status = 'Cancel'
			else:
				cl.cancel_invoice = 0
				cl.payment_status = None

			# try:
			# 	if gflat=='on':
			# 		cl.qty    = modify_qty
			# 	else:
			# 		print ''
			# except:
			# 	pass
			

			cl.invoice_date   = str(invoice_date)
			if currency=='INR':
				cl.inr = 'INR'
				cl.usd = None
			else:
				cl.inr = None
				cl.usd = 'USD'


			#print '----------',modify_qty
			cl.save()
			t+=1
			
	else:
		#print '_______unpaid zero'
		pass
		# if unpaid=='0':
		# 	cancel_paid_details  = models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_details)
		# 	for p in cancel_paid_details:
		# 		update_invoice 				  = models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_details).first()
		# 		igst 		   				  = ((tot_amt*18)/100)
		# 		tds  		   				  = p.tds
		# 		net_amt 	   				  = ((tot_amt+igst)-tds)
		# 		update_invoice.invoice_amount = net_amt
		# 		update_invoice.received_date  = p.received_date
		# 		update_invoice.payment_status = p.payment_status
		# 		update_invoice.save()
	UpDates				= models.invoice.objects.filter(invoice_no=edit_invoice_no).first()
	split_m 			= UpDates.month.split('-')
	
	qry11   = "SELECT sum(price*rate*qty) FROM invoice.it_invoice where invoice_no='"+str(edit_invoice_no)+"'"	
	cursor 	= connection.cursor()
	cursor.execute(qry11)
	invoice_details2 = cursor.fetchall()	
	usd_amts = invoice_details2[0][0]/int(split_m[2])
	UpDates	= models.invoice.objects.filter(invoice_no=edit_invoice_no)
	for v in UpDates:
		v.usd_amount = usd_amts
		v.save()

	# print '------',c.price,'---',c.qty,'-----',c.rate,'-----',(split_m[2]),'----',usd_amts,'---',edit_invoice_no
	# #usd_amtx 			= models.invoice.objects.filter(invoice_no=invoice_no,proj_name=proj_name).aggregate(Sum('total_amount'))	
	# #tot_amts 			= usd_amtx['total_amount__sum']	
	# UpDates.usd_amount  = round(usd_amts,0)
	# UpDates.save()


	latest_invoice_date = datetime.strptime(invoice_date, "%Y-%m-%d").strftime('%d-%b-%Y')
	sums = 0
	split_address6 = ''

	for x in invoice_details:
		amount = 0
		if x['Description']!='Add':

			try:
				if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
					amount = float(x['unit_cost'])*float(x['total_cost'])*int(x['qty'])
				else:
					pass
			except:
				if proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
					amount = float(x['unit_cost'])*int(x['qty'])
				else:
					pass

			try:
				save_invoice  = models.invoice.objects.filter(invoice_no=invoice_no,ship_name=x['Description'],client_id=client_details,proj_name=proj_name).first()
		 		save_invoice.client_address = client_address
		 	except:
		 		pass


		 	


	 		#paid_invoice  = models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_details,payment_status='Paid').count()
	 		try:
		 		if cancel_invoice=='1':
					save_invoice.cancel_invoice = cancel_invoice
					save_invoice.payment_status = 'Cancel'
					save_invoice.invoice_amount = None
					save_invoice.received_date  = None
					save_invoice.tds 		    = None
					save_invoice.ship_name      = x['Description'].strip()
					save_invoice.amount 		= amount
					msg = 'cancel'
		 		elif cancel_invoice=='0':
					save_invoice.cancel_invoice = cancel_invoice
					save_invoice.payment_status = None
					msg = 'change_cancel'

		 		save_invoice.invoice_date       = invoice_date
		 		save_invoice.ship_name          = x['Description'].strip()
		 		# save_invoice.vm_name 		    = edit_vm_name
		 		save_invoice.amount 		    = amount
		 		save_invoice.price 			    = check_invoice.price #x['unit_cost']
		 		save_invoice.rate 			    = check_invoice.rate #x['total_cost']
		 		save_invoice.qty 			    = check_invoice.qty #x['qty']
		 		#save_invoice.remark 		    = remarks
		 		save_invoice.invoice_no 	 	= edit_invoice_no
		 		##print '------------',remarks

		 		try:
		 			save_invoice.price_type  = select_type.price_type
		 		except:
		 			save_invoice.price_type  = None
		 		save_invoice.save()

		 		sums+=amount

		 	except:
		 		pass

	if proj_name=='BOSS' and currency=='INR' or proj_name=='CHM' and currency=='INR':
		total_amount   		= tot_amt
		taxable_amount 		= (total_amount*18)/100
		net_taxable_amount 	= (taxable_amount+total_amount)

	if proj_name=='BOSS' and currency=='USD' or proj_name=='CHM' and currency=='USD':
		total_amount   		= tot_amt
		taxable_amount 		= (total_amount)
		net_taxable_amount 	= (taxable_amount+total_amount)

	calling_pdf  = models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_details)
	#print '---------',calling_pdf

	try:
		clientaddress  = client_address.split(',')
		split_address1 = clientaddress[0]
		split_address2 = clientaddress[1]
		split_address3 = clientaddress[2]
		split_address4 = clientaddress[3]
		split_address5 = clientaddress[4]
	except:
		split_address1 = split_address1
		split_address2 = split_address2
		split_address3 = split_address3
		split_address4 = split_address4
		split_address5 = split_address5
	

	if client_name!='Adhart' or client_name!='Adhart Shipping Pte. Ltd':
		if proj_name=='BOSS':
			gt_date = vc.month.split('-')
			
			split_month = gt_date[2]
			
			

			# if client_name=='Shell' or client_name=='Shell NWE':
			# 	if total_row_table<10:
			# 		# phele get_create_pdf_client_name tha
			# 		print '-----1'
			# 		arr  = get_create_pdf(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'BOSS','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5)	
			# 	else:
			# 		print '-----2'
			# 		arr  = get_create_pdf(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'BOSS','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5)	

			# 		#invoice_array = models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_details,proj_name=proj_name)
			# 		#sh.get_calling_for_excel(client_name,invoice_array,invoice_no,12,total_row_table)						
				
			# elif client_name=='Clearlake':
			# 	arr  = get_create_pdf(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'BOSS','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5)					
			#  	#ct.get_calling_for_excel(client_name,calling_pdf,invoice_no,12,total_row_table)
			# elif client_name=='Ultranav':       				
			#  	#dt.get_calling_for_excel_default(client_name,calling_pdf,invoice_no,12,total_row_table)
			# 	arr  = get_create_pdf(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'BOSS','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5)
			# #elif client_name=='Oldendorff':
			# #	otp.get_calling_for_excel_otp(client_name,calling_pdf,invoice_no,12,total_row_table)
			# else:
			if client_name=='Poompuhar Shipping Corporation Limited' or client_name=='TNPGCL':
				#print '-->>',client_name
				arr  = get_create_pdf_client_name(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'BOSS','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,font_set,add_line,get_period,get_page)
			else:
				arr  = get_create_pdf(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'BOSS','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,font_set,add_line,get_period,get_page,layout,split_month,ntype)

		elif proj_name=='CHM':
			gt_date = vc.month.split('-')			
			split_month = gt_date[2]

			if client_name=='Shell' or client_name=='Shell NWE':
				if edit_invoice_no:					
					arr  = get_create_pdf(calling_pdf,client_name,0,edit_invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'CHM','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,font_set,add_line,get_period,get_page,layout,split_month,ntype)					
				else:
					print '-----4'

					# phele get_create_pdf_client_name tha
					arr  = get_create_pdf(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'CHM','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,font_set,add_line,get_period,get_page,layout,0,split_month,ntype)					
			else:
				if edit_invoice_no:
					arr  = get_create_pdf(calling_pdf,client_name,0,edit_invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'CHM','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,font_set,add_line,get_period,get_page,layout,split_month,ntype)					
				else:
					arr  = get_create_pdf(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'CHM','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,font_set,add_line,get_period,get_page,layout,0,split_month,ntype)				
	else:
		for r in invoice_details:			
			try:
				v  = models.invoice.objects.filter(ship_name=r['Description'],client_id=client_details,proj_name=proj_name,id=r['invoiceID']).first()			
			 	v.price = r['unit_cost']		 	
				v.save()	
			except:
				pass	
		
		invoice_array = models.invoice.objects.filter(invoice_no=invoice_no,client_id=client_details,proj_name=proj_name)
		if client_name=='Poompuhar Shipping Corporation Limited' or client_name=='TNPGCL':
			#apj.get_calling_for_excel(client_name,invoice_array,invoice_no,12,total_row_table)
			arr  = get_create_pdf_client_name(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'BOSS','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,font_set,add_line,get_period,get_page,split_month,ntype)					
		else:

		#if client_name=='Shell':			
			#ct.get_calling_for_excel(client_name,invoice_array,invoice_no,12)
			arr  = get_create_pdf(calling_pdf,client_name,0,invoice_no,0,0,split_address1,split_address2,0,latest_invoice_date,customer_no,'BOSS','0','edit',currency,total_amount,taxable_amount,net_taxable_amount,split_address3,split_address4,split_address5,font_set,add_line,get_period,get_page,layout,split_month,ntype)					

	if unpaid=='1' and cancel_invoice=='1':
		msg = 'both'
	elif unpaid=='1' and cancel_invoice=='0':
		msg = 'pending'
	else:
		pass

	total_details   = models.invoice.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client_id=client_details).aggregate(Sum('price'))
	counter         = models.invoice.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client_id=client_details).count()	
	details_invoice = models.invoice.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client_id=client_details)
	e=0
	for c in details_invoice:		
		up_amount 		= c.price*c.rate #invoice_details[e]['unit_cost']

		c.total_amount 	= up_amount #net_price#total_details['price__sum']
		c.save()
		e+=1

	login_user 	    = request.user	
	app_url 		= request.path		
	split_url 		= app_url.split('/')
	url_nme 		= split_url[2].capitalize()
	IST 			= pytz.timezone('Asia/Kolkata') 
	datetime_ist 	= datetime.now(IST)		 
	now_date 		= datetime_ist.strftime('%Y-%m-%d %H:%M:%S')
	InID 			= models.log_sessions()
	InID.date  		= now_date 
	InID.user_name  = login_user
	InID.url_name   = "Update Invoice"
	InID.invoice_no = invoice_no
	InID.status     = "Only updated"
	InID.save()	

	context={
	'msg' : msg,	
	}

	return HttpResponse(json.dumps(context))

def delete_invoice_template(request):
	invoice_no 	   	= json.loads(request.GET['invoice_no'])[0]
	del_ship_name   = request.GET['delete_invoice']
	invoiceID 	   	= request.GET['invoiceID']
	proj_name  	   	= request.GET['proj_name']
	client_name    	= request.GET['client_name']
	currency_type   = request.GET['currency_type']	
	
	try:
		models.invoice.objects.filter(invoice_no=invoice_no,ship_name=del_ship_name).delete()
	except:
		pass

	del_details  = models.invoice.objects.filter(invoice_no=invoice_no,id=invoiceID).first()	
	clientID     = models.Client.objects.filter(client_name=client_name,proj_name=proj_name,currency_type=currency_type).first()	
	check_vessel = models.delete_vessel_details.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client_id=clientID,currency_type=currency_type,ship_name=del_ship_name).count()
	
	if check_vessel!=0:
		deleted_invoice = models.delete_vessel_details.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client_id=clientID,currency_type=currency_type,ship_name=del_ship_name).first()
		msg 		  = 'no'
		deleted_date  = deleted_invoice.delete_date.strftime("%d/%b/%Y")
		invoice_datex = deleted_invoice.invoice_date.strftime("%d/%b/%Y")
	else:
		deleted_invoice = models.delete_vessel_details()
		msg 		  = 'done'	
		deleted_date  = ''
		invoice_datex = ''

	deleted_invoice.invoice_no    = invoice_no
	deleted_invoice.invoice_date  = del_details.invoice_date
	deleted_invoice.delete_date   = datetime.now().date()
	deleted_invoice.ship_name     = del_ship_name
	deleted_invoice.client_id     = clientID
	deleted_invoice.proj_name     = proj_name
	deleted_invoice.currency_type = currency_type	
	deleted_invoice.price         = del_details.price	
	deleted_invoice.save()	
	del_invoice_date 			  = deleted_date
	gen_invoice_date 			  = invoice_datex

	total_details 	= models.invoice.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client_id=clientID).aggregate(Sum('price'))
	counter       	= models.invoice.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client_id=clientID).count()
	
	details_invoice = models.invoice.objects.filter(invoice_no=invoice_no,proj_name=proj_name,client_id=clientID)
	for c in details_invoice:
		c.total_amount = total_details['price__sum']
		c.save()
	
	context={
	'deleted_date' 		: str(del_invoice_date),
	'gen_invoice_date' 	: str(gen_invoice_date),
	'msg' 		   		: msg
	}

	return HttpResponse(json.dumps(context))


def convert_money_to_text(money):
    try:
        money_number = int(money)
    except ValueError:
        return "You must enter Number"
    if money_number == 0:
        return None
    positions 		= [None for i in range(4)]
    key_range 		= 0
    one_place 		= ["", "One ", "Two ", "Three ", "Four ","Five ", "Six ", "Seven ", "Eight ", "Nine "]
    one_ten_place   = ["Ten ", "Eleven ", "Twelve ", "Thirteen ", "Fourteen ","Fifteen ", "Sixteen ", "Seventeen ", "Eighteen ","Nineteen "]
    ten_place 		= ["Twenty ", "Thirty ", "Forty ", "Fifty ","Sixty ", "Seventy ", "Eighty ", "Ninety "]
    name_of_number  = ["Thousand ", "Lakh ", "Crore "]
    money_number_money_text = ''
    positions[0] = money_number % 1000  # units
    positions[1] = money_number / 1000
    positions[2] = money_number / 100000
    positions[1] = positions[1] - 100 * positions[2]  # thousands
    positions[3] = money_number / 10000000  # crores
    positions[2] = positions[2] - 100 * positions[3]  # lakhs
    for counter in range(3, 0, -1):
        if positions[counter] != 0:
            key_range = counter
            break
    for i in range(key_range, -1, -1):
        if positions[i] == 0:
            continue
        ones = positions[i] % 10  # ones
        tens = positions[i] / 10
        hundreds = positions[i] / 100  # hundreds
        tens = tens - 10 * hundreds  # tens
        if (hundreds > 0):
            money_number_money_text += one_place[hundreds] + "Hundred "
        if (ones > 0 or tens > 0):
            if (hundreds > 0 and i == 0):
                money_number_money_text += "and "
            if (tens == 0):
                money_number_money_text += one_place[ones]
            elif (tens == 1):
                money_number_money_text += one_ten_place[ones]
            else:
                money_number_money_text += ten_place[tens - 2] + \
                    one_place[ones]
        if (i != 0):
            money_number_money_text += name_of_number[i - 1]
    return money_number_money_text

def chm_select_ship_address(request):
	if request.user.is_authenticated():
		try:
			ship = json.loads(request.GET['shipID'])
		except:
			ship = 0

		if ship==0:
			ship_details = models.Ship.objects.all()
		else:
			ship_details = models.Ship.objects.filter(id=ship)
		select_ship	= []
		s_no = 1
		arr = []
		for sh in ship_details:
			if sh.ship_name not in arr:
				arr.append(sh.ship_name)

		for x in arr:
			ship_list = models.Ship.objects.filter(ship_name=x).first()
			#f ship_list.client.proj_name=='CHM':
			if ship_list.client:
				if ship_list.client.proj_name=='CHM':
					client_name = ship_list.client.client_name
					proj_name   = ship_list.client.proj_name
					vm_name     = ship_list.vm_name
					pool_name   = ship_list.pool_name
				# else:
				# 	client_name = ''
				# 	proj_name   = ''
				# 	vm_name     = ''
				# 	pool_name   = ''

					select_ship.append({
						'ship_id'   : ship_list.id,
						'ship_name' : ship_list.ship_name,
						'address'   : ship_list.address,
						'email'     : ship_list.email,
						'email_cc'  : ship_list.email_cc,
						'client'    : client_name,
						's_no' 		: s_no,
						'proj_name' : proj_name,
						'vm_name'   : vm_name,
						'pool_name' : pool_name,
						})
					s_no+=1

		context={
		'select_ship' : select_ship,
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def chm_update_ship_address(request):
	if request.user.is_authenticated():
		address 		 = request.GET['address']
		email 			 = request.GET['email']
		email_c 		 = request.GET['email_c']
		IDx     		 = request.GET['id']
		vm_name 		 = request.GET['vm']
		pool_name 		 = request.GET['pool_name']
		update  		 = models.Ship.objects.filter(id=IDx).first()
		update.address   = address
		update.email     = email
		update.email_cc  = email_c
		update.vm_name 	 = vm_name
		update.pool_name = pool_name
		update.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')


def chm_address_entry(request):
	if request.user.is_authenticated():
		#api_url 	 = "http://0.0.0.0:8000/hb/get_chm_data/"
		api_url 	 = "https://chm.bwesglobal.com/hb/get_chm_data/"
		api_method   = "GET"
		parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response     = requests.get(api_url, params=parameters,verify=False)
		ch_array     = json.loads(response.content)
		chm_array    = ch_array['finance_array']
		ctt_array    = json.loads(response.content)
		clt_array    = ctt_array['cl_array']
		clt_array    = ctt_array['cl_array']

		merge_ship   = []
		ship_array   = []
		client_list  = []

		for s in chm_array:
			if s['ship_name'] not in merge_ship:
				merge_ship.append(s['ship_name'])

		for t in merge_ship:
			check = models.Ship.objects.filter(ship_name=t).first()
			if check>1:
				select_ship_name = check.ship_name
			else:
				select_ship_name = t
			#print '_______>>>>>',select_ship_name

			ship_array.append({
				'select_ship_name' : select_ship_name,
				})

		# client_arr = models.Client.objects.filter(proj_name='CHM')
		# for cl in client_arr:
		# 	client_list.append({
		# 		'id'		  : cl.id,
		# 		'client_name' : cl.client_name,
		# 		})
		for cl in clt_array:
			client_list.append({
				'client_name'  : cl['client_name'],
				})


		context={
		'ship_array'  : ship_array,
		'client_list' : client_list,
		}
		return render_to_response("invoice_display/chm/chm_address_entry.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')

def client_handler(request):
	if request.user.is_authenticated():
		client_name = json.loads(request.GET['client_name'])

		proj_name   = request.GET['proj_name']
		# api_url 	 = "http://0.0.0.0:8000/hb/get_chm_data/"
		api_url 	 = "https://chm.bwesglobal.com/hb/get_chm_data/"
		api_method   = "GET"
		parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response     = requests.get(api_url, params=parameters,verify=False)
		ch_array     = json.loads(response.content)
		chm_array    = ch_array['finance_array']
		ctt_array    = json.loads(response.content)
		clt_array    = ctt_array['cl_array']
		clt_array    = ctt_array['cl_array']

		merge_ship  = []
		ship_array  = []
		client_list = []

		for s in chm_array:
			if s['client_name']==client_name:

				if s['ship_name'] not in merge_ship:
					merge_ship.append(s['ship_name'])

		for t in merge_ship:
			check = models.Ship.objects.filter(ship_name=t).first()
			if check>1:
				select_ship_name = check.ship_name
			else:
				select_ship_name = t
			#print '_______>>>>>',select_ship_name

			ship_array.append({
				'select_ship_name' : select_ship_name,
				})

		# client_arr = models.Client.objects.filter(proj_name='CHM')
		# for cl in client_arr:
		# 	client_list.append({
		# 		'id'		  : cl.id,
		# 		'client_name' : cl.client_name,
		# 		})
		for cl in clt_array:
			client_list.append({
				'client_name'  : cl['client_name'],
				})


		context={
		'ship_array'  : ship_array,
		'client_list' : client_list,
		}

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')



def submit_ship_address_for_address(request):
	if request.user.is_authenticated():
		ship_name 	= json.loads(request.GET['ship_list'])
		address 	= json.loads(request.GET['address'])
		email 		= json.loads(request.GET['email'])
		email_c 	= json.loads(request.GET['email_c'])
		vm_name 	= json.loads(request.GET['vm_name'])

		# api_url 	 = "http://0.0.0.0:8000/hb/get_chm_data/"
		api_url 	 = "https://chm.bwesglobal.com/hb/get_chm_data/"
		api_method   = "GET"
		parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response     = requests.get(api_url, params=parameters,verify=False)
		ch_array     = json.loads(response.content)
		chm_array    = ch_array['finance_array']
		for x in chm_array:
			if x['ship_name'] in ship_name:
				cl_name = x['client_name']
		client_name = cl_name
		clientID 	= models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()
		check 	 	= models.Ship.objects.filter(ship_name=ship_name,client_id=str(clientID)).count()
		if check>0:
			save_address = models.Ship.objects.filter(ship_name=ship_name,client_id=str(clientID)).first()
		else:
			save_address = models.Ship()
		save_address.ship_name 	= ship_name
		save_address.address 	= address
		save_address.email 		= email
		save_address.email_cc   = email_c
		save_address.client_id  = str(clientID)
		save_address.vm_name	= vm_name
	 	save_address.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

def chm_pool_entry(request):
	if request.user.is_authenticated():
		client_details = models.Client.objects.filter(proj_name='BOSS')
		client_list    = []
		client_array   = []
		login_user 	   = request.user	
		for cl in client_details:
			if cl.client_name not in client_array:
				client_array.append(cl.client_name)

		for c in client_array:
			client_list.append({
				'client_name' : c,
				})

		#api_url 	 	  = "http://0.0.0.0:8004/api/get_data_boss/"	
		# api_url 		  = "https://bossv2.bwesglobal.com/api/get_data_boss/"	
		# api_method        = "GET"		
		# parameters        = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'name': 'Shell','ship_type':'No','start_date':'2019-04-01','end_date': '2019-09-30'}
		# response          = requests.get(api_url, params=parameters,verify=False)
		# boss_array        = json.loads(response.content)
		# boss_array        = boss_array['boss_array']
		# for x in boss_array:
		# 	print '=========',x['ship_class']
		context={
		'client_list' : client_list,
		'login_user'  : login_user,
		}
		return render_to_response("invoice_display/chm/chm_pool_entry.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')


def submit_pool_address(request):
	if request.user.is_authenticated():
		client_name = json.loads(request.GET['ship_list'])
		address 	= json.loads(request.GET['address'])
		email 		= json.loads(request.GET['email'])
		email_c 	= json.loads(request.GET['email_c'])
		e_pool_name = json.loads(request.GET['pool_name'])
		e_proj_name = json.loads(request.GET['e_proj_name'])
		client_dt   = models.Client.objects.filter(client_name=client_name,proj_name=e_proj_name).first()
		check 	 	= models.pool_master.objects.filter(client_id=client_dt.id,pool=e_pool_name).count()
		if check>0:
			save_address = models.pool_master.objects.filter(client_id=client_dt.id,pool=e_pool_name).first()
		else:
			save_address = models.pool_master()
		save_address.client_name = client_name
		save_address.address 	 = address
		save_address.email 		 = email
		save_address.email_cc    = email_c
		save_address.client_id   = client_dt.id
		save_address.pool	     = e_pool_name
	 	save_address.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

def chm_select_pool_address(request):
	if request.user.is_authenticated():
		client_name = json.loads(request.GET['shipID'])
		if client_name==0:
			client_details = models.Client.objects.filter(proj_name='CHM').first()
		else:
			client_details = models.Client.objects.filter(client_name=client_name,proj_name='CHM').first()

		if client_name==0:
			ship_details = models.pool_master.objects.all()
		else:
			ship_details = models.pool_master.objects.filter(client_id=client_details.id)
		select_ship	= []
		s_no = 1
		for sh in ship_details:
			try:
				proj_name = sh.client.proj_name
				if sh.client:
					client_name = sh.client.client_name
					pool_name   = sh.pool
				else:
					client_name = ''
					pool_name   = ''
			except:
				client_name = 'okkk'
				pool_name   = 'Pool Removed'

			if sh.vm_name:
				vm_name  = sh.vm_name
			else:
				vm_name = ""

			if sh.email!=None and (sh.email).strip()!="null":
				email = sh.email
			else:
				email = ""
			

			if sh.email_cc!=None and (sh.email_cc).strip()!="null":
				email_cc = sh.email_cc
			else:
				email_cc = ""

			if pool_name!='Pool Removed':
				select_ship.append({
					'address'   : sh.address,
					'email'     : email,
					'email_cc'  : email_cc,
					'client'    : client_name,
					'vm_name'   : vm_name,
					's_no' 		: s_no,
					'pool_name' : pool_name,
					'id'		: sh.id,
					'proj_name' : proj_name
					})
				s_no+=1

		context={
		'select_ship' : select_ship,
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def chm_update_pool_address(request):
	if request.user.is_authenticated():
		address 		 = request.GET['address']
		email 			 = request.GET['email']
		email_c 		 = request.GET['email_c']
		IDx     		 = request.GET['id']
		pool_name 		 = request.GET['pool_name']
		e_vm_name 		 = request.GET['e_vm_name']
		update  		 = models.pool_master.objects.filter(id=IDx).first()
		update.address   = address
		update.email     = email
		update.email_cc  = email_c
		update.pool 	 = pool_name
		update.vm_name   = e_vm_name
		update.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')


def boss_address_entry(request):	
	if request.user.is_authenticated():
		#api_url 	= "http://0.0.0.0:8003/api/get_data_boss/"		
		api_url     = "https://bossv2.bwesglobal.com/api/get_data_boss/"
		api_method  = "GET"
		parameters  = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'name': '','start_date':'','end_date': '','ship_type' : ''}
		response    = requests.get(api_url, params=parameters,verify=False)	
		#print '=======',response.content
		
		boss_array        = json.loads(response.content)	
		boss_array  = json.loads(response.content)
		ctt_array   = json.loads(response.content)
		boss_array  = boss_array['boss_array']
		clt_array   = ctt_array['cl_array']
		# clt_array   = ctt_array['cl_array']
		#print '==========',clt_array

		merge_ship  = []
		ship_array  = []
		client_list = []

		for s in boss_array:
			if s['ship_name'] not in merge_ship:
				merge_ship.append(s['ship_name'])

		for t in merge_ship:
			check = models.Ship.objects.filter(ship_name=t).first()
			if check>1:
				select_ship_name = check.ship_name
			else:
				select_ship_name = t

			ship_array.append({
				'select_ship_name' : select_ship_name,
				})



		for cl in clt_array:
			client_list.append({
				'client_name'  : cl['client_name'],
				})


		context={
		'ship_array' : ship_array,
		'client_list' : client_list,
		}
		#print '=============',context
		return render_to_response("invoice_display/boss/boss_address_entry.html")
	else:
		return HttpResponseRedirect('/it/user_login')

def client_handler_boss(request):
	if request.user.is_authenticated():
		client_name = json.loads(request.GET['client_name'])		
		proj_name   = request.GET['proj_name']
		#api_url 	= "http://0.0.0.0:8003/api/get_data_boss/"
		api_url     = "https://bossv2.bwesglobal.com/api/get_data_boss/"
		api_method  = "GET"
		parameters  = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response    = requests.get(api_url, params=parameters,verify=False)
		boss_array  = json.loads(response.content)
		boss_array  = boss_array['boss_array']

		merge_ship = []
		ship_array = []
		client_list = []

		for s in boss_array:
			if s['client_name']==client_name:
				if s['ship_name'] not in merge_ship:
					merge_ship.append(s['ship_name'])

		for t in merge_ship:
			check = models.Ship.objects.filter(ship_name=t).first()
			if check>1:
				select_ship_name = check.ship_name
			else:
				select_ship_name = t
			#print '_______>>>>>',select_ship_name

			ship_array.append({
				'select_ship_name' : select_ship_name,
				})

		# client_arr = models.Client.objects.filter(proj_name='CHM')
		# for cl in client_arr:
		# 	client_list.append({
		# 		'id'		  : cl.id,
		# 		'client_name' : cl.client_name,
		# 		})


		context={
		'ship_array'  : ship_array,
		'client_list' : client_list,
		}

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def boss_select_pool_address(request):
	if request.user.is_authenticated():
		client_name = json.loads(request.GET['shipID'])
		if client_name==0:
			client_details = models.Client.objects.filter(proj_name='BOSS').first()
		else:
			client_details = models.Client.objects.filter(client_name=client_name,proj_name='BOSS').first()

		if client_name==0:
			ship_details = models.pool_master.objects.all()
		else:
			ship_details = models.pool_master.objects.filter(client_id=client_details.id)
		select_ship	= []
		s_no = 1
		for sh in ship_details:
			if sh.client:
				client_name = sh.client.client_name
				pool_name   = sh.pool
			else:
				client_name = ''
				pool_name   = ''

			select_ship.append({
				'address'   : sh.address,
				'email'     : sh.email,
				'email_cc'  : sh.email_cc,
				'client'    : client_name,
				's_no' 		: s_no,
				'pool_name' : pool_name,
				'id'		: sh.id,
				})
			s_no+=1

		context={
		'select_ship' : select_ship,
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')


def boss_select_ship_address(request):
	if request.user.is_authenticated():
		try:
			ship = json.loads(request.GET['shipID'])
		except:
			ship = 0
		if ship==0:
			ship_details = models.Ship.objects.all()
		else:
			ship_details = models.Ship.objects.filter(id=ship)
		select_ship	= []
		s_no = 1
		for sh in ship_details:
			#print '________',sh.client.client_name
			if sh.client:
				if sh.client.proj_name=='BOSS':
					client_name = sh.client.client_name
					proj_name   = sh.client.proj_name
					vm_name     = sh.vm_name
					pool_name   = sh.pool_name
				# else:
				# 	client_name = ''
				# 	proj_name   = ''
				# 	vm_name     = ''
				# 	pool_name   = ''

					select_ship.append({
						'ship_id'   : sh.id,
						'ship_name' : sh.ship_name,
						'address'   : sh.address,
						'email'     : sh.email,
						'email_cc'  : sh.email_cc,
						'client'    : client_name,
						's_no' 		: s_no,
						'proj_name' : proj_name,
						'vm_name'   : vm_name,
						'pool_name' : pool_name,
						})
					s_no+=1

		context={
		'select_ship' : select_ship,
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def boss_update_ship_address(request):
	if request.user.is_authenticated():
		address 		 = request.GET['address']
		email 			 = request.GET['email']
		email_c 		 = request.GET['email_c']
		IDx     		 = request.GET['id']
		vm_name 		 = request.GET['vm']
		pool_name 		 = request.GET['pool_name']
		update  		 = models.Ship.objects.filter(id=IDx).first()
		update.address   = address
		update.email     = email
		update.email_cc  = email_c
		update.vm_name 	 = vm_name
		update.pool_name = pool_name
		update.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

def submit_boss_ship_for_address(request):
	if request.user.is_authenticated():
		ship_name 	= json.loads(request.GET['ship_list'])
		address 	= json.loads(request.GET['address'])
		email 		= json.loads(request.GET['email'])
		email_c 	= json.loads(request.GET['email_c'])
		vm_name 	= json.loads(request.GET['vm_name'])

		#api_url 	= "http://0.0.0.0:8003/api/get_data_boss/"
		api_url 	= "https://bossv2.bwesglobal.com/api/get_data_boss/"
		api_method  = "GET"
		parameters  = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		response    = requests.get(api_url, params=parameters,verify=False)
		boss_array  = json.loads(response.content)
		boss_array  = boss_array['boss_array']
		for x in boss_array:
			if x['ship_name'] in ship_name:
				cl_name = x['client_name']
		client_name = cl_name

		clientID 	= models.Client.objects.filter(client_name=client_name,proj_name='BOSS').first()
		check 	 	= models.Ship.objects.filter(ship_name=ship_name,client_id=str(clientID)).count()
		if check>0:
			save_address = models.Ship.objects.filter(ship_name=ship_name,client_id=str(clientID)).first()
		else:
			save_address = models.Ship()
		save_address.ship_name 	= ship_name
		save_address.address 	= address
		save_address.email 		= email
		save_address.email_cc   = email_c
		save_address.client_id  = str(clientID)
		save_address.vm_name	= vm_name
	 	save_address.save()
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

def mail_tracker(request):
	if request.user.is_authenticated():
		invoice_details = models.invoice.objects.filter(cancel_invoice=0,invoice_date='2020-12-01')
		client_arr   	= []
		client_list  	= []
		login_user 		= request.user	
		now 			= datetime.now().date()
		
		try:
			year_number     = now.strftime('%Y')
		except:
			year_number     = 2022
		month_number    = now.strftime('%m')

		try:
			prev_month      = int(month_number)
		except:
			prev_month      = 12
			
		if prev_month<=9:
			prv_mth = '0'+str(prev_month)
		else:
			prv_mth = prev_month

		start_date 		= str(year_number)+'-'+str(prv_mth)+'-01' #'2023-12-01' #
		get_month		= monthrange(int(year_number),int(prv_mth))[1] #'2023-12-01'#
		end_date_format	= str(year_number)+'-'+str(prv_mth)+'-'+str(get_month)	 #'2023-12-31' #
		
		# start_date 	= '01'+'/'+str(prv_mth)+'/'+str(year_number)
		# get_month	= monthrange(int(year_number),int(month_number))[1]
		# end_date	= str(get_month)+'/'+str(month_number)+'/'+str(year_number)	
		#print '----',now
		for i in invoice_details:
			try:
				client_name = i.client.client_name
			except:
				client_name = ''
			if client_name not in client_arr:
				client_arr.append(client_name)

		for cl in client_arr:
			client_list.append({
				'client_name' : cl,
				})

		context={
		'client_list' : client_list,
		'start_date'  : str(start_date),
		'end_date'    : str(end_date_format),
		'login_user'  : login_user
		}
		return render_to_response("invoice_display/mail_tracker.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')


def select_client_handler(request):	
	if request.user.is_authenticated():
		client_name = json.loads(request.GET['client_name'])
		proj_name 	= json.loads(request.GET['proj_name'])
		start_date 	= json.loads(request.GET['start_date'])
		end_date 	= json.loads(request.GET['end_date'])
		
		

		if client_name!='Select Client Name':
		 	client 		= models.Client.objects.filter(client_name=client_name,proj_name=proj_name).first()			
		# 	#if start_date==0 and end_date==0:
		# 	#	invoice_details = models.invoice.objects.filter(proj_name=proj_name,cancel_invoice=0,payment_status=None,client_id=client)
				
		# 	#else:
			invoice_details = models.invoice.objects.filter(proj_name=proj_name,cancel_invoice=0,payment_status=None,client_id=client,invoice_date__lte=end_date,invoice_date__gte=start_date)
		# else:
		# 	invoice_details = ''
			#print '----',start_date,'---'

			

		invoice_array   = []
		invoice_append  = []
		s_no =1
		for cl in invoice_details:
			if cl.invoice_no not in invoice_append:
				invoice_append.append(cl.invoice_no)

		x = 0
		for i in sorted(invoice_append):
			client 		= models.Client.objects.filter(client_name=client_name,proj_name=proj_name).first()
			invoice_det = models.invoice.objects.filter(invoice_no=i,proj_name=proj_name,client_id=client).order_by('invoice_no').first()
			counter     = models.invoice.objects.filter(invoice_no=i).count()
			invoice_date = ''
			disch_port   = ''
			if counter>1:
				if invoice_det.vessel_type!='None' and invoice_det.vessel_type!=None:
					if invoice_det.vessel_type=='Teekay':
						fleet 	  = invoice_det.ship_name
						voyage_no = invoice_det.voyage_no
						vm_name   = invoice_det[x].vm_name
						try:
							invoice_date = invoice_det.invoice_date
							disch_date   = invoice_det.disch_date
							disch_port 	 = invoice_det.disch_port
						except:
							invoice_date = ''
							disch_date   = ''
							disch_port   = ''
					else:
						fleet 	  = str(invoice_det.vessel_type)+' Fleet'
						voyage_no = ''
						vm_name   = ''
				else:
					fleet     = ''
					voyage_no = ''
					vm_name   = ''

			else:
				
				invoice_date  = invoice_det.invoice_date.strftime('%d-%b-%Y')
				#invoice_date   = datetime.strptime(str(invoice_datex), "%Y-%m-%d").strftime('%d-%b-%Y')
				fleet 		   = invoice_det.ship_name
				voyage_no 	   = invoice_det.voyage_no
				try:
					disch_date = invoice_det.disch_date
					disch_port = invoice_det.disch_port
				except:
					disch_date = ''
					disch_port = ''

			x+=1


			invoice_array.append({
				'ship_name' 	: fleet,
				'voyage_no' 	: voyage_no,
				'vm_name'   	: invoice_det.vm_name,
				's_no'			: s_no,
				'link'     	 	: invoice_det.url,
				'mail_to'  	 	: invoice_det.mail_to,
				'mail_cc'   	: invoice_det.mail_from,
				'id' 			: invoice_det.id,
				'invoice_no' 	: invoice_det.invoice_no,
				'client_name' 	: invoice_det.client.client_name,
				'proj_name'     : invoice_det.client.proj_name,
				'disch_date'    : str(invoice_date),
				'disch_port'	: disch_port,
				'invoice_date'  : '',#str(invoice_date),				
				})
			s_no+=1

		context={
		'invoice_array' : invoice_array
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

def select_invoice_no_mail(request):
	models.mail_invoice_details.objects.all().delete()
	selection_array = json.loads(request.GET['selection_invoice'])
	client_name 	= json.loads(request.GET['client_name'])
	proj_name 		= json.loads(request.GET['proj_name'])

	select_array    = []
	mail_array      = []
	select_invoice  = [int(x) for x in selection_array]
	for s in select_invoice:
		invoice_det         = models.invoice.objects.filter(id=s).first()
		invoice_no          = invoice_det.invoice_no
		client_id           = invoice_det.client_id
		save_det            = models.mail_invoice_details()
		save_det.invoice_no = invoice_no
		save_det.client_id  = client_id
		if invoice_det.inr!=None and invoice_det.usd==None:
			currency_type = 'INR'
		elif invoice_det.inr==None and invoice_det.usd!=None:
			currency_type = 'USD'
		save_det.currency_type = currency_type
		save_det.proj_name 	   = invoice_det.proj_name
		save_det.save()

	client_id = invoice_det.client_id

	return HttpResponse(json.dumps(client_id))

def mail_send(request):
	clientID  		 = int(json.loads(request.GET['client']))
	proj_name 		 = request.GET['proj_name']
	attached_invoice = models.mail_invoice_details.objects.filter(client_id=clientID,proj_name=proj_name)
	invoice_array 	 = []
	tag_name 		 = ''
	login_user 	= request.user

	for x in attached_invoice:
		if x.currency_type=='USD':
			invoice_det  = models.invoice.objects.filter(invoice_no=x.invoice_no,usd='USD').first()
		elif x.currency_type=='INR':
			invoice_det  = models.invoice.objects.filter(invoice_no=x.invoice_no,inr='INR').first()
		if invoice_det.proj_name=='BOSS':
			vessel_type    = invoice_det.vessel_type
			vessel_name    = invoice_det.vessel_type
			caption        = 'BlueWater/BOSS/Invoices'
			display        = 'none'
			voyage_no      = ''
			boss_log_show  = ''
			chm_log_show   = 'none'
			format_year    = datetime.strptime(invoice_det.month, "%Y-%m-%d").strftime('%Y')
			format_month   = datetime.strptime(invoice_det.month, "%Y-%m-%d").strftime('%b')
			int_month 	   = datetime.strptime(invoice_det.month, "%Y-%m-%d").strftime('%m')
			get_month 	   = monthrange(int(format_year),int(int_month))[1]
			period 		   = str(format_month)+' '+str(format_year)
			tag_name 	   = 'BOSS'

		elif invoice_det.proj_name=='CHM':
			if invoice_det.client.client_name=='Shell NWE':
				format_year  = datetime.strptime(invoice_det.month, "%Y-%m-%d").strftime('%Y')
				format_month = datetime.strptime(invoice_det.month, "%Y-%m-%d").strftime('%b')
				int_month 	 = datetime.strptime(invoice_det.month, "%Y-%m-%d").strftime('%m')
				get_month 	 = monthrange(int(format_year),int(int_month))[1]
				period 		 = str(format_month)+str(format_year)
				vessel_type  = 'Shell NWE'
				period       = str(format_month)+str(format_year)
			else:
				vessel_type = str(invoice_det.ship_name)+'_'+str(invoice_det.voyage_no)
				period      = ''

			format_year    	= datetime.strptime(invoice_det.month, "%Y-%m-%d").strftime('%Y')
			format_month   	= datetime.strptime(invoice_det.month, "%Y-%m-%d").strftime('%b')
			int_month 	   	= datetime.strptime(invoice_det.month, "%Y-%m-%d").strftime('%m')
			get_month 	   	= monthrange(int(format_year),int(int_month))[1]

			if invoice_det.client.client_name=='Shell' or invoice_det.client.client_name=='Shell NWE':
				caption 	= "****[Shell]/Cargo Heating Services/ Contract No. DS65730/ Invoice****"
			else:
				caption     = '****['+str(invoice_det.client.client_name)+']/BlueWater/Cargo Heating Management Services/Invoices****'

			display     	= ''
			vessel_name 	= invoice_det.ship_name
			voyage_no   	= invoice_det.voyage_no
			boss_log_show   = 'none'
			chm_log_show 	= ''
			period  		= str(format_month)+' '+str(format_year)
			tag_name 	   	= 'CHM'


		try:
			disch_date  = invoice_det.disch_date.strftime("%d-%b-%Y")
		except:
			disch_date  = ''

		try:
			invoice_mail = models.pool_master.objects.filter(client_id=clientID).first()
			mail_to 	= invoice_mail.email
			mail_cc 	= invoice_mail.email_cc
			mail_from 	= invoice_det.mail_from
		except:
			mail_to     = ''
			mail_cc     = ''
			mail_from   = ''

		
		if invoice_det.client.client_name=='Ultranav':
			pool = invoice_det.account_type
			hide = ''	
		
		elif invoice_det.client.client_name=='Navig8':
			pool = invoice_det.account_type
			hide = ''		

		elif invoice_det.client.client_name=='Shell':
			pool = invoice_det.account_type
			hide = ''		

		elif invoice_det.client.client_name=='Shell NWE':
			pool = invoice_det.account_type
			hide = ''

		elif invoice_det.client.client_name=='Litasco_Dubai':
			pool = invoice_det.remark
			hide = ''
		else:
			pool = ''
			hide = 'none'

		try:
			nomination_date = invoice_det.nomination_date.strftime("%d-%b-%Y")
		except:
			nomination_date = ""

		try:
			voyage_id       = invoice_det.voyage_id
		except:
			voyage_id 		= ''

		invoice_array.append({
		'ship_name' 	: vessel_name,
		'voyage_no' 	: voyage_no,
		'invoice_no' 	: invoice_det.invoice_no,
		'url'  			: invoice_det.url,
		'invoice_date' 	: invoice_det.invoice_date.strftime("%d-%b-%Y"),
		'vm_name' 		: invoice_det.vm_name,
		'disch_port'  	: invoice_det.disch_port,
		'disch_date'    : disch_date,
		'vessel_type'   : vessel_type,
		'caption'       : caption,
		'display'       : display,
		'chm_log_show'  : chm_log_show,
		'boss_log_show'	: boss_log_show,
		'period'        : period,
		'mail_to' 		: mail_to,
		'mail_cc' 		: mail_cc,
		'mail_from' 	: mail_from,
		'pool'			: pool,
		'hide'  		: hide,
		'nominate_date' : nomination_date,
		'voyage_id'  	: voyage_id,
		})

	context={
	'invoice_array' : invoice_array,
	'tag_name'		: tag_name,
	'login_user'    : login_user,
	'hide'			: hide,
	}
	return render_to_response("invoice_display/mail_sent.html",context)

def attached_mail_details(request):
	import smtplib
	import pprint
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from django.core.mail import EmailMultiAlternatives
	from email.MIMEImage import MIMEImage

	clientID 	   = json.loads(request.GET['clientID'])[0]
	details        = json.loads(request.GET['details'])
	sign 		   = json.loads(request.GET['sign'])
	to      	   = json.loads(request.GET['to'])
	mail_from      = json.loads(request.GET['from'])
	mail_cc 	   = json.loads(request.GET['cc'])
	subject 	   = json.loads(request.GET['subject'])
	log_details    = models.mail_invoice_details.objects.filter(client_id=clientID)
	bcc_email 	   = 'santosh@bwesglobal.com'
	text_content   = 'This is an important message.'
	select_dir     = os.path.dirname(__file__)

	for x in log_details:
		cl = models.Client.objects.filter(id=clientID).first()
		vessel_details  = models.invoice.objects.filter(client_id=clientID,invoice_no=x.invoice_no).first()
	 	vm_name    		= vessel_details.vm_name
	log 		   = request.GET['log']
	html_content   = 'Good day,<br><br><font size="3em">'+details+'</font><br><br>'+(log)+'<br><br><br>'+(sign)+''
	mailto 		   = to
	cc_email 	   = mail_cc
	mailsubject    = str(cl.client_name)+'/'+str(subject)
	#if mail_cc!=None or mail_from!=None:
	msg  = EmailMultiAlternatives(mailsubject,text_content,'santosh@bwesglobal.com',[mailto],bcc=[bcc_email],cc=[cc_email])	
	#elif mail_cc==None or mail_from==None:
	#	msg  = EmailMultiAlternatives(mailsubject,text_content,'santosh@bwesglobal.com',[mailto])

	msg.attach_alternative(html_content, "text/html")
	attach_details = models.mail_invoice_details.objects.filter(client_id=clientID)
	for t in attach_details:
		att_details    = models.invoice.objects.filter(client_id=clientID,invoice_no=t.invoice_no).first()
		slect_pdf_file = str(select_dir)+str(att_details.url)
	 	msg.attach_file(slect_pdf_file)
	msg.send()

	single_data = []
	for c in log_details:
		i = models.invoice.objects.filter(invoice_no=c.invoice_no,cancel_invoice=0).first()
		if i.invoice_no not in single_data:
			single_data.append(i.invoice_no)

	for j in single_data:
		invoice_mail_check = models.inbox_invoice_details.objects.filter(invoice_no=j).count()
		if invoice_mail_check>0:
			save_mail_check = models.inbox_invoice_details.objects.filter(invoice_no=j).first()
		else:
			save_mail_check = models.inbox_invoice_details()
			
	 	ii = models.invoice.objects.filter(invoice_no=j,cancel_invoice=0).first()
		save_mail_check.invoice_no   	 = ii.invoice_no
		save_mail_check.invoice_date 	 = ii.invoice_date
		save_mail_check.vessel_name  	 = ii.ship_name
		save_mail_check.voy_no 	 	 	 = ii.voyage_no
		save_mail_check.invoice_amount 	 = ii.invoice_amount
		save_mail_check.pdf_path 		 = ii.url
		save_mail_check.mail 			 = to
		save_mail_check.mail_cc 		 = mail_cc
		save_mail_check.mail_from	     = mail_from
		save_mail_check.sent_mail_date   = datetime.now().date()
		save_mail_check.client_id        = ii.client_id
		save_mail_check.save()
	return HttpResponse(json.dumps('done'))

def pool_master(request):
	#api_url 	 = "http://0.0.0.0:8000/hb/get_chm_data/"
	api_url 	 = "https://chm.bwesglobal.com/hb/get_chm_data/"
	api_method   = "GET"
	parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
	response     = requests.get(api_url, params=parameters,verify=False)
	ctt_array    = json.loads(response.content)
	clt_array    = ctt_array['cl_array']
	clt_array    = ctt_array['cl_array']
	ch_array     = json.loads(response.content)
	chm_array    = ch_array['finance_array']
	client_list  = []
	pool_list    = []
	pol_array    = []
	pool_array = models.pool_master.objects.all()
	for pl in pool_array:
		client_name = pl.client.client_name
		pool_list.append({
			'pool_id' 		: pl.id,
			'pool_name' 	: pl.pool,
			'email'			: pl.email,
			'email_cc'  	: pl.email_cc,
			'client_name' 	: client_name,
			'address' 		: pl.address,
			})

	not_array = []
	for p in chm_array:
		if p['pool_namex'] not in not_array:
			not_array.append(p['pool_namex'])

	for v in not_array:
		pol_array.append({
			'pool_name' : v
		})


	for cl in clt_array:
		client_list.append({
		'client_name'  : cl['client_name'],
		})

	#api_url 	 = "http://0.0.0.0:8003/api/get_data_boss/"
	api_url 	 = "https://bossv2.bwesglobal.com/api/get_data_boss/"
	api_method   = "GET"
	parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
	response     = requests.get(api_url, params=parameters,verify=False)
	cl_array     = json.loads(response.content)
	cl_array     = cl_array['cl_array']
	boss_array   = json.loads(response.content)
	boss_array   = boss_array['boss_array']
	boss_client_list = []
	for x in cl_array:
		boss_client_list.append({
			'client_name' : x['client_name']
			})

	pll_arr = []
	for c in boss_array:
		if c['ship_class'] not in pll_arr:
			pll_arr.append(c['ship_class'])

	boss_pol_list = []
	for bp in pll_arr:
		if bp!=None:
			boss_pol_list.append({
				'pool_name' : bp
				})
	context={
	'client_list'      : client_list,
	'pool_list'        : pool_list,
	'boss_client_list' : boss_client_list,
	'pool_details'     : pol_array,
	'boss_pol_list'    : boss_pol_list,
	}
	return render_to_response("invoice_display/chm/pool_master.html",context)

def select_project_handler(request):
	proj_name 	   = json.loads(request.GET['proj_name'])
	client_array   = []
	client_list    = []
	client_details = models.invoice.objects.filter(proj_name=proj_name)
	for cl in client_details:
		client = models.Client.objects.filter(id=cl.client_id).first()
		try:
			if client.client_name not in client_list:
				client_list.append(client.client_name)
		except:
			pass

	for c in client_list:
		client_array.append({
		'client_name' : c,
		})
	#print '------Open ho gaya E-Mail'
	#print client_array
	return HttpResponse(json.dumps(client_array))

@csrf_exempt
def submit_pool_master(request):
	e_client_name   = json.loads(request.POST['e_client_name'])
	e_address   	= json.loads(request.POST['e_address'])
	e_mail   		= json.loads(request.POST['e_mail'])
	e_mail_cc   	= json.loads(request.POST['e_mail_cc'])
	e_pool_name   	= json.loads(request.POST['e_pool_name'])
	e_proj_name		= json.loads(request.POST['e_proj_name'])
	clientID 		= models.Client.objects.filter(client_name=e_client_name,proj_name=e_proj_name).first()

	check = models.pool_master.objects.filter(client_id=clientID,pool=e_pool_name).count()
	if check>0:
		submit_pool_master = models.pool_master.objects.filter(client_id=clientID,pool=e_pool_name).first()
	else:
		submit_pool_master = models.pool_master()
	submit_pool_master.client_id = clientID.id
	submit_pool_master.pool 	 = e_pool_name
	submit_pool_master.email 	 = e_mail
	submit_pool_master.email_cc  = e_mail_cc
	submit_pool_master.address   = e_address
	submit_pool_master.save()
	return HttpResponse(json.dumps('done'))


@csrf_exempt
def update_pool_master(request):
	e_clientID  			= json.loads(request.POST['clientID'])
	pool_name   			= json.loads(request.POST['pool_name'])
	address   				= json.loads(request.POST['address'])
	mail   					= json.loads(request.POST['mail'])
	mail_cc   				= json.loads(request.POST['mail_cc'])
	update_pool 			= models.pool_master.objects.filter(id=e_clientID).first()
	update_pool.pool_name 	= pool_name
	update_pool.address  	= address
	update_pool.email  		= mail
	update_pool.email_cc 	= mail_cc
	update_pool.save()
	return HttpResponse(json.dumps('done'))

def show_folder(request):	
	import os
	path  = "/var/www/html/invoice/it/static/pdf/"
	files = os.listdir(path)
	folder_details  = []
	for f in files:
		if f.endswith('.png') or f.endswith('.html'):
			print 
		else:
			check_invoice = models.invoice.objects.filter(client__client_name=f,proj_name='CHM').first()			
			if check_invoice:
				if check_invoice.proj_name=='CHM':				
					folder_details.append({
						'folder_name' : f,
						'folder_icon' : '/static/img/folder.png/'		
						})
		
	context={
	'folder_details' : folder_details
	}
	
	#return HttpResponse(json.dumps('done'))
	return render_to_response("invoice_display/show_folder.html",context)


def show_fold(request):	
	import os
	path  = "/var/www/html/invoice/it/static/pdf/"
	files = os.listdir(path)
	folder_details_boss  = []
	for f in files:
		if f.endswith('.png') or f.endswith('.html'):
			print 
		else:
			check_invoice = models.invoice.objects.filter(client__client_name=f,proj_name='BOSS').first()			
			if check_invoice:
				if check_invoice.proj_name=='BOSS':										
					folder_details_boss.append({
						'folder_name' : f,
						'folder_icon' : '/static/img/folder.png/'		
						})
		
	context={
	'folder_details_boss' : folder_details_boss
	}
	
	#return HttpResponse(json.dumps('done'))
	return render_to_response("invoice_display/show_fold.html",context)


@csrf_exempt
def filter_invoice_tracker(request):
	try:
		curr_invodate =  json.loads(request.POST['curr_invodate'])
	except:
	 	curr_invodate = ""
	

 	try:
		start_date 		 = json.loads(request.POST['start_date'])
		end_date 		 = json.loads(request.POST['end_date'])
		start_date_for   = datetime.strptime(start_date,"%m/%d/%Y").strftime('%Y-%m-%d')
		end_date_for     = datetime.strptime(end_date,"%m/%d/%Y").strftime('%Y-%m-%d')
	except:
		min_date  		 = models.invoice.objects.all().order_by('invoice_date').first()
	 	invoice_min_date = min_date.invoice_date.date()
	 	max_date  		 = datetime.now().date() #
	 	max_datexx       = models.invoice.objects.all().order_by('-invoice_date').first()
	 	invoice_max_date = max_datexx.invoice_date.date()	 	
	 	start_date_for   = invoice_min_date
	  	end_date_for     = max_date
		
	#print '==========',start_date_for,'======',end_date_for
	try:
		prjoxx = json.loads(request.POST['projx'])
	except:
		prjoxx = ''
	
	try:
		currency_list    = json.loads(request.POST['usd_inr_list'])
	except:
		currency_list = "and cl.currency_type='USD'"
	
	
	try:
		proj_name  = json.loads(request.POST['project_list'])		

	except:
		proj_name = 'CHM'


	
	try:
		unpaid_list  = json.loads(request.POST['pad_unpaid_list'])
	except:
		unpaid_list  =" 0"
	
	try:
		payment_status = json.loads(request.POST['payment_status'])
	except:
		payment_status = "0"

	try:
		client_list    	= json.loads(request.POST['client_list'])
	except:
		client_list = "0"

	try:
		usd_inr_list   	= json.loads(request.POST['usd_inr_list'])
	except:
		usd_inr_list = "0"

	try:
		pad_unpaid_list = json.loads(request.POST['pad_unpaid_list'])
	except:
		pad_unpaid_list = "0"


	try:
		curr = json.loads(request.POST['url_currency'])[0]
		if curr=='INR':
			insert_proj_name  = ""
		elif curr=='USD':
			insert_proj_name  = "and ins.proj_name='"+str(proj_name)+"'"
	except:
		insert_proj_name  = ""

	# if proj_name=='BOSS':
	# 	insert_proj_name  = "and ins.proj_name='BOSS'"
	if proj_name=='CHM':
		insert_proj_name  = "and ins.proj_name='CHM'"
	else:
		insert_proj_name  = ""




	filters = "WHERE ins.invoice_date>='"+str(start_date_for)+"' and ins.invoice_date<='"+str(end_date_for)+"' "+str(insert_proj_name)+" "+str(currency_list)+" "+str(curr_invodate)+" "+payment_status+" and cl.id=ins.client_id GROUP BY ins.invoice_no,ins.proj_name,ins.inr,ins.usd;"
	
	list_arr  	   	= []
	price 		   	= ''

	qry    = "SELECT * FROM it_invoice ins,it_client cl "+str(filters)+""
	#print '=======',qry
	cursor = connection.cursor()
	cursor.execute(qry)
	invoice_details = cursor.fetchall()
	shhip_list 	    = []
	client_arr      = []
	client_list     = []
	invoice_list    = []
	total_amount    = ''
	total_igst_list = ''
	tax_chm_amount  = 0
	invoice_style   = ''	
	cr 				= 0
	for i in invoice_details:
		ship_name = i[7]
		if usd_inr_list=='INR':
			counter  = models.invoice.objects.filter(invoice_no=i[1],inr='INR').count()
		elif usd_inr_list=='USD':
			counter  = models.invoice.objects.filter(invoice_no=i[1],usd='USD').count()
		else:
			counter  = ''

		chm_amt 		  = 0
		chm_sums  		  = 0
		boss_amt 		  = 0
		boss_sums 		  = 0
		label_chm 		  = ''
		label_boss 		  = ''
		single_chm_amt 	  = 0
		single_chm_sums   = 0
		single_boss_amt   = 0
		single_boss_sums  = 0
		period 			  = ''
		igst_boss         = 0
		igst_chm          = 0
		total_igst_chm 	  = 0
		total_igst_boss   = 0
		invoice_calc 	  = 0
		sum_boss     	  = 0
		tax_boss_amount   = 0

		if counter>1:
			voyage_no = ''
			if i[23]!='None':
				shipname = str(i[23])+' Fleet'
				if shipname=='Shell NWE Fleet':
					ship_name = ''
				else:
					if counter=='':
						ship_name = i[7]
						if ship_name.isdigit():
							ship_details  = models.invoice.objects.filter(id=i[0]).first()
							if ship_details.vessel_type=='VLCC' and ship_details.proj_name=='BOSS':
								ship_name = 'VLCC Fleet'
							elif ship_details.vessel_type=='LR1' and ship_details.proj_name=='BOSS':
								ship_name = 'LR1 Fleet'
							elif ship_details.vessel_type=='LR2' and ship_details.proj_name=='BOSS':
								ship_name = 'LR2 Fleet'
							elif ship_details.vessel_type=='VLGC' and ship_details.proj_name=='BOSS':
								ship_name = 'VLGC Fleet'
							elif ship_details.vessel_type=='Tsakos' and ship_details.proj_name=='BOSS':
								ship_name = 'Tsakos Fleet'

					else:
						ship_name = shipname
			else:
				ship_name = ''


			# if i[9]=='BOSS' and i[39]=='INR':
			# 	try:
			# 		boss_amt = i[27]*i[28]*i[26]
			# 	except:
			# 		boss_amt = 0
			# 	label_boss = 'INR '
			# elif i[9]=='BOSS' and i[39]=='USD':
			# 	boss_amt = i[27]*i[26]
			# 	label_boss = 'USD '

			if i[9]=='CHM' and i[39]=='INR':
				try:
					chm_amt = i[27]*i[28]*i[26]
				except:
					chm_amt = 0
				label_chm = 'INR '
			elif i[9]=='CHM' and i[39]=='USD':
				chm_amt = i[27]*i[26]
				label_chm = 'USD '

			#if i[9]=='BOSS' and i[39]=='INR' or i[9]=='CHM' and i[39]=='INR':
			if i[9]=='CHM' and i[39]=='INR':
				invoice_calc = models.invoice.objects.filter(invoice_no=i[1])
				cr=0
				for x in invoice_calc:
					cr+=1
					try:
						boss_sums+=x.qty*x.price*x.rate
					except:
						boss_sums=0
					tax_boss_amount=(boss_sums)
					igst_boss=(boss_sums*18/100)
					try:
						chm_sums+=x.qty*x.price*x.rate
					except:
						chm_sums=0
					tax_chm_amount=(chm_sums)
					igst_chm=(chm_sums*18/100)

			# elif i[9]=='BOSS' and i[39]=='USD': #or i[9]=='CHM' and i[38]=='USD':
				#invoice_calc = models.invoice.objects.filter(invoice_no=i[1],proj_name='BOSS',client_id=64,usd='USD')
			if i[9]=='CHM' and i[39]=='USD':
				invoice_calc = models.invoice.objects.filter(invoice_no=i[1],proj_name='CHM')
			#print '=========', i[9],'====',i[38]
			cr=0
			for x in invoice_calc:
				cr+=1
				try:
					boss_sums+=x.price*x.qty
				except:
					boss_sums=0
				tax_boss_amount=boss_sums
				try:
					chm_sums+=x.qty*x.price
				except:
					chm_sums=0
				tax_chm_amount = chm_sums
				igst_chm  = 0
				igst_boss = 0

			if i[9]=='CHM':
				if i[6]!=1:
					total_amount = str(label_chm)+str(round(tax_chm_amount,0))
					total_igst_list = round(igst_chm,1)
				else:
					total_amount = ''
					total_igst_list = ''

			elif i[9]=='BOSS' and i[39]=='USD' and i[36]=='Shell':
				if i[6]!=1:
					total_amount    = str(label_boss)+str(round(tax_boss_amount,0))
					total_igst_list = round(igst_boss,1)
					#print '==========',total_amount,'=====',label_boss,'======',tax_boss_amount
				else:
					total_amount = ''
					total_igst_list = ''
		else:
			if counter==1:
				single_label_boss = ''
				# if i[9]=='BOSS' and i[39]=='INR':
				# 	single_boss_amt = i[27]*i[28]*i[26]
				# 	single_label_boss = 'INR '
				# elif i[9]=='BOSS' and i[39]=='USD':
				# 	single_boss_amt = i[27]*i[26]
				# 	single_label_boss = 'USD '

				if i[9]=='CHM' and i[39]=='INR':
					single_chm_amt = i[27]*i[28]*i[26]
					single_label_chm = 'INR '
				elif i[9]=='CHM' and i[39]=='USD':
					single_chm_amt = i[27]*i[26]
					single_label_chm = 'USD '

				for e in xrange(1,counter+1):
					#if i[9]=='BOSS' and i[39]=='INR' or i[9]=='CHM' and i[39]=='INR':
					if [9]=='CHM' and i[39]=='INR':
						single_boss_sums+=single_boss_amt
						#tax_single_boss = ((single_boss_sums*18/100)+single_boss_sums)
						tax_single_boss = (single_boss_sums)
						igst_boss = (single_boss_sums*18/100)
						single_chm_sums+=single_chm_amt
						#tax_single_chm = ((single_chm_sums*18/100)+single_chm_sums)
						tax_single_chm = (single_chm_sums)
						igst_chm = (single_chm_sums*18/100)
					#elif i[9]=='BOSS' and i[39]=='USD' or i[9]=='CHM' and i[39]=='USD':
					elif i[9]=='CHM' and i[39]=='USD':
						single_boss_sums+=single_boss_amt
						tax_single_boss = single_boss_sums
						single_chm_sums+=single_chm_amt
						tax_single_chm = single_chm_sums
						igst_chm  = 0
						igst_boss = 0



				if i[9]=='CHM':
					if i[6]!=1:
						total_amount = str(single_label_chm)+str(round(tax_single_chm,0))
						total_igst_list = round(igst_chm,1)
					else:
						total_amount = ''
						total_igst_list = ''

				# elif i[9]=='BOSS':
				# 	if i[6]!=1:
				# 		total_amount = str(single_label_boss)+str(round(tax_single_boss,0))
				# 		total_igst_list = round(igst_boss,1)
				# 	else:
				# 		total_amount = ''
				# 		total_igst_list = ''


			voyage_no = i[8]
			ship_name = i[7]
			

		#if i[9]=='BOSS' and i[39]=='INR' or i[9]=='CHM' and i[39]=='INR':
		if i[9]=='CHM' and i[39]=='INR':
			try:
				start_date_for = (i[15]).strftime('%b')
				period = '01-'+str(start_date_for)+'-'+(i[15]).strftime('%Y')
			except:
				month_split 	= i[19].split(',')
				disch_date_for  = datetime.strptime(month_split[0], "%Y-%m-%d").strftime('%d-%b-%Y')
				period 			= disch_date_for
		elif i[9]=='CHM' and i[39]=='USD':
			try:
				start_date_for  = (i[15]).strftime('%d-%b-%Y')
				period 			= start_date_for
			except:
				month_split 	= i[19].split(',')
				disch_date_for  = datetime.strptime(month_split[0], "%Y-%m-%d").strftime('%d-%b-%Y')
				period 			= disch_date_for

		try:
			client_name = i[37] #invoices.client.client_name
		except:
			client_name = ''


		#if i[36]=='Shell' and i[9]=='BOSS' and i[38]=='USD':
		#	check_payment_status = models.invoice.objects.filter(payment_status="Paid",invoice_no=i[1],proj_name='BOSS',usd='USD',client_id=64).count()
		# else:
		check_payment_status = models.invoice.objects.filter(payment_status="Paid",invoice_no=i[1]).count()
		if check_payment_status>0:
			show_button = 'none'
		else:
			show_button = ''

		if i[6]==0 and i[11]=="Paid":
			#print '______Paid'
			icons  		= ''
			colors 		= 'green'
			show_button = 'none'
		elif i[6]==1 and i[11]==None:
			#print '_______Cancel'
			icons  		= 'fa-times-circle fa-1x'
			colors 		= 'red'
			show_button = 'none'
		elif i[6]==0 and i[11]==None:
			icons  		= ''
			colors 		= 'black'
			show_button = ''
		else:
			#print '______Default'
			icons  		= 'fa-times-circle fa-1x'
			colors 		= 'red'
			show_button = 'none'

		client = i[37]		
		if client not in client_arr:
			client_arr.append(client)

		for_invoice_date  = i[2].date()
		for_rececive_date = i[4]

		#if i[9]=='CHM' and i[39]=='INR' or i[9]=='BOSS' and i[39]=='INR':
		if i[9]=='CHM' and i[39]=='INR':
			if i[6]!=1:
				exchange_rate = i[28]
				price 		  = i[27]
			else:
				exchange_rate = ''
				price 		  = ''
		else:
			exchange_rate = ''

		

		try:
			invoice_date = datetime.strptime(str(for_invoice_date), "%Y-%m-%d").strftime('%d-%b-%Y')

		except:
			invoice_date = ''

		try:
			disch_date = datetime.strptime(invoices.disch_date, "%Y-%m-%d").strftime('%d-%b-%Y')
		except:
			disch_date = ''

		try:
			rec_date = datetime.strptime(str(for_rececive_date), "%Y-%m-%d").strftime('%d-%b-%Y')

		except:
			rec_date = ''

		if i[3]!=None:
			invoice_amt = i[3]
		else:
			invoice_amt = ''

		remarks = i[22]
		if i[9]=='CHM' and i[39]=='INR':
			invoice_style = i[1]+'/'+str(i[9])+'/'+str(i[38])
		elif i[9]=='CHM' and i[39]=='USD':
			invoice_style = i[1]+'/'+str(i[9])+'/'+str(i[38])
		# elif i[9]=='BOSS' and i[39]=='INR':
		# 	invoice_style = i[1]+'/'+str(i[9])+'/'+str(i[38])
		# elif i[9]=='BOSS' and i[39]=='USD':
		# 	invoice_style = i[1]+'/'+str(i[9])+'/'+str(i[38])

		try:
			price_type = str(client_name)+' ('+i[34]+')'
		except:
			price_type = ''


		# if i[21]:
		# 	url_pdf = i[21]
		# 	img_logo    = '/static/img/pdf.png'
		# else:
		

		if client_name=='Poompuhar Shipping Corporation Limited':
			select_dir  = os.path.dirname(__file__)
			vvds = i[1]
			split_invoice_no  = vvds.replace('/','_')
			url_pdfx    = '/static/pdf/Poompuhar Shipping Corporation Limited/poompuhar_template_'+str(split_invoice_no)+'.xlsx'
			img_logo    = '/static/img/excel.png'
		
		elif client_name=='Clearlake':
			select_dir  = os.path.dirname(__file__)
			vvds = i[1]
			split_invoice_no  = vvds.replace('/','_')
			url_pdfx    = '/static/pdf/Clearlake/clearlake_template_'+str(split_invoice_no)+'.xlsx'
			img_logo    = '/static/img/excel.png'
		elif client_name=='Shell':
			if cr>20:
				select_dir  = os.path.dirname(__file__)
				vvds = i[1]
				split_invoice_no  = vvds.replace('/','_')
				url_pdfx    = '/static/pdf/Shell/shell_template_'+str(split_invoice_no)+'.xlsx'
				img_logo    = '/static/img/excel.png'
			elif cr<20:
				url_pdfx	= i[21]
				img_logo    = '/static/img/pdf.png'
		else:
			url_pdfx	= i[21]
			img_logo    = '/static/img/pdf.png'

		


		

		#max_invoice_date = models.invoice.objects.all().aggregate(Max('invoice_date'))
		min_invoice_date = models.invoice.objects.all().aggregate(Min('invoice_date'))
		max_date = datetime.now().date() # #max_invoice_date['invoice_date__max']
		min_date = min_invoice_date['invoice_date__min']
		if i[24]==6:
			pool_wise = i[23]
		else:
			pool_wise = ''

		invoice_list.append({
			'ship_name' 	 : ship_name,
			'voyage_no' 	 : voyage_no,
			'invoice_date' 	 : str(invoice_date),
			'invoice_amount' : invoice_amt,#invoices.invoice_amount,
			'recieved_date'  : str(rec_date),
			'client_address' : i[10],
			'payment_status' : i[11],
			'mail_to' 		 : i[12],
			'mail_cc' 		 : i[13],
			'mail_from'      : i[14],
			'disch_date'     : str(disch_date),
			'disch_port' 	 : i[16],
			'inr' 			 : i[17],
			'usd' 			 : i[18],
			'cancel_invoice' : i[6],
			'vm_name' 		 : i[5],
			'invoice_no' 	 : i[1],
			'client_name'  	 : client_name,
			'proj_name' 	 : i[9],
			'period' 		 : period,
			'invoice_id' 	 : i[1],
			'show_button'    : show_button,
			'icons_cancel'   : icons,
			'colors' 		 : colors,
			'url_pdf'		 : url_pdfx, #i[21],
			'client_price'   : total_amount,
			'total_igst_list': total_igst_list,
			'exchange_rate'  : exchange_rate,
			'tds' 			 : i[31],
			'invoice_remark' : remarks,
			'currency_type'  : i[37],
			'id'			 : i[0],
			'pool_types' 	 : i[23],
			'client_id'		 : i[24],
			'invoice_style'	 : invoice_style,
			'price_type' 	 : price_type,
			'price' 		 : price,
			'pool_wise' 	 : pool_wise,
			'img_logo'       : img_logo,
			})

	

	for cl in client_arr:
		client_list.append({
			'client_name' : cl,
			})

	try:
		format_max_date = max_date.strftime('%m/%d/%Y')
		format_min_date = min_date.strftime('%m/%d/%Y')
	except:
		format_max_date = ''
		format_min_date = ''
	
	context={
		'invoice_list' : invoice_list,
		'client_list'  : client_list,
		'max_date'     : str(format_max_date),
		'min_date'     : str(format_min_date),
	}
	return HttpResponse(json.dumps(context))

def update_rate_exchange(request):
	if request.user.is_authenticated():
		rate 	  	   = request.GET['rate']
		client_lt 	   = request.GET['client_lt']
		proj_name 	   = request.GET['proj_name']
		client_details = models.Client.objects.filter(proj_name=proj_name,client_name=client_lt).first()
		client_details.rate = rate
		client_details.save()

		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')

@csrf_exempt
def total_generated_chm_boss(request):
	invoice_details = models.invoice.objects.filter(inr='INR',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').order_by('invoice_no')
	invoice_array 	= []
	ship_array 		= []
	invoice_amt 	= ''
	s_no=1
	for i in invoice_details:
		if i.invoice_no not in ship_array:
			ship_array.append(i.invoice_no)

	for x in ship_array:
	 	invoices = models.invoice.objects.filter(invoice_no=x,inr='INR',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').first()
	 	counter  = models.invoice.objects.filter(invoice_no=x,inr='INR',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').count()
	 	if counter>1:
	 		voyage_no = ''
	 		if invoices.vessel_type!='None' and invoices.vessel_type!=None:	 			
	 			if invoices.vessel_type=='Teekay':
	 				ship_name  = invoices.ship_name
	 				voyage_no  = invoices.voyage_no
	 				disch_port = invoices.disch_port
	 				try:
			 			disch_date = invoices.disch_date.strftime('%d-%b-%Y')
			 		except:
			 			disch_date = ''
	 			else:
	 				ship_name  = str(invoices.vessel_type)+' Fleet'
	 				voyage_no  = ''
	 				disch_port = ''
	 				disch_date = ''
	 		else:
	 			ship_name  = ''
	 			disch_port = ''
	 			disch_date = ''
	 	else:
	 		voyage_no  = invoices.voyage_no
	 		ship_name  = invoices.ship_name
	 		disch_port = invoices.disch_port
	 		try:
	 			disch_date = invoices.disch_date.strftime('%d-%b-%Y')
	 		except:
	 			disch_date = ''

	 	invoice_date_for = invoices.invoice_date.date()
	 	format_invoice_date = invoice_date_for.strftime('%d-%b-%Y')
	 	if invoices.payment_status=='Paid':
	 		status 		= 'Paid'
	 		color 		= 'green'
	 		font_color  = 'white'
	 	elif invoices.payment_status=="Cancel":
	 		status = "Cancel"
	 		color = 'red'
	 		font_color  = 'white'
	 	elif invoices.payment_status==None:
	 		status = "Generated"
	 		color = ''
	 		font_color  = 'black'
	 	else:
	 		status = ''
	 		color  = ''
	 		font_color  = ''

		try:
			if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR':
				label = 'INR '
				if invoices.invoice_amount:
					invoice_amt = str(label)+str(invoices.invoice_amount)
				else:
					invoice_amt = ''

			elif invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD':
				label = 'USD '
				if invoices.invoice_amount:
					invoice_amt = str(label)+str(invoices.invoice_amount)
				else:
					invoice_amt = ''
		except ValueError:
			print '----'

		invoice_array.append({
			'invoice_no'  	: invoices.invoice_no,
			'invoice_date' 	: str(format_invoice_date),
			'vm_manager'  	: invoices.vm_name,
			'voyage_no'   	: voyage_no,
			'proj_name'   	: invoices.proj_name,
			's_no' 		  	: s_no,
			'ship_name'   	: ship_name,
			'disch_port'    : disch_port,
			'disch_date'    : str(disch_date),
			'client_name'   : invoices.client.client_name,
			'status' 		: status,
			'invoice_amount': invoice_amt,
			'color' 		: color,
			'font_color'    : font_color,
			})
		s_no+=1

	context={
	'invoice_array' : invoice_array
	}
	return HttpResponse(json.dumps(context))


@csrf_exempt
def total_generated_usd_only(request):
	invoice_details = models.invoice.objects.filter(usd='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').order_by('invoice_no')
	invoice_array 	= []
	ship_array 		= []
	invoice_amt = ''
	s_no=1
	for i in invoice_details:
		if i.invoice_no not in ship_array:
			ship_array.append(i.invoice_no)

	for x in ship_array:
	 	invoices = models.invoice.objects.filter(invoice_no=x,usd='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').first()
	 	counter  = models.invoice.objects.filter(invoice_no=x,usd='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').count()
	 	if counter>1:
	 		voyage_no = ''
	 		if invoices.vessel_type!='None' and invoices.vessel_type!=None:
	 			if invoices.vessel_type=='Teekay':
	 				ship_name  = invoices.ship_name
	 				voyage_no  = invoices.voyage_no
	 				disch_port = invoices.disch_port
	 				try:
			 			disch_date = invoices.disch_date.strftime('%d-%b-%Y')
			 		except:
			 			disch_date = ''
	 			else:
	 				ship_name  = str(invoices.vessel_type)+' Fleet'
	 				voyage_no  = ''
	 				disch_port = ''
	 				disch_date = ''
	 		else:
	 			ship_name  = ''
	 			disch_port = ''
	 			disch_date = ''
	 	else:
	 		voyage_no  = invoices.voyage_no
	 		ship_name  = invoices.ship_name
	 		disch_port = invoices.disch_port
	 		try:
	 			disch_date = invoices.disch_date.strftime('%d-%b-%Y')
	 		except:
	 			disch_date = ''

	 	invoice_date_for = invoices.invoice_date.date()
	 	format_invoice_date = invoice_date_for.strftime('%d-%b-%Y')
	 	if invoices.payment_status=='Paid':
	 		status 		= 'Paid'
	 		color 		= 'green'
	 		font_color  = 'white'
	 	elif invoices.payment_status=="Cancel":
	 		status = "Cancel"
	 		color = 'red'
	 		font_color  = 'white'
	 	elif invoices.payment_status==None:
	 		status = "Generated"
	 		color = ''
	 		font_color  = 'black'
	 	else:
	 		status = ''
	 		color  = ''
	 		font_color  = ''

		# if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR':
		# 	label = 'INR '
		# 	if invoices.invoice_amount:
		# 		invoice_amt = str(label)+str(invoices.invoice_amount)
		# 	else:
		# 		invoice_amt = ''

		try:
			if invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD':
				label = 'USD '
				if invoices.invoice_amount:
					invoice_amt = str(label)+str(invoices.invoice_amount)
				else:
					invoice_amt = ''
		except:
			pass

		try:
			client_details_name = invoices.client.client_name
		except:
			client_details_name = 'Nox'

		invoice_array.append({
			'invoice_no'  	: invoices.invoice_no,
			'invoice_date' 	: str(format_invoice_date),
			'vm_manager'  	: invoices.vm_name,
			'voyage_no'   	: voyage_no,
			'proj_name'   	: invoices.proj_name,
			's_no' 		  	: s_no,
			'ship_name'   	: ship_name,
			'disch_port'    : disch_port,
			'disch_date'    : str(disch_date),
			'client_name'   : client_details_name,
			'status' 		: status,
			'invoice_amount': invoice_amt,
			'color' 		: color,
			'font_color'    : font_color,
			})
		s_no+=1

	context={
	'invoice_array' : invoice_array
	}
	return HttpResponse(json.dumps(context))


@csrf_exempt
def total_paid_invoice(request):
	invoice_details = models.invoice.objects.filter(payment_status='Paid',inr='INR').order_by('invoice_no')
	invoice_array = []
	ship_array = []
	invoice_amt = ''
	s_no=1
	for i in invoice_details:
		if i.invoice_no not in ship_array:
			ship_array.append(i.invoice_no)

	for x in ship_array:
		invoices = models.invoice.objects.filter(invoice_no=x,inr='INR').first()
		counter   = models.invoice.objects.filter(invoice_no=x,inr='INR').count()
		if counter>1:
			voyage_no = ''
			if invoices.vessel_type!='None' and invoices.vessel_type!=None:
				ship_name = str(invoices.vessel_type)+' Fleet'
				disch_port = ''
				disch_date = ''
			else:
				ship_name = ''
				disch_port = ''
				disch_date = ''
		else:
			voyage_no = invoices.voyage_no
			ship_name = invoices.ship_name
			disch_port = invoices.disch_port
			try:
				disch_date = invoices.disch_date.strftime('%d-%b-%Y')
			except:
				disch_date = ''

		invoice_date_for = invoices.invoice_date.date()
		format_invoice_date = invoice_date_for.strftime('%d-%b-%Y')
		if invoices.payment_status=='Paid':
			status = 'Paid'
			color = 'green'
			font_color  = 'white'
		elif invoices.payment_status=="Cancel":
			status = "Cancel"
			color = 'red'
			font_color  = 'white'
		elif invoices.payment_status==None:
			status = "Generated"
			color = ''
			font_color  = 'black'
		else:
			status = ''
			color  = ''
			font_color  = ''

		if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
			label = 'INR '
			if invoices.invoice_amount:
				invoice_amt = str(label)+str(invoices.invoice_amount)
			else:
				invoice_amt = ''

		elif invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD' or invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
			label = 'USD '
			if invoices.invoice_amount:
				invoice_amt = str(label)+str(invoices.invoice_amount)
			else:
				invoice_amt = ''

		invoice_array.append({
			'invoice_no'  	: invoices.invoice_no,
			'invoice_date' 	: str(format_invoice_date),
			'vm_manager'  	: invoices.vm_name,
			'voyage_no'   	: voyage_no,
			'proj_name'   	: invoices.proj_name,
			's_no' 		  	: s_no,
			'ship_name'   	: ship_name,
			'disch_port'    : disch_port,
			'disch_date'    : str(disch_date),
			'client_name'   : invoices.client.client_name,
			'status' 		: status,
			'invoice_amount': invoice_amt,
			'color' 		: color,
			'font_color'    : font_color,
			})

		s_no+=1

	context={
	'invoice_array' : invoice_array
	}
	return HttpResponse(json.dumps(context))

@csrf_exempt
def total_paid_invoice_usd_only(request):
	invoice_details = models.invoice.objects.filter(payment_status='Paid',usd='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').order_by('invoice_no')
	invoice_array = []
	ship_array = []
	s_no=1
	invoice_amt = ''
	for i in invoice_details:
		if i.invoice_no not in ship_array:
			ship_array.append(i.invoice_no)

	for x in ship_array:
		invoices = models.invoice.objects.filter(invoice_no=x,usd='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').first()
		counter   = models.invoice.objects.filter(invoice_no=x,usd='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').count()
		if counter>1:
			voyage_no = ''
			if invoices.vessel_type!='None' and invoices.vessel_type!=None:
				ship_name = str(invoices.vessel_type)+' Fleet'
				disch_port = ''
				disch_date = ''
			else:
				ship_name = ''
				disch_port = ''
				disch_date = ''
		else:
			voyage_no = invoices.voyage_no
			ship_name = invoices.ship_name
			disch_port = invoices.disch_port
			try:
				disch_date = invoices.disch_date.strftime('%d-%b-%Y')
			except:
				disch_date = ''

		invoice_date_for = invoices.invoice_date.date()
		format_invoice_date = invoice_date_for.strftime('%d-%b-%Y')
		if invoices.payment_status=='Paid':
			status = 'Paid'
			color = 'green'
			font_color  = 'white'
		elif invoices.payment_status=="Cancel":
			status = "Cancel"
			color = 'red'
			font_color  = 'white'
		elif invoices.payment_status==None:
			status = "Generated"
			color = ''
			font_color  = 'black'
		else:
			status = ''
			color  = ''
			font_color  = ''

		# if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
		# 	label = 'INR '
		# 	if invoices.invoice_amount:
		# 		invoice_amt = str(label)+str(invoices.invoice_amount)
		# 	else:
		# 		invoice_amt = ''

		if invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD' or invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
			label = 'USD '
			if invoices.invoice_amount:
				invoice_amt = str(label)+str(invoices.invoice_amount)
			else:
				invoice_amt = ''

		invoice_array.append({
			'invoice_no'  	: invoices.invoice_no,
			'invoice_date' 	: str(format_invoice_date),
			'vm_manager'  	: invoices.vm_name,
			'voyage_no'   	: voyage_no,
			'proj_name'   	: invoices.proj_name,
			's_no' 		  	: s_no,
			'ship_name'   	: ship_name,
			'disch_port'    : disch_port,
			'disch_date'    : str(disch_date),
			'client_name'   : invoices.client.client_name,
			'status' 		: status,
			'invoice_amount': invoice_amt,
			'color' 		: color,
			'font_color'    : font_color,
			})

		s_no+=1

	context={
	'invoice_array' : invoice_array
	}
	return HttpResponse(json.dumps(context))

@csrf_exempt
def total_pending_invoice(request):
	invoice_details = models.invoice.objects.filter(payment_status=None,cancel_invoice='0',inr='INR',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').order_by('invoice_no')
	invoice_array 	= []
	ship_array 		= []
	invoice_amt = ''
	s_no=1
	for i in invoice_details:
		if i.invoice_no not in ship_array:
			ship_array.append(i.invoice_no)

	for x in ship_array:
		invoices = models.invoice.objects.filter(invoice_no=x,inr='INR',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').first()
		counter  = models.invoice.objects.filter(invoice_no=x,inr='INR',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').count()

		if counter>1:
			voyage_no = ''
			if invoices.vessel_type!='None' and invoices.vessel_type!=None:
				ship_name  = str(invoices.vessel_type)+' Fleet'
				disch_port = ''
				disch_date = ''
			else:
				ship_name  = ''
				disch_port = ''
				disch_date = ''
		else:
			voyage_no  = invoices.voyage_no
			ship_name  = invoices.ship_name
			disch_port = invoices.disch_port
			try:
				disch_date = invoices.disch_date.strftime('%d-%b-%Y')
			except:
				disch_date = ''

		invoice_date_for 	= invoices.invoice_date.date()
		format_invoice_date = invoice_date_for.strftime('%d-%b-%Y')
		if invoices.payment_status=='Paid':
			status     = 'Paid'
			color      = 'green'
			font_color = 'white'
		elif invoices.payment_status=="Cancel":
			status     = "Cancel"
			color      = 'red'
			font_color = 'white'
		elif invoices.payment_status==None:
			status = "Generated"
			color  = ''
			font_color  = 'black'
		else:
			status = ''
			color  = ''
			font_color  = ''

		if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
			label = 'INR '
			if invoices.invoice_amount:
				invoice_amt = str(label)+str(invoices.invoice_amount)
			else:
				invoice_amt = ''

		elif invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD' or invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
			label = 'USD '
			if invoices.invoice_amount:
				invoice_amt = str(label)+str(invoices.invoice_amount)
			else:
				invoice_amt = ''

		if invoices.proj_name=='BOSS':
			header_color = 'orange'
		elif invoices.proj_name=='CHM':
			header_color = 'black'

		invoice_array.append({
			'invoice_no'  	: invoices.invoice_no,
			'invoice_date' 	: str(format_invoice_date),
			'vm_manager'  	: invoices.vm_name,
			'voyage_no'   	: voyage_no,
			'proj_name'   	: invoices.proj_name,
			's_no' 		  	: s_no,
			'ship_name'   	: ship_name,
			'disch_port'    : disch_port,
			'disch_date'    : str(disch_date),
			'client_name'   : invoices.client.client_name,
			'status' 		: status,
			'invoice_amount': invoice_amt,
			'color' 		: color,
			'font_color'    : font_color,
			'header_color'  : header_color,
			})

		s_no+=1

	context={
	'invoice_array' : invoice_array
	}
	return HttpResponse(json.dumps(context))

@csrf_exempt
def total_pending_invoice_usd_only(request):
	invoice_details = models.invoice.objects.filter(payment_status=None,cancel_invoice='0',usd='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').order_by('invoice_no')
	invoice_array 	= []
	ship_array 		= []
	s_no=1
	invoice_amt = ''
	for i in invoice_details:
		if i.invoice_no not in ship_array:
			ship_array.append(i.invoice_no)

	for x in ship_array:
		invoices = models.invoice.objects.filter(invoice_no=x,usd='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').first()
		counter   = models.invoice.objects.filter(invoice_no=x,usd='USD',invoice_date__gte='2023-01-01',invoice_date__lte='2023-12-31').count()

		if counter>1:
			voyage_no = ''
			if invoices.vessel_type!='None' and invoices.vessel_type!=None:
				ship_name  = str(invoices.vessel_type)+' Fleet'
				disch_port = ''
				disch_date = ''
			else:
				ship_name  = ''
				disch_port = ''
				disch_date = ''
		else:
			voyage_no  = invoices.voyage_no
			ship_name  = invoices.ship_name
			disch_port = invoices.disch_port
			try:
				disch_date = invoices.disch_date.strftime('%d-%b-%Y')
			except:
				disch_date = ''

		invoice_date_for 	= invoices.invoice_date.date()
		format_invoice_date = invoice_date_for.strftime('%d-%b-%Y')
		if invoices.payment_status=='Paid':
			status     = 'Paid'
			color      = 'green'
			font_color = 'white'
		elif invoices.payment_status=="Cancel":
			status     = "Cancel"
			color      = 'red'
			font_color = 'white'
		elif invoices.payment_status==None:
			status = "Generated"
			color  = ''
			font_color  = 'black'
		else:
			status = ''
			color  = ''
			font_color  = ''

		# if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
		# 	label = 'INR '
		# 	if invoices.invoice_amount:
		# 		invoice_amt = str(label)+str(invoices.invoice_amount)
		# 	else:
		# 		invoice_amt = ''

		if invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD' or invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
			label = 'USD '
			if invoices.invoice_amount:
				invoice_amt = str(label)+str(invoices.invoice_amount)
			else:
				invoice_amt = ''

		if invoices.proj_name=='BOSS':
			header_color = 'orange'
		elif invoices.proj_name=='CHM':
			header_color = 'black'

		invoice_array.append({
			'invoice_no'  	: invoices.invoice_no,
			'invoice_date' 	: str(format_invoice_date),
			'vm_manager'  	: invoices.vm_name,
			'voyage_no'   	: voyage_no,
			'proj_name'   	: invoices.proj_name,
			's_no' 		  	: s_no,
			'ship_name'   	: ship_name,
			'disch_port'    : disch_port,
			'disch_date'    : str(disch_date),
			'client_name'   : invoices.client.client_name,
			'status' 		: status,
			'invoice_amount': invoice_amt,
			'color' 		: color,
			'font_color'    : font_color,
			'header_color'  : header_color,
			})

		s_no+=1

	context={
	'invoice_array' : invoice_array
	}
	return HttpResponse(json.dumps(context))

@csrf_exempt
def total_cancelled_invoice(request):
	invoice_details = models.invoice.objects.filter(payment_status='Cancel',inr='INR').order_by('invoice_no')
	invoice_array   = []
	ship_array      = []
	invoice_amt     = ''
	s_no 			= 1
	for i in invoice_details:
		if i.invoice_no not in ship_array:
			ship_array.append(i.invoice_no)

	for x in ship_array:
		invoices = models.invoice.objects.filter(invoice_no=x,inr='INR').first()
		counter  = models.invoice.objects.filter(invoice_no=x,inr='INR').count()
		if counter>1:
			voyage_no = ''
			if invoices.vessel_type!='None' and invoices.vessel_type!=None:
				ship_name  = str(invoices.vessel_type)+' Fleet'
				disch_port = ''
				disch_date = ''
			else:
				ship_name  = ''
				disch_port = ''
				disch_date = ''
		else:
			voyage_no  = invoices.voyage_no
			ship_name  = invoices.ship_name
			disch_port = invoices.disch_port
			try:
				disch_date = invoices.disch_date.strftime('%d-%b-%Y')
			except:
				disch_date = ''

		invoice_date_for    = invoices.invoice_date.date()
		format_invoice_date = invoice_date_for.strftime('%d-%b-%Y')
		if invoices.payment_status=='Paid':
			status = 'Paid'
			color = 'green'
			font_color  = 'white'
		elif invoices.payment_status=="Cancel":
			status = "Cancel"
			color = 'red'
			font_color  = 'white'
		elif invoices.payment_status==None:
			status = "Generated"
			color = ''
			font_color  = 'black'
		else:
			status = ''
			color  = ''
			font_color  = ''

		if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
			label = 'INR '
			if invoices.invoice_amount:
				invoice_amt = str(label)+str(invoices.invoice_amount)
			else:
				invoice_amt = ''

		elif invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD' or invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
			label = 'USD '
			if invoices.invoice_amount:
				invoice_amt = str(label)+str(invoices.invoice_amount)
			else:
				invoice_amt = ''

		if invoices.proj_name=='BOSS':
			header_color = 'orange'
		elif invoices.proj_name=='CHM':
			header_color = 'black'

		invoice_array.append({
			'invoice_no'  	: invoices.invoice_no,
			'invoice_date' 	: str(format_invoice_date),
			'vm_manager'  	: invoices.vm_name,
			'voyage_no'   	: voyage_no,
			'proj_name'   	: invoices.proj_name,
			's_no' 		  	: s_no,
			'ship_name'   	: ship_name,
			'disch_port'    : disch_port,
			'disch_date'    : str(disch_date),
			'client_name'   : invoices.client.client_name,
			'status' 		: status,
			'invoice_amount': invoice_amt,
			'color' 		: color,
			'font_color'    : font_color,
			'header_color'  : header_color,
			})

		s_no+=1

	context={
	'invoice_array' : invoice_array
	}
	return HttpResponse(json.dumps(context))

@csrf_exempt
def total_cancelled_invoice_usd_only(request):
	invoice_details = models.invoice.objects.filter(payment_status='Cancel',usd='USD').order_by('invoice_no')
	invoice_array = []
	ship_array = []
	s_no=1
	invoice_amt = ''
	for i in invoice_details:
		if i.invoice_no not in ship_array:
			ship_array.append(i.invoice_no)

	for x in ship_array:
		invoices = models.invoice.objects.filter(invoice_no=x,usd='USD').first()
		counter   = models.invoice.objects.filter(invoice_no=x,usd='USD').count()
		if counter>1:
			voyage_no = ''
			if invoices.vessel_type!='None' and invoices.vessel_type!=None:
				ship_name = str(invoices.vessel_type)+' Fleet'
				disch_port = ''
				disch_date = ''
			else:
				ship_name = ''
				disch_port = ''
				disch_date = ''
		else:
			voyage_no = invoices.voyage_no
			ship_name = invoices.ship_name
			disch_port = invoices.disch_port
			try:
				disch_date = invoices.disch_date.strftime('%d-%b-%Y')
			except:
				disch_date = ''

		invoice_date_for = invoices.invoice_date.date()
		format_invoice_date = invoice_date_for.strftime('%d-%b-%Y')
		if invoices.payment_status=='Paid':
			status = 'Paid'
			color = 'green'
			font_color  = 'white'
		elif invoices.payment_status=="Cancel":
			status = "Cancel"
			color = 'red'
			font_color  = 'white'
		elif invoices.payment_status==None:
			status = "Generated"
			color = ''
			font_color  = 'black'
		else:
			status = ''
			color  = ''
			font_color  = ''

		# if invoices.proj_name=='BOSS' and invoices.client.currency_type=='INR' or invoices.proj_name=='CHM' and invoices.client.currency_type=='INR':
		# 	label = 'INR '
		# 	if invoices.invoice_amount:
		# 		invoice_amt = str(label)+str(invoices.invoice_amount)
		# 	else:
		# 		invoice_amt = ''

		if invoices.proj_name=='BOSS' and invoices.client.currency_type=='USD' or invoices.proj_name=='CHM' and invoices.client.currency_type=='USD':
			label = 'USD '
			if invoices.invoice_amount:
				invoice_amt = str(label)+str(invoices.invoice_amount)
			else:
				invoice_amt = ''

		if invoices.proj_name=='BOSS':
			header_color = 'orange'
		elif invoices.proj_name=='CHM':
			header_color = 'black'

		invoice_array.append({
			'invoice_no'  	: invoices.invoice_no,
			'invoice_date' 	: str(format_invoice_date),
			'vm_manager'  	: invoices.vm_name,
			'voyage_no'   	: voyage_no,
			'proj_name'   	: invoices.proj_name,
			's_no' 		  	: s_no,
			'ship_name'   	: ship_name,
			'disch_port'    : disch_port,
			'disch_date'    : str(disch_date),
			'client_name'   : invoices.client.client_name,
			'status' 		: status,
			'invoice_amount': invoice_amt,
			'color' 		: color,
			'font_color'    : font_color,
			'header_color'  : header_color,
			})

		s_no+=1

	context={
	'invoice_array' : invoice_array
	}
	return HttpResponse(json.dumps(context))

import scp
import subprocess


def mail_log(request):
	if request.user.is_authenticated():
		mail_list 	= models.inbox_invoice_details.objects.all().order_by('invoice_no')
		mail_array 	= []
		login_user 	= request.user	
		for x in mail_list:
			client_details = models.Client.objects.filter(id=x.client.id).first()
			if client_details.proj_name=='BOSS':
				header_color = '#004471'
			elif client_details.proj_name=='CHM':
				header_color = '#ED741A'
			mail_array.append({
				'vessel_name' 	: x.vessel_name,
				'voy_no'		: x.voy_no,
				'invoice_no' 	: x.invoice_no,
				'invoice_amt' 	: x.invoice_amount,
				'invoice_date' 	: x.invoice_date,
				'client' 		: x.client.client_name,
				'mail_to' 		: x.mail,
				'mail_from' 	: x.mail_from,
				'mail_cc' 		: x.mail_cc,
				'sent_date' 	: x.sent_mail_date,
				'proj_name' 	: client_details.proj_name,
				'header_color' 	: header_color,
				})

		context={
		'mail_array' : mail_array,
		'login_user' : login_user
		}		
		return render_to_response("invoice_display/mail_log.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')


def select_client_for_pool(request):
	if request.user.is_authenticated():
		proj_name = json.loads(request.GET['proj_name'])
		client_details = models.Client.objects.filter(proj_name=proj_name)
		client_array = []
		for cl in client_details:
			client_array.append({
				'client_name' : cl.client_name
				})
		context={
		'client_array' : client_array
		}
		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')


def selected_currency_type_handler(request):
	if request.user.is_authenticated():
		invoice_details = ''
		currency_type = json.loads(request.GET['currency_type'])
		if currency_type=='USD':
			invoice_details = models.invoice.objects.filter(usd=currency_type)
		elif currency_type=='INR':
			invoice_details = models.invoice.objects.filter(inr=currency_type)
		client_array = []
		for x in invoice_details:
			client_name = x.client.client_name
			if client_name not in client_array:
				client_array.append(client_name)
		cl_list  = []
		for cl in client_array:
			if currency_type=='USD':
				cliend_id = models.invoice.objects.filter(client__client_name=cl,usd='USD').first()
			if currency_type=='INR':
				cliend_id = models.invoice.objects.filter(client__client_name=cl,inr='INR').first()
				#print '_______',cliend_id.id
			cl_list.append({
				'client_name' : cl,
				'cliend_id'   : cliend_id.id
				})
		context={
		'cl_list' : cl_list
		}

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')

@csrf_exempt
def vaild_clearlake_invoice_details(request):
	if request.user.is_authenticated():
		ship_name  			= json.loads(request.POST['ship_name'])
		start_dtt    		= json.loads(request.POST['start_dtt'])	
		client_name  		= json.loads(request.POST['client_name'])
		format_month_name   = datetime.strptime(start_dtt, "%m/%d/%Y").strftime('%B')
		format_year_name    = datetime.strptime(start_dtt, "%m/%d/%Y").strftime('%Y')

		remove_vessel_space = ship_name.replace('_', ' ')		 	
		client_details 		= models.Client.objects.filter(client_name=client_name,proj_name='BOSS').first()
		vessel_name 		= remove_vessel_space.strip()

		try:
			qry    = "SELECT * FROM it_invoice where proj_name='BOSS' and month_name='"+str(format_month_name)+"' and ship_name='"+str(vessel_name)+"' and cancel_invoice="'0'" and Year(month)='"+str(format_year_name)+"' and client_id='87'"
			
			#print qry
			cursor = connection.cursor()
			cursor.execute(qry)
			invoice_details = cursor.fetchall()
			for x in invoice_details:
				if x>0:
					display_button = 'none'
					shipname       = ship_name
				else:
					display_button = ''
					shipname       = ship_name

			context={
			'display_button' : display_button,
			'shipname'   	 : shipname,
			}	
		except:
			context={
			'display_button' : '',
			'shipname'   	 : '',
			}

		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')