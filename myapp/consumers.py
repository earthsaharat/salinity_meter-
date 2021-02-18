import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = self.scope['url_route']['kwargs']['device_id']
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)
		self.accept()

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)

	def receive(self, text_data):
		pass
		# text_data_json = json.loads(text_data)
		# message = text_data_json['message']
		# async_to_sync(self.channel_layer.group_send)(
		# 	self.room_group_name,
		# 	{
		# 		'type': 'general_message',
		# 		'message': message
		# 	}
		# )

	def general_message(self, event):
		self.send(text_data=json.dumps({
			'message': event['message']
		}))

	def data_message(self, event):
		self.send(text_data=json.dumps({
			'timestamp': timezone.now().isoformat(),
			'salinity': event['salinity'],
		}))