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
import json
from pathlib import Path

def filter_for_json_data(request):
	if request.user.is_authenticated():
		login_user 			= request.user
		json_array 			= []
		json_data  			= models.json_data.objects.all().order_by('-id')
		dtate 				= datetime.now().date()
		year_name			= datetime.strptime(str(dtate), "%Y-%m-%d").strftime('%Y') #2021
		month_number 		= datetime.strptime(str(dtate), "%Y-%m-%d").strftime('%m')
		day_number 			= datetime.strptime(str(dtate), "%Y-%m-%d").strftime('%d')
		month_no 			= int(month_number)-1  #12
		if month_no<10:
			month_str = "0"+str(month_no)
		else:
			month_str = month_no
		start_date  = year_name+'-'+str(month_str)+'-01'
		
		try:
			get_month   = monthrange(int(year_name),int(month_str))[1]
			end_date    = str(year_name)+'-'+str(month_str)+'-'+str(get_month)	
			Start_Date1 = datetime.strptime(str(start_date),"%Y-%m-%d").strftime('%m/%d/%Y')
			End_Date1   = datetime.strptime(str(end_date),"%Y-%m-%d").strftime('%m/%d/%Y')
		except:
			Start_Date1 = '2023-12-01'
			End_Date1   = '2023-12-31'
		
		#print '---------',start_date,'------',end_date
		for c in json_data:
			#print '-----',c.upload_date,'---',c.file_name
			try:
				size1 		  	= os.path.getsize(c.file_name)				
				file_size(str(size1))
				get_file_size1 	= convert_bytes(size1)	
			except:
				get_file_size1 = ''

			split_file 		= c.file_name.split('/')
			file_namex 		= split_file[7]
			json_array.append({
				'upload_date' : c.upload_date,
				'file_name'   : file_namex,
				'file_size'   : get_file_size1,
				})
		client_list = models.Client.objects.filter(status=1,proj_name='BOSS')

		context={
			'json_data'  : json_array,
			'Start_Date' : Start_Date1,
			'End_Date'   : End_Date1,
			'login_user' : login_user,
			'client_list': client_list,
		}
		return render_to_response("invoice_display/json_data.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')


@csrf_exempt
def get_json_data(request):
	import re 
	if request.user.is_authenticated():
		start_date 			= json.loads(request.POST['start_date'])
		end_date 			= json.loads(request.POST['end_date'])
		static_data 		= json.loads(request.POST['static_data'])
		
		voyage_data 		= json.loads(request.POST['voyage_data'])
		try:
			client_ID 	 	= json.loads(request.POST['client_id'])
			client_name 	= json.loads(request.POST['client_name'])			
		except:
			client_ID   	= None
			client_name 	= None

		start_date_format 	= datetime.strptime(start_date, "%m/%d/%Y").strftime('%Y-%m-%d')
		end_date_format 	= datetime.strptime(end_date, "%m/%d/%Y").strftime('%Y-%m-%d')
		#print '--------->>',client_name
		
			
		api_urlx 		= "https://bossv2.bwesglobal.com/api/get_static_details/"		
		api_methodx     = "GET"			
		parametersx     = {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'name': '','ship_type':'','start_date':str(start_date_format),'end_date': str(end_date_format)}
		responsex       = requests.get(api_urlx, params=parametersx,verify=False)		
		client_listx    = json.loads(responsex.content)
		cl_dets 		= client_listx['ship_details']
		error 			= 'Done'

		for key in cl_dets:			
			if cl_dets[key]["clients_id"][0]==63:
				account_tab = cl_dets[key]["account_tab"]				
			else:
				account_tab = cl_dets[key]["account_tab"]

			
			patn 			= re.sub(r"[\([{})\]]", "", str(cl_dets[key]["clients_id"]))			
			ship_id     	= cl_dets[key]["id"]
			client_id   	= patn	
			ship_name   	= cl_dets[key]["ship_name"]
			db1				= models.api_client_data()
			db1.account_tab = account_tab			 				 	
			db1.ship_name   = ship_name
			db1.address 	= cl_dets[key]["address"]
			db1.client_id 	= str(patn)
			db1.ship_id     = ship_id			 	
			db1.save()
			#print '----------',cl_dets[key]["clients_id"]

		#print '--------',client_name
		try:
			if client_name =='Reliance':
				clID = 66
			
			elif client_name =='8520':
				clID = 59
			
			elif client_name=='15576':
				clID = 113
			
			elif client_name=='Sakhalin Energy':
				clID = 120
			
			elif client_name=='Ardmore':
				clID = 111
			
			elif client_name =='Apeejay':
				clID = 107
			
			elif client_name =='Dynagas Ltd':
				clID = 128
			
			elif client_name =='42':
				clID = 17
			
			elif client_name =='20002':
				clID = 136

			elif client_name =='15578':
				clID = 120

			elif client_name =='20007':
				clID = 131

			elif client_name =='20005':
				clID = 132

			elif client_name =='20011':
				clID = 135				
			else:
				clID = client_ID
		except:
			pass
		
		try:
			if client_name==63:
				billing_type = 'monthly_flat'
			if client_name==112:
				billing_type = 'monthly_prorated'
			if client_name=='Apeejay' or client_name=='15576':
				billing_type = 'voyage_eop'	
			else:
				billing_type = 'monthly_prorated'

			
			api_url1 			= "https://aboss.bwesglobal.com/api/get_ship_to_be_billed/"		
			api_method1      	= "GET"			
			parameters1      	= {'key' : "938e67ec-e20f-408b-9bd5-5913bfdc1d7b",'client_id': clID,'billing_date':str(start_date_format),'billing_type': billing_type}
			response1        	= requests.get(api_url1, params=parameters1,verify=False)		
			voyage_list     	= json.loads(response1.content)	
			#print '-------',clID,'----',parameters1
		except:
			pass
		

		try:
			models.vessel_billing_day.objects.all().delete()
			models.merge_billing_day.objects.all().delete()
		except:
			pass	

		
		today 	= datetime.now().date()		
		year    = datetime.strptime(str(today), "%Y-%m-%d").strftime('%Y')
		d1    	= str(today).split('-')
		d2 		= int(d1[1])-1		
		d3 		= d2

		if d3<10:
			tag = '0'+str(d3)
		else:
			tag = d3

		start_date = str(year)+'-'+str(tag)+'-01'
		try:
			get_month  = monthrange(int(year),int(tag))[1]
		except:
			get_month = 31
		
		end_date2  = str(year)+'-'+str(tag)+'-'+str(get_month)		
		
		#print '---------',get_month
		if static_data!=1:
			for c in voyage_list:
				end_format2  	= datetime.strptime(str(c['End Date']),"%d %b %Y").strftime('%Y-%m-%d')
				start_format2 	= datetime.strptime(str(c['Start Date']),"%d %b %Y").strftime('%Y-%m-%d')	
				#if start_format2>='2023-04-15' and end_format2<='2023-04-30':
				#print '--------',start_format2,'-----',end_format2
				if billing_type=='monthly_flat':
					end_format1  = ""#datetime.strptime(str(c['End Date']),"%d %b %Y").strftime('%Y-%m-%d')
					ship_name 	 = c['Ship Name']
					client_name  = c['Client Name']
					last_port  	 = ''#c['Last Port']
					no_of_day 	 = ''#c['No. of Days']
					voyage_id 	 = ''#c['voyage_id']
					first_port 	 = ''#c['First Port']
					ship_id 	 = c['Ship Id']
			 	else:
					end_format1  = datetime.strptime(str(c['End Date']),"%d %b %Y").strftime('%Y-%m-%d')
					ship_name 	 = c['Ship Name']
					client_name  = c['Client Name']
					last_port  	 = c['Last Port']
					no_of_day 	 = c['No. of Days']
					voyage_id 	 = c['voyage_id']
					first_port 	 = c['First Port']
					ship_id 	 = c['Ship Id']
									

				
				db  = models.vessel_billing_day()
				try:
					if billing_type=='monthly_flat':
						start_format = ""
						end_format   = ""
					else:
						start_format = datetime.strptime(str(c['Start Date']),"%d %b %Y").strftime('%Y-%m-%d')
						end_format 	 = datetime.strptime(str(c['End Date']),"%d %b %Y").strftime('%Y-%m-%d')	
				except:
					start_format  = ""
					end_format    = ""			
				
			 	
			 	#account_list      = models.api_client_data.objects.filter(ship_name=ship_name,client_id="["+str(clID)+"]").first()
			 	
			 	account_list      = models.api_client_data.objects.filter(ship_name=ship_name,client_id=clID).first()			
			 	db.ship_name 	  = ship_name			
			 	db.no_of_day 	  = no_of_day
			 	db.client_id 	  = clID
			 	db.first_port 	  = first_port
			 	db.last_port 	  = last_port
			 	db.client_name 	  = client_name
			 	db.ship_id 		  = ship_id			 
			 	
				try:
					acc_tb = account_list.account_tab	
				except:
					acc_tb = None			 	
				
				if billing_type=='monthly_flat':
					db.start_date = str(start_format) #"2022-02-01"
					db.end_Date   = str(end_format)   #"2022-02-28"
				else:
					db.start_date = str(start_format)
					db.end_Date   = str(end_format)
				db.voyage_id      = voyage_id

				if client_name==112:
					db.account_tab = client_name
				# elif client_name=='Clearlake':
				# 	db.account_tab = client_name
				elif client_name==115:
					db.account_tab = client_name
				elif client_name==111:
					db.account_tab = client_name
				elif client_name==106:
					db.account_tab = client_name
				# elif client_name=='Ultranav':
				# 	db.account_tab = client_name
				elif client_name==64:
					try:
						db.account_tab = acc_tb
					except:
						db.account_tab = acc_tb				
				else:
					if client_name==8520:
						try:
							if account_list.account_tab!=None:
								db.account_tab = account_list.account_tab
							else:
								db.account_tab = client_name	
						except:							
							db.account_tab = client_name
					else:				
						db.account_tab = client_name #account_list.account_tab	
				db.save()

			print '--------',client_name		
				

			QUERY  		= "SELECT sum(end_Date-start_date),ship_name,account_tab,last_port,max(end_Date) FROM invoice.it_vessel_billing_day where client_name='"+str(client_name)+"' group by ship_name;"
			
			cursor 		= connection.cursor()
			cursor.execute(QUERY)		
			day_details = cursor.fetchall()
			for t in day_details:
				sum_of_days = t[0]
				vessel_name = t[1]
				acc_tab     = t[2]
				last_port   = t[3]		
				end_dates   = t[4]
				cl_name 	= client_name
				models.merge_billing_day.objects.filter(client_name=client_name,ship_name=vessel_name).delete()
				eDB 		= models.merge_billing_day.objects.filter(client_name=client_name,ship_name=vessel_name).count()
				if eDB>1:
					dbms = models.merge_billing_day.objects.filter(client_name=client_name,ship_name=vessel_name).first()
				else:
					dbms = models.merge_billing_day()

				try:
					get_port_name = models.vessel_billing_day.objects.filter(end_Date=end_dates,client_name=client_name,ship_name=vessel_name).first()
					last_name 	  = get_port_name.last_port
				except:
					last_name 	  = ''

				dbms.no_of_day    = int(sum_of_days)+1
				dbms.ship_name    = vessel_name
				dbms.client_name  = client_name
				dbms.port_name    = last_name
				dbms.noon_date    = end_dates
				
				try:
					dbms.account_tab = acc_tab
				except:
					dbms.account_tab = None			
				dbms.save()

			for c1 in voyage_list:		
				ship_namec 	 = c1['Ship Name']
				vessel_details = models.vessel_billing_day.objects.filter(ship_name=ship_namec).count()			
				for c2 in range(0,vessel_details):
					# if c2>1:
					# 	ac2 = 1
					# else:
					# 	ac2 = 1
					st 			= models.vessel_billing_day.objects.filter(ship_name=ship_namec).first()
					st.status  	= c2				
					st.save()

		return HttpResponse(json.dumps('Done'))
	else:
		return HttpResponseRedirect('/it/user_login')


def convert_bytes(num):   
	for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:		
		if num < 1024.0:			
			return "%3.1f %s" % (num,x)
		num = num/1024.0


def file_size(file_path):    
	if os.path.isfile(file_path):
		file_info = os.stat(file_path)
		return convert_bytes(file_info.st_size)



@csrf_exempt
def voyage_data(request):
	if request.user.is_authenticated():
		# cl_id 			= request.POST['select_client']
		# cl_state_date 	= json.loads(request.POST['start_datex'])
		# cl_end_date 		= json.loads(request.POST['end_datex'])
		# cl_details		= models.boss_client.objects.filter(id=cl_id,proj_name='BOSS').first()
		voyage_array 		= []
		#get_voyage_details = models.merge_billing_day.objects.filter()
		s_no 				= 0
		get_voyage_details 	= models.vessel_billing_day.objects.all()
		for t in get_voyage_details:			
			if t.client_id==83 or t.client_id==113:				
				voyage_array.append({
					'sno' 		: s_no,
					'report'	: t.voyage_id,
					'ship_name' : t.ship_name,
					'route'     : str(t.first_port)+'-'+str(t.last_port),
					'first_row'	: '',
					'sec_row' 	: '',
				})
			else:				
				if t.status!=None:						
					sno 	  = s_no+1
					ship_name = t.ship_name
					s_no+=1
				else:
					sno       = ''
					ship_name = ""


				voyage_array.append({
				'first_row' : 2, #for hide
				'sec_row'   : 3, #for hide
				'route'     : "",
				'report'	: "",
				's_no' 		: sno,
				'ship_name' : ship_name,
				'to'		: t.last_port,
				'from'      : t.first_port,
				'to_date'	: str(t.end_Date),
				'from_date' : str(t.start_date),

			})
			
			
		try:
			first_hidden_column 	= int(voyage_array[0]['first_row'])
		except:
			first_hidden_column = 0

		try:
			second_hidden_column 	= int(voyage_array[0]['sec_row'])
		except:
			second_hidden_column = 0
		
		context={
		'voyage_array'   		: voyage_array,
		'first_hidden_column'  	: first_hidden_column,	
		'second_hidden_column' 	: second_hidden_column,
		}


		return HttpResponse(json.dumps(context))
	else:
		return HttpResponseRedirect('/it/user_login')