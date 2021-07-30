from django.contrib import admin

from . import models

class DeviceAdmin(admin.ModelAdmin):
	def custom_id(obj):
		if obj.site_id is not None: return str(obj.site_id)
		return str(obj.id)
	custom_id.short_description = 'ID'
	list_display = (custom_id,'name', 'is_station', 'notification', 'key')
	list_display_links = (custom_id, 'name')
	list_filter = ('is_station',)
admin.site.register(models.Device, DeviceAdmin)

class NotificationAdmin(admin.ModelAdmin):
	list_display = ('id','name','LINE_enable','LINE_token')
	list_display_links = ('id', 'name')
	list_filter = ('LINE_enable',)
admin.site.register(models.Notification, NotificationAdmin)
