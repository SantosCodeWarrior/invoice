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

@csrf_exempt
def bank_statement(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'admin':
		login_user  = request.user
		get_bnk_det = models.bank_name.objects.filter(id=2).first()
		bnk_det 	= models.bank_statement_inr.objects.all()
		bnk_array   = []
		for c in bnk_det:
			txn_dte = datetime.strptime(str(c.txn_date), "%Y-%m-%d").strftime('%d-%b-%Y')
			
			bnk_array.append({
				'id'			: c.id,
				'descs'			: c.descs,
				'txn_date' 		: c.txn_date,
				'amount_inr'	: c.amount_inr,
				'gt_tx_date'	: str(txn_dte),
				'referencez'   	: c.referencez,
				'reference_no'  : c.reference_no,
				'stxn_date'		: str(c.txn_date),
				})


		context={
		'login_user' 	: login_user,
		'bank_name'		: get_bnk_det.bank_name,
		'bnk_array'		: bnk_array,
		}	

		return render_to_response("invoice_display/bnk_statement.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')



def bank_entry_inr(request):	
	tabs_name=json.loads(request.GET['tabs_name'])	
	
	for t in tabs_name:			
		check = models.bank_statement_inr.objects.filter(id=t['id']).count()		
		print '-----',check
		if check>=1:
			bnk = models.bank_statement_inr.objects.filter(id=t['id']).first()
			print '----update hoga'
		else:		
			bnk = models.bank_statement_inr()
			print '-----insert hoga'

		if t['amt_inr']!=None or t['descs']!=None or t['reference_no']!=None or t['bank_name']!=None or t['txn_date']!=None:# or t[6]!=None: # or t[6]!=None:
			
			try:
				txn_dates = datetime.strptime(t['txn_date'], "%d-%b-%Y").strftime('%Y-%m-%d')
			except:
				txn_dates = datetime.strptime(t['txn_date'], "%d-%m-%Y").strftime('%Y-%m-%d')
			
			get_split = t['descs'].split(' ')
			
			
			try:
				bnk.txn_date = str(txn_dates)
			except:
				bnk.txn_date = ''
			

			bnk.descs		   	= t['descs']
			bnk.amount_inr	   	= t['amt_inr']			
			bnk.referencez 		= get_split[2]
			bnk.reference_no    = t['reference_no']
			bnk.bank_name	   	= 'HDFC'			
			bnk.save()	
			
	
	return HttpResponse(json.dumps("done"))

@csrf_exempt
def bank_details_inr(request):
	bank_details = models.bank_statement_inr.objects.filter(bank_name='HDFC')
	bnk_array 	 = []
	s_no 		 = 1
	for x in bank_details:
		
		if x.d_c=='D' or x.d_c=='d':			
			html = ''				
		else:
			html = '<a href="/it/master_inv/?BANKID='+str(x.id)+'" target="_blank">View</a>',				
		
		try:
			txn_date = x.txn_date.strftime("%d-%b-%Y")
		except:
			txn_date = ''
		

		try:
			calc 		= x.descs.split('USD')
			extra_split = calc[1]		
			extra_calc 	= extra_split.split('@')
			price 		= extra_calc[0]
			rate 		= extra_calc[1]
			total_amt   = (Decimal(price)*Decimal(rate))
		except:
			extra_split = ''
			extra_calc  = ''			
			total_amt   = ''

		bnk_array.append({
			'id'			  : False,
			'html'		  	  : html,
			's_no' 		 	  : x.id,
			'txn_date'   	  : str(txn_date),
			'descs'   	 	  : x.descs,
			'amt_inr' 	  	  : x.amount_inr,
			'd_c'		 	  : x.d_c,
			'amount_balance'  : x.amount_balance,
			'referencez'	  : x.referencez,
			'bank_name'		  : x.bank_name,
			'reference_no' 	  : x.reference_no,			
		})
		s_no+=1

	context={
		'bnk_array'  : bnk_array,
	}
	return HttpResponse(json.dumps(context))

@csrf_exempt
def delete_bank_details(request):
	bank_details = json.loads(request.POST['bank_details'])		
	for x in bank_details:
		if x!=None:
			if x[0]==True:				
				models.bank_statement_inr.objects.filter(id=x[8]).delete()
				return HttpResponse(json.dumps('delete'))		
			elif x[8]==False:
			 	return HttpResponse(json.dumps('check'))
			else:
				pass
	
	return HttpResponse(json.dumps('done'))


def update_bank_statement_inr(request):
	x_idx  		 	= json.loads(request.GET['x_idx'])
	x_descs  		= json.loads(request.GET['x_descs'])
	x_txn_date  	= json.loads(request.GET['x_txn_date'])
	x_amount_inr  	= json.loads(request.GET['x_amount_inr'])
	x_referencez  	= json.loads(request.GET['x_referencez'])
	x_reference_no  = json.loads(request.GET['x_reference_no'])
	print '----------->>>>',x_idx

	db 				=  models.bank_statement_inr.objects.filter(id=x_idx).first()	
	db.descs 		= x_descs
	db.txn_date     = x_txn_date
	db.amount_inr   = x_amount_inr
	db.referencez   = x_referencez 
	db.reference_no = x_reference_no
	db.save()
	return HttpResponse(json.dumps('done'))

def delete_bank_statement_inr(request):
	x_idx  		 	= json.loads(request.GET['x_idx'])
	models.bank_statement_inr.objects.filter(id=x_idx).delete()
	return HttpResponse(json.dumps('done'))