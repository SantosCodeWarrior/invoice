from django.shortcuts import render,render_to_response
from it import models
from django.http import HttpResponse
import json
from django.db.models import Count
from django.db import connection
from datetime import date,timedelta,datetime

import os
import time
from collections import Counter
import numpy as np
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
import math
import urllib2
import urlparse
from django.views.decorators.csrf import csrf_exempt
from decimal import *
from django.contrib.auth.models import User

import smtplib
import pprint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage

def update_password(request):
	if request.user.is_authenticated():	
		user 	  = models.Users.objects.filter(user=request.user)[0]		
		user_type = user.user_type
		user_ID   = user.user_id		
		#vm_id     = user.voyage_manager_id
		#shp_id    = user.ship_id
		#cl_id     = user.client_id
		# vm 		  = models.Voyage_Manager.objects.filter(id=vm_id)[0]
		# vm 		  = vm.vm_name
		login_user = request.user	

		context={
		'user_ID'    : user_ID,
		'login_user' : login_user		
		}	
		return render_to_response('invoice_display/security/edit_password.html',context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')

def change_update_details(request):
	if request.user.is_authenticated():		
		userID      = request.GET['userID']
		new_pwd     = request.GET['new_pwd']
		#old_pwd     = request.GET['old_pwd']
		conf_pwd    = request.GET['conf_pwd']
		user        = models.Users.objects.filter(user=userID)[0]	
		 
		
		if new_pwd==conf_pwd:
	 		u = User.objects.get(id=userID)
			u.set_password(conf_pwd)
			u.save()						
	 	else:
	 		return HttpResponse(json.dumps('not_match'))	
		

		chk     = models.new_users.objects.filter(user=userID).count()
		if chk>0:			
			new = models.new_users.objects.filter(user=userID).first()
		else:			
			new = models.new_users()		
		new.user_id				= userID
		new.change_password 	= new_pwd		
		new.save()	

	
		html_content   = "Good day <b><font color='orange'>Automated Invoice Module (AIM)</font></b>,<br><br>Updated Password: "+str(new_pwd)+"<br/><br/><br/><b>Thanks & Best Regards</b><br/>Invoice Team"
		mailto 		   = 'santosh@bwesglobal.com'
		cc_email 	   = 'santosh@bwesglobal.com'
		mailsubject    = 'Update Password Alert from Automated Invoice Module (AIM)'
		text_content   = 'This is an important message.'
		msg 		   = EmailMultiAlternatives(mailsubject,text_content,'santosh@bwesglobal.com',[mailto],bcc=[cc_email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		
		return HttpResponse(json.dumps('done'))
	else:
		return HttpResponseRedirect('/it/user_login')