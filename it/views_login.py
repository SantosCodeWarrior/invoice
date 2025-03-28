import django.middleware.csrf
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from it import models
import json

from datetime import datetime
from django.contrib import messages
from django.template import RequestContext
from django.core import serializers
from django.contrib.auth.models import User
from ipware.ip import get_ip
# import grequests

import grequests
import requests

import smtplib
import pprint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage


def user_login(request):
	if request.method == 'POST':
		username = json.loads(request.POST['username'])
		password = json.loads(request.POST['password'])
		user 	 = authenticate(username = username, password = password)




		if user:
			if user.is_active:
				login(request,user)
				ip_detail=get_user_ip(request)
				save_ip_det(ip_detail,user.id,username)
				#print '_____',user
				return HttpResponse(json.dumps('loggedin'))
			else:
				return HttpResponse(json.dumps("account disabled"))
		else:
			return HttpResponse(json.dumps("invalid"))
	else:
		if request.user.is_authenticated():
			return HttpResponseRedirect('/it/index')
		elif request.user.is_authenticated() and models.Users.objects.filter(user = request.user)[0].user_type == 'admin':
			return HttpResponseRedirect('/it/dashboard')
		return render_to_response('login/login.html',  RequestContext(request, {}))

def user_entry(request):
	#if request.user.is_authenticated():
	if request.method == 'POST':
		user_data = (request.POST)
		if True:
			un 		= user_data['username']
			ps 		= user_data['password']
			email 	= user_data['email']
			user 	= User.objects.create_user(username=un,email=email,password=ps)
			#print '_______',user
			user_model = models.Users()
			user_model.user = user
			user_model.user_type = user_data['user_type']
			if user_data['user_type'] == 'client':
				client = models.Client.objects.filter(id = user_data['obj_id'])[0]
				user_model.client = client
			else:
				voyage_manager = models.Voyage_Manager.objects.filter(id = user_data['obj_id'])[0]
				user_model.voyage_manager = voyage_manager
			user_model.save()
			return HttpResponse(json.dumps('done'))
		else:
			return HttpResponse(errors)
	else:
		return render(request,'login/data_entry_users.html', {})
	# else:
	# 	#return render(request,'login/data_entry_users.html', {})
	# 	return HttpResponseRedirect('/hb/user_login')

def user_logout(request):	
	logout(request)
	return HttpResponseRedirect('/it/user_login')

def log_sessions(request):
	userx 			= request.GET['userx']
	date_timem 		= request.GET['date_timem']
	InID 			= models.log_sessions()
	InID.date  		= date_timem
	InID.user_name  = userx
	InID.save()
		
	return HttpResponse(json.dumps('done'))


def get_user_ip(request):
	try:
		ip = get_ip(request)
		#print "------------"
		hosts=[]
		if ip is not None:
			#print "we have an IP address for user",ip
			hosts.append('http://api.db-ip.com/addrinfo?addr='+str(ip)+'&api_key=fa871e8abacd62600db9f57aa5746f2e15cd0d40')
			#print "---------------------",hosts
			rs=(grequests.get(u) for u in hosts)
			response=grequests.map(rs)
			for r in response:
				# try:
				ip_detail=json.loads(r.text)
			return ip_detail
		else:
			return 0
	except:
		pass


def save_ip_det(ip_detail,user_id,username):
	if ip_detail!=0:
		log 			=	 	models.login_log()
		log.user_id_id	=	 	user_id
		#print ip_detail['address']
		log.ip_adress	=	 	ip_detail['address']
		log.country 	= 	 	ip_detail['country']
		log.state 		= 		ip_detail['stateprov']
		log.city 		= 		ip_detail['city']
		log.save()
		try:
			send_simple_message(ip_detail['address'],username,ip_detail['city'],ip_detail['country'],ip_detail['stateprov'],str(datetime.now())[0:16])
		except:
			pass
	else:
		log 			= 		models.login_log()
		log.user_id_id	=		user_id
		log.ip_adress	=		0
		log.country		=		"-"
		log.state 		= 		"-"
		log.city 		= 		"-"
		log.save()

def send_simple_message(ip_address,username,city,country,state,e_date):
	#print '==========',	username
	import smtplib
	import pprint
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from django.core.mail import EmailMultiAlternatives
	from email.MIMEImage import MIMEImage
	
	html_content = "Good day <b><font color='orange'><b>"+str(username).capitalize()+",</b></font><br><br>logged in to <b><font color='#007bff'>Automated Invoice Module (AIM)</font></b> from <b>"+str(country)+"</b> , <b>"+str(state)+"</b>, <b>"+str(city)+"</b> using IP Address <b>"+str(ip_address)+"</b> on <b>"+str(e_date)+" GMT</b><br/><br/> <b>Thanks & Best Regards</b><br/>Invoice Team"
	if username=='arti':
		m_body = 'arti.rawat@bwesglobal.com'
	
	if username=='vasudha':
		m_body = 'vasudha.pant@bwesglobal.com'

	if username=='admin':
		m_body = "santosh@bwesglobal.com"

	if username=='sandeepm':
		m_body = "sandeep@bwesglobal.com"

	if username=='anuragt':
		m_body = "anurag.tiwari@bwesglobal.com"

	if username=='santosht':
		m_body = "santosh@bwesglobal.com"

	if username=='abhishek':
		m_body = "abhishek.topal@bwesglobal.com"

	if username=='gmadam':
		m_body = "sandeep@bwesglobal.com"

	mailto 		   = 'santosh@bwesglobal.com'
	cc_email 	   =  m_body
	mailsubject    = 'Login Alert from Invoice'
	text_content   = 'This is an important message.'
	msg 		   = EmailMultiAlternatives(mailsubject,text_content,'santosh@bwesglobal.com',[mailto],bcc=[cc_email])
	msg.attach_alternative(html_content, "text/html")
	#msg.send()
	
import random
def get_otp_plan(request):
	userID  		= json.loads(request.GET['userID'])	
	get_user_name 	= models.Users.objects.filter(email = userID).first()
	CHK 			= models.otp_verification.objects.filter(user_name=get_user_name.user_type).count()
	
	if CHK!=0:
		db = models.otp_verification.objects.filter(user_name=get_user_name.user_type).first()	
	else:
		db 			= models.otp_verification()

	otp 			= generate_otp()
	db.otps 		= otp
	db.user_name    = get_user_name.user_type
	db.current_date = datetime.now().date()
	db.save()	
	print '-----------',CHK

	html_content   	= "Good day <font color='orange'><b>"+str(userID)+",</b></font><font color='#007bff'></font><br><br><br>Secure One-Time Password (OTP): <b> "+str(otp)+"</b>.<br><br><i style='font-size:12px;'>For your security, do not share it with anyone.</i><br/><br/> <b>Thanks & Best Regards</b><br/>Invoice Team"
	m_body 			= "santosh@bwesglobal.com"
	mailto 		   	=  userID
	cc_email 	   	=  m_body
	mailsubject    	= '**** OTP Alert ****'
	text_content   	= 'This is an important message.'
	msg 		   	= EmailMultiAlternatives(mailsubject,text_content,'santosh@bwesglobal.com',[mailto],bcc=[cc_email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
	return HttpResponse(json.dumps('done'))
	

def generate_otp():
	otp = random.randint(1000, 9999)
	return otp



def otp_verification(request):	
	#if request.user.is_authenticated():
	ty_input_otp = json.loads(request.GET['type_input_otp'])	
	user_nmae 	 = json.loads(request.GET['user_nmae'])
	chk_user 	 = models.Users.objects.filter(email = user_nmae).first()
	user_request = chk_user.user_type
	otpx  		 = models.otp_verification.objects.filter(otps=ty_input_otp,user_name=user_request).count()	
	msgs         = ''
	username 	 = ''
	password     = ''
	if otpx==1:
		valid_otp       = ''
		dvv 			= models.Users.objects.filter(email = user_nmae).first()
		user_request 	= dvv.user_type
		userID 			= dvv.user_id
		gPassword		= models.new_users.objects.filter(user_id = userID).first()
		print '------',user_request
		
		if user_request=='santosht':	
			username 		= user_request
			password 		= gPassword.change_password
			
		elif user_request=='sandeepm':
			username 		= user_request
			password 		= gPassword.change_password
			
			
		elif user_request=='abhishek':
			username 		= user_request
			password 		= gPassword.change_password
			

		elif user_request=='arti':
			username 		= user_request
			password 		= gPassword.change_password
			

		elif user_request=='vasudha':
			username 		= user_request
			password 		= gPassword.change_password
			

		elif user_request=='anuragt':
			username 		= user_request
			password 		= gPassword.change_password

		elif user_request=='admin':
			username 		= user_request
			password 		= gPassword.change_password

		else:
			return HttpResponse(json.dumps("account disabled"))

		user = authenticate(username = username, password = password)			
		if user:
			if user.is_active:
				login(request,user)
				ip_detail=get_user_ip(request)
				save_ip_det(ip_detail,user.id,username)
				msgs = 'loggedin'
		
	else:
		valid_otp = 'Invalid'

	context={
	'msgs'		: msgs,
	'username' 	: username,
	'otp_msg'   : valid_otp, 
	}

	return HttpResponse(json.dumps(context))