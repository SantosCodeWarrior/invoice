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
import os
from it.forms import DocumentForm

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

def upload_files(request):
	if request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'admin':
		login_user  = request.user
		context={
			'login_user' : login_user,			
		}	
		return render_to_response("upload.html",context)	
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')

@csrf_exempt
def submit_upload_images(request):
	if request.method == 'POST':
		x=0
		for f in request.FILES:
			tag  			= request.POST['tag']		
			form 			= DocumentForm(request.POST,request.FILES)
			image_name  	= request.FILES[f]
			split 			= tag.split('_')
			#print '-----',split[0],'----',split[1]
			# if split[1]=='b':
			# 	flag = split[0]
			img  = models.master_inw_data.objects.filter(inward_no=tag).first()
			geID = tag
			# if split[1]=='r':
			# 	flag = split[0]
			# 	img  = models.master_inw_data.objects.filter(id=flag).first()
			# 	geID = None

				
			#split_png 		= str(image_name).split('.')			
			png 			= str(img.inward_no)+'.png'
			img.image_file 	= image_name
			img.file_name 	= png
			img.inward_no 	= geID
			img.get_path 	= '/var/www/html/invoice/it/static/Advice_images/'+str(png)			
			img.save()

			from_files 		= '/var/www/html/invoice/it/static/Advice_images/'+str(image_name)
			change_files 	= '/var/www/html/invoice/it/static/Advice_images/'+str(png)			
			os.rename(from_files, change_files)
			x+=1

			username   	= "BWTW059"
			password   	= "sandeep@123"
			clientname  = "OHMSERVER"
			servername  = "OHMSERVER"
			domain 	   	= 'WORKGROUP'
			ipaddress  	= "172.16.5.100"
			conn 	   	= SMBConnection(username,password,clientname,servername,domain,use_ntlm_v2=True, sign_options=2, is_direct_tcp=True)
			conn.connect(ipaddress,445)
			Shares 		= conn.listShares()
			share_name  = Shares[5].name
			print '---------',share_name 	
			
				
			path_name  = 'Finance/Current/Finance/Advice_images/'
			sharedfiles = conn.listPath(share_name,path_name)	

			with open("/var/www/html/invoice/it/static/Advice_images/"+str(png), 'rb') as file:
				conn.storeFile('Finance',"Finance/Current/Finance/Advice_images/"+str(png), file)	 
				
			conn.close()
		return render_to_response('upload.html',{'form': form},context_instance=RequestContext(request))
	return HttpResponse(json.dumps('Done'))


# @csrf_exempt
# def submit_upload_images(request):
# 	if request.method == 'POST':
# 		x=0
# 		for f in request.FILES:
# 			tag  			= request.POST['tag']		
# 			form 			= DocumentForm(request.POST,request.FILES)
# 			image_name  	= request.FILES[f]
# 			split 			= tag.split('_')
# 			#print '-----',split[0],'----',split[1]
# 			if split[1]=='b':
# 				flag = split[0]
# 				img  = models.master_inw_data.objects.filter(bank_id=flag).first()
# 				geID = flag
# 			if split[1]=='r':
# 				flag = split[0]
# 				img  = models.master_inw_data.objects.filter(id=flag).first()
# 				geID = None

				
# 			split_png 		= str(image_name).split('.')			
# 			png 			= str(img.bank_id)+'.'+str(split_png[1])
# 			img.image_file 	= image_name
# 			img.file_name 	= png
# 			img.bank_id 	= geID
# 			img.get_path 	= '/var/www/html/invoice/it/static/Invoice_Images/'+str(png)			
# 			img.save()

# 			from_files 		= '/var/www/html/invoice/it/static/Invoice_Images/'+str(image_name)
# 			change_files 	= '/var/www/html/invoice/it/static/Invoice_Images/'+str(png)			
# 			os.rename(from_files, change_files)
# 			x+=1
# 		return render_to_response('upload.html',{'form': form},context_instance=RequestContext(request))
# 	return HttpResponse(json.dumps('Done'))