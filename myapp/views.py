from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

from . import models

from django.utils import timezone
from datetime import datetime
import pytz

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

def sendUpdate(device_obj,data_obj):
	if device_obj.notification is not None:
		if device_obj.notification.LINE_enable:
			LineRequestFunction(
				'Result at'+
				'\n'+data_obj['timestamp'].astimezone(pytz.timezone('Asia/Bangkok')).strftime("%d/%m/%Y, %H:%M:%S")+
				'\nSalinity: '+str(data_obj['salinity'])+'mS/cm'+
				'\nppm: '+str(data_obj['ppm'])+
				'\nppt: '+str(data_obj['ppt'])
				,device_obj.notification.LINE_token)
	ws_payload = {
		'type': 			'data_message',
		'device_id': 	device_obj.id,
		'timestamp': 	data_obj['timestamp'].isoformat(),
		'data':				{},
	}
	def ws_add_data(data_key):
		if data_key in data_obj:
			if data_obj[data_key] is not None:
				if not math.isnan(data_obj[data_key]): ws_payload['data'][data_key] = data_obj[data_key]
	ws_add_data('salinity')
	ws_add_data('ppm')
	ws_add_data('ppt')
	ws_add_data('lat')
	ws_add_data('lng')
	print(ws_payload)
	# async_to_sync(channel_layer.group_send)(str(device_obj.id), ws_payload)
	async_to_sync(channel_layer.group_send)('all', ws_payload)

def home(request):
	return redirect(view, device_id=1)

def view(request,device_id):
	return render(request, 'view.html',{
		'device_id':device_id,
		'device_list':models.Device.objects.all()
	})

def api(request):
	device_id 	= request.GET.get('device')
	if device_id is None: return HttpResponse('No device')
	device_key 	= request.GET.get('key')
	if device_key is None: return HttpResponse('No key')
	device_obj  = models.Device.objects.getFromID(device_id)
	if device_obj is None: return HttpResponse('Device not found')
	if device_obj.key != device_key: return HttpResponse('Invalid key')
	data_obj = {
		'timestamp'		: timezone.now(),
		'salinity' 		: float(request.GET.get('salinity','NaN')),
		'ppm' 				: float(request.GET.get('ppm','NaN')),
		'ppt' 				: float(request.GET.get('ppt','NaN')),
		'lat' 				: float(request.GET.get('lat','NaN')),
		'lng' 				: float(request.GET.get('lng','NaN')),
	}
	sendUpdate(device_obj,data_obj)
	return HttpResponse('OK')

@csrf_exempt
def api_station(request):
	if request.method == 'POST':
		request_body = json.loads(request.body)
		# print(request_body)
		device_obj = models.Device.objects.getFromSiteID(request_body['siteID'])
		if device_obj is None: return HttpResponse('Device not found')
		timestamp_BKK = datetime.fromtimestamp(request_body['timestamp'], tz=pytz.timezone('Asia/Bangkok'))
		timestamp_UTC = timestamp_BKK.astimezone(pytz.utc)
		data_obj = {
			'timestamp'		: timestamp_UTC,
			'salinity' 		: request_body['waterSensorData']['Salinity'],
		}
		sendUpdate(device_obj,data_obj)
	return HttpResponse('OK')


	