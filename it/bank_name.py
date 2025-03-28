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




def bank_name(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'admin':
		login_user 	= request.user

		client_list = models.Client.objects.filter(status=1).order_by('client_name')
		cl_list 	= []
		cl_array = []
		for c in client_list:
			if c.client_name not in cl_array:
				cl_array.append(c.client_name)
			
		for x in cl_array:
			client_t = models.Client.objects.filter(client_name=x).order_by('client_name').first()			
			cl_list.append({
					'id' 		  : client_t.id,				
					'client_name' : client_t.client_name+' - '+str(client_t.currency_type)+' - '+str(client_t.proj_name)
					})

		
		bank_list = models.bank_name.objects.all()
		bnk_list  = []
		for t in bank_list:			
			try:
				client_id 		= t.client_id
				client_name		= t.client_id.client_name
				proj_name       = t.client_id.proj_name 
			except:
				client_id 		= ''
				client_name		= ''
				proj_name 		= ''	
		

			bnk_list.append({
				'id' 			: t.id,
				'bank_address1' : t.bank_address1,
 				'swift_code1'  	: t.swift_code1,
 				'account_name1' : t.account_name1,
 				'account_no1'  	: t.account_no1,
 				'contact_no1'  	: t.contact_no1,
 				'bank_address2' : t.bank_address2,
 				'swift_code2'  	: t.swift_code2,
 				'account_name2' : t.account_name2,
 				'account_no2'  	: t.account_no2,
 				'contact_no2'  	: t.contact_no2,
 				'client_name' 	: client_name,
 				'bank_name'		: t.bank_name,
 				'proj_name'		: proj_name,
 				'client_id' 	: client_id,
 				})


		context={
			'cl_list'  	 : cl_list,
			'bnk_list' 	 : bnk_list,
			'login_user' : login_user,	
		}
		
		return render_to_response("invoice_display/bank_name.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')


def update_bank_entry(request):
	e_id    		= json.loads(request.GET['e_id'])
	e_client_id   	= json.loads(request.GET['e_client_name'])
	e_bank_name1    = json.loads(request.GET['e_bank_name1'])
	e_bank_address1 = json.loads(request.GET['e_bank_address1'])
	e_account_no1   = json.loads(request.GET['e_account_no1'])
	e_account_name1 = json.loads(request.GET['e_account_name1'])
	e_account_no1   = json.loads(request.GET['e_account_no1'])
	e_swift_code1   = json.loads(request.GET['e_swift_code1'])
	e_bank_name2    = json.loads(request.GET['e_bank_name2'])
	e_bank_address2 = json.loads(request.GET['e_bank_address2'])
	e_account_name2 = json.loads(request.GET['e_account_name2'])
	e_account_no2   = json.loads(request.GET['e_account_no2'])
	e_swift_code2   = json.loads(request.GET['e_swift_code2'])

	
	ubank 				= models.bank_name.objects.filter(id=e_id).first()	
	ubank.client_id 	= e_client_id
	ubank.bank_address1 = e_bank_address1
	ubank.swift_code1   = e_swift_code1
	ubank.account_name1 = e_account_name1
	ubank.account_no1   = e_account_no1
	#ubank.contact_no1   = 
	ubank.bank_address2 = e_bank_address2
	ubank.swift_code2   = e_swift_code2
	ubank.account_name2 = e_account_name2
	ubank.account_no2   = e_account_no2
	#ubank.contact_no2   = 
	#ubank.save()

	return HttpResponse(json.dumps('done'))