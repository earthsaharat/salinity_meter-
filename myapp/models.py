from django.db import models

import string
import random

def Device_KeyGenerate():
  return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(20)])

class Device_ModelManager(models.Manager):
	def getFromID(self,id):
		devices = super().get_queryset().filter(id=int(id))
		if len(devices) > 0: return devices[0]
		return None

class Device(models.Model):
	name 				= models.CharField(max_length=50)
	key 				= models.CharField(max_length=50,default=Device_KeyGenerate)
	LINE_enable = models.BooleanField(default=False)
	LINE_token 	= models.CharField(max_length=50, blank=True)

	objects = Device_ModelManager()