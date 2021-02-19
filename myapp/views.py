from django.shortcuts import render, redirect
from django.http import HttpResponse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

from . import models

from django.utils import timezone

import pytz
import json
import requests
import math

def LineRequestFunction(message,token):
	url = 'https://notify-api.line.me/api/notify'
	try:
		headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
		r = requests.post(url, headers=headers , data = {'message':message})
		# print('line request done : '+str(r.status_code))
	except Exception as e:
		print(str(e))

def home(request):
	return redirect(view, device_id=1)

def view(request,device_id):
	return render(request, 'view.html',{
		'device_id':device_id,
		'device_list':models.Device.objects.all()
	})

def api(request):
	device_id 	= request.GET.get('device')
	device_key 	= request.GET.get('key')
	device_obj  = models.Device.objects.getFromID(device_id)
	if device_obj is None: return HttpResponse('Device not found')
	if device_obj.key != device_key: return HttpResponse('Invalid key')
	timestamp		= timezone.now()
	salinity 		= float(request.GET.get('salinity','NaN'))
	ppm 				= float(request.GET.get('ppm','NaN'))
	ppt 				= float(request.GET.get('ppt','NaN'))
	if device_obj.LINE_enable:
		LineRequestFunction(
			'Result at'+
			'\n'+timestamp.astimezone(pytz.timezone('Asia/Bangkok')).strftime("%d/%m/%Y, %H:%M:%S")+
			'\nSalinity: '+str(salinity)+'mS/cm'+
			'\nppm: '+str(ppm)+
			'\nppt: '+str(ppt)
			,device_obj.LINE_token)
	async_to_sync(channel_layer.group_send)(device_id, {
		'type': 'data_message',
		'timestamp': timestamp.isoformat(),
		'salinity': salinity if not math.isnan(salinity) else None,
		'ppm': 			ppm if not math.isnan(ppm) else None,
		'ppt': 			ppt if not math.isnan(ppt) else None,
	})
	return HttpResponse('OK')