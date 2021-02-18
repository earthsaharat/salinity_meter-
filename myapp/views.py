from django.shortcuts import render, redirect
from django.http import HttpResponse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

def home(request):
	return redirect(view)

def view(request):
	return render(request, 'view.html')

def api(request):
	async_to_sync(channel_layer.group_send)(request.GET.get('device','1'), {
		'type': 'data_message',
		'salinity': int(request.GET.get('salinity','-1')),
	})
	return HttpResponse('OK')