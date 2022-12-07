from django.contrib import admin
from .models import Notification, NotificationType, NotificationBase

# Register your models here.
admin.site.register(NotificationBase)
admin.site.register(Notification)

@admin.register(NotificationType)
class AdminNotificationTypeName(admin.ModelAdmin):
    list_display = ('name_type', )