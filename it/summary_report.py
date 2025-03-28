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


def summary_report(request):
	name				= ''
	ship_type 			= ''
	start_date_format	= ''
	api_url 		    = "https://bossv2.bwesglobal.com/api/get_data_boss/"
	#api_url 		    = "http://0.0.0.0:8004/api/get_data_boss/"
	api_method          = "GET"
	parameters          = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'name': '','ship_type':'','start_date':'','end_date': ''}
	response            = requests.get(api_url, params=parameters,verify=False)
	report_array        = json.loads(response.content)
	summary_array       = report_array['sh_array']
	summary_list 		= []
	
	for c in summary_array:
		show_details = models.Client.objects.filter(client_name=c['client_name'],status=1).count()		
		if show_details>0:
			try:
				redeliver_date = c['redeliver_date']
			except:
				redeliver_date = ''

			try:
				entry_date = c['entry_date']
			except:
				entry_date = ''
			
			summary_list.append({
				'id'  			 : c['id'],
				'ship_name' 	 : c['ship_name'],
				'account_name'   : c['account_name'],
				'redeliver_date' : str(redeliver_date),
				'entry_date'     : entry_date,
				'client_name'    : c['client_name'],			
				})

	context={
		'summary_list' : summary_list
	}	
	return render_to_response("invoice_display/summary_report.html",context)
	

@csrf_exempt
def summary_details_export(request):
	summary_details = json.loads(request.POST['summary_details'])
	for c in summary_details:		
		client_name  	= c['Client Name']
		vessel_name  	= c['Vessel Name']
		entry_date   	= c['Ship Entry Date']
		account_name 	= c['Account Name']
		redeliver_date 	= c['Redelivered Date']
		



	return HttpResponse(json.dumps('done'))