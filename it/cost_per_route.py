import os
from django.http import HttpResponse
import json
from it import models
from django.shortcuts import render
from django.shortcuts import render,render_to_response


def cost_per_route(request):
	if request.user.is_authenticated():			
		cost_details = models.cost_per_route.objects.all()
		cost_array   = []
		client_array = []
		login_user = request.user	
		for x in cost_details:
			if x.client_id_id==113:
				clID = 15576
			else:
			 	clID = x.client_id_id
			client  = models.Client.objects.filter(status=1,proj_name='BOSS',id=clID).exclude(client_name='').exclude(client_name='Test').first()
			try:
				cl_name = client.client_name
				cl_id 	= x.id
			except:
				cl_name = ""
				cl_id 	= ""
			cost_array.append({
				'id'    	: cl_id,
				'cost'  	: x.cost,
				'route' 	: x.route,
				'client'    : cl_name,
				'client_id' : cl_id,
				})
		
		client_list  = models.Client.objects.filter(status=1,proj_name='BOSS').exclude(client_name='').exclude(client_name='Test')  
		for c in client_list:
			try:
				cl_name = c.client_name
			except:
				cl_name = ""
			client_array.append({
				'client_name' : c.client_name,
				'client_id'   : c.id,
				})
		context={
			'cost_array'   : cost_array,
			'client_array' : client_array,
			'login_user'   : login_user
		}

		return render_to_response("invoice_display/cost_per_route.html",context)
		if user.is_anonymous():
			return HttpResponseRedirect('/it/user_login')
	else:
		return HttpResponseRedirect('/it/user_login')

def update_cost_route(request):
	idx 				 = json.loads(request.GET['IDx'])
	cost 				 = json.loads(request.GET['cost'])
	route 				 = json.loads(request.GET['route'])
	client 				 = json.loads(request.GET['client'])
	
	updates 			 = models.cost_per_route.objects.filter(id=idx).first()
	updates.cost 		 = cost
	updates.route 		 = route
	updates.client_id_id = client
	updates.save()
	return HttpResponse(json.dumps('done'))

def submit_cost_route(request):
	cost   = json.loads(request.GET['cost'])
	route  = json.loads(request.GET['route'])
	client = json.loads(request.GET['client']) 
	clID   = models.Client.objects.filter(status=1,proj_name='BOSS',client_name=client).first() 
	check  = models.cost_per_route.objects.filter(cost=cost,route=route,client_id_id=clID.id).count()
	if check>0:
		route_db = models.cost_per_route.objects.filter(cost=cost,route=route,client_id_id=clID.id).first()
		msg = 'already'
	else:
		route_db = models.cost_per_route()
		msg = 'done'

	route_db.cost 			= cost
	route_db.route  		= route
	route_db.client_id_id 	= clID.id	
	route_db.save()	
	return HttpResponse(json.dumps(msg))

def delete_cost_route(request):
	deleteID  = json.loads(request.GET['delID'])
	models.cost_per_route.objects.filter(id=deleteID).delete()
	return HttpResponse(json.dumps('delx'))