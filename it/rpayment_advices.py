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

def rpayment_advices(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'admin':
		login_user  	= request.user		
		context={
		'login_user'  : login_user
		}

		#print '--------',client_array
		return render_to_response("invoice_display/rpayment_advices.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')



def get_client_list(request):	
	qry 			= "SELECT client_name,proj_name,currency_type,id FROM invoice.it_client where status='1' group by client_name,proj_name,currency_type;"
	cursor 			= connection.cursor()
	cursor.execute(qry)
	#print qry
	client_details 	= cursor.fetchall()
	client_array 	= []
	for f in client_details:			
		client_array.append({
			'cl_id'	  : f[3],
			'client'  : str(f[0])+' - '+str(f[1])+' - '+str(f[2]),
			'cl_name' : f[0],
		})

	return HttpResponse(json.dumps(client_array))

def insert_payment_advise(request):
	datas 	= json.loads(request.GET['datas'])
	for c in datas:
		if c['client_name']!=None:
			split_client_name 	= c['client_name'].split('-')
			cl_client_name 		= split_client_name[0].strip()

			try:
				cl_proj_name 	= split_client_name[1].strip()
			except:
				return HttpResponse(json.dumps('empty'))

			cl_currency_type 	= split_client_name[2].strip()
			inward_nos 			= c['inward_no']
			inward_date 		= c['date']
			inward_amount 		= c['fcy_amount']
			inward_remarks 		= c['remarks']
			inward_rate 		= c['rate']

			qry1 				= 'SELECT id FROM invoice.it_client where status="1" and proj_name="'+str(cl_proj_name)+'" and currency_type="'+str(cl_currency_type)+'" and client_name="'+str(cl_client_name)+'";'
			cursor 				= connection.cursor()
			cursor.execute(qry1)			
			get_client_id 		= cursor.fetchall()
			client_id 			= int(get_client_id[0][0])
			#print '------',type(client_id)
			CHK = models.master_inw_data.objects.filter(inward_no=inward_nos).count()
			if CHK!=0:
				db = models.master_inw_data.objects.filter(inward_no=inward_nos).first()
				return HttpResponse(json.dumps('alert'))
			else:
				db = models.master_inw_data()

			db.txn_date   	= inward_date 
			db.amount     	= inward_amount
			db.currency 	= cl_currency_type
			db.proj_name 	= cl_proj_name
			db.client_id_id	= int(client_id)
			db.remarks  	= inward_remarks
			db.rate 		= inward_rate
			db.entry_date 	= datetime.now().date()
			db.inward_no 	= inward_nos
			db.save()

			m_chk  			= models.remittance_data.objects.filter(certificate_no=inward_nos).count()	
			if m_chk!=0:
				m_update	= models.remittance_data.objects.filter(certificate_no=inward_nos).first()
			else:
				m_update	= models.remittance_data()
			
			m_update.rate 				= inward_rate	
			m_update.remarks 			= inward_remarks
			m_update.currency 			= cl_currency_type
			m_update.client_id 			= client_id #n_client_name
			m_update.total_amount 		= inward_amount
			m_update.inward_amount 		= inward_amount
			m_update.certificate_no 	= inward_nos
			m_update.net_amount_ref 	= inward_amount
			m_update.remittance_date 	= inward_date
			m_update.entry_date 		= datetime.now().date()
			m_update.save()		
	

	return HttpResponse(json.dumps('done'))