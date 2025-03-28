from django.shortcuts import render
from django.shortcuts import render,render_to_response
from it import models
from django.http import HttpResponse
import json
from django.db.models import Count
from django.db import connection
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

from shutil import copyfile
import shutil

def welcome_chp_api(request):
	if request.user.is_authenticated():
		# api_url 	 = "http://0.0.0.0:8000/hb/get_chm_data/"
		# api_method   = "GET"
		# parameters   = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b"}
		# response     = requests.get(api_url, params=parameters)	
		# ch_array     = json.loads(response.content)
		# cl_array     = ch_array['cl_array']
		chm_append   = []

		# for ch in cl_array:			
		# 	check = models.Client.objects.filter(client_name=ch['client_name'],proj_name=ch['proj_name']).count()
		# 	if check>0:
		# 		save_client = models.Client.objects.filter(client_name=ch['client_name'],proj_name=ch['proj_name']).first()
		# 		print '___________update'
		# 	else:
		# 		save_client = models.Client()
		# 		print '___________insert'
		# 	save_client.price  			= ch['client_price']
		# 	save_client.client_name  	= ch['client_name']
		# 	save_client.price_type  	= ch['price_type']
		# 	save_client.currency_type  	= ch['curr_type']
		# 	save_client.duration_type  	= ch['dur_type']
		# 	save_client.rate  			= ch['price_rate']
		# 	save_client.proj_name  		= ch['proj_name']
		# 	save_client.save()
			
		client_details = models.Client.objects.all()
		for cl in client_details:
			if cl.client_name=='stena bulk' or cl.client_name=='Stena Weco':
				merge_type = 1	
			else:
				merge_type = 0

			chm_append.append({
			'client_id'    : cl.id,
			'client_price' : cl.price,
			'client_name'  : cl.client_name,
			'price_type'   : cl.price_type,
			'curr_type'    : cl.currency_type,
			'dur_type'	   : cl.duration_type,
			'price_rate'   : cl.rate,
			'proj_name'    : cl.proj_name,
			'merge_type'   : merge_type,
			'tin_number'   : cl.tin_number,
			})
		
		context={
		'chm_append' : chm_append,
		}
		return render_to_response("invoice_display/chm/welcome_fetch_chm.html",context)
	else:
		return HttpResponseRedirect('/it/user_login')


@csrf_exempt
def update_client_details(request):
	if request.user.is_authenticated():
		e_client_name  = request.POST['e_client_name']		
		e_rate_c 	   = request.POST['e_rate_c']
		customer_no    = request.POST['customer_no']
		e_proj_name    = request.POST['proj_name']
		clientID 	   = request.POST['clientID']
		e_price_c 	   = request.POST['e_price_c']
		price_type_c   = request.POST['price_type_c']			
		usd_inr 	   = request.POST['usd_inr']		
		save_client_db = models.Client.objects.filter(client_name=e_client_name,proj_name='CHM',id=clientID).first()			
		save_client_db.client_name   = e_client_name			
		save_client_db.currency_type = usd_inr
		save_client_db.duration_type = usd_inr
		save_client_db.price 		 = e_price_c				
		save_client_db.rate 		 = e_rate_c
		save_client_db.tin_number	 = customer_no	
		save_client_db.price_type    = price_type_c
		save_client_db.proj_name 	 = e_proj_name		
		save_client_db.save()
		
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')