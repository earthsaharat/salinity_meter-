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

class Notification(models.Model):
	name 				= models.CharField(max_length=50)
	LINE_enable = models.BooleanField(default=False)
	LINE_token 	= models.CharField(max_length=50, null=True, blank=True)
	def __str__(self):
		output = self.name
		if self.LINE_enable:
			output += ' (LINE)'
		else:
			output += ' (Off)'
		return output

class Device_ModelManager(models.Manager):
	def getFromID(self,id):
		devices = super().get_queryset().filter(id=int(id))
		if len(devices) > 0: return devices[0]
		return None
	def getFromSiteID(self,site_id):
		devices = super().get_queryset().filter(site_id=site_id)
		if len(devices) > 0: return devices[0]
		return None

class Device(models.Model):
	objects 			= Device_ModelManager()
	name 					= models.CharField(max_length=50)
	key 					= models.CharField(max_length=50,default=Device_KeyGenerate,null=True,blank=True)
	notification	= models.ForeignKey(Notification,on_delete=models.SET_NULL,null=True,blank=True)
	is_station		= models.BooleanField(default=False)
	site_id				= models.CharField(max_length=50,unique=True,null=True,blank=True)
	location_lat	= models.FloatField(null=True,blank=True)
	location_lng	= models.FloatField(null=True,blank=True)


