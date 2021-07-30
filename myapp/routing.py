from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('ws/device/all', consumers.ChatConsumer.as_asgi()),
	# path('ws/device/<device_id>', consumers.ChatConsumer.as_asgi()),
]