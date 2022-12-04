from django.contrib import admin
from .models import NotificationBase, NotificationType

# Register your models here.

@admin.register(NotificationBase)
class AdminNotification(admin.ModelAdmin):
    list_display = ('user', 'text', 'notification_time', 'id')
    list_filter = ('user', 'created_time')


@admin.register(NotificationType)
class AdminNotificationTypeName(admin.ModelAdmin):
    list_display = ('name_type', )