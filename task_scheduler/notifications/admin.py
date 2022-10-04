from django.contrib import admin
from .models import Notification

# Register your models here.

@admin.register(Notification)
class AdminNotification(admin.ModelAdmin):
    list_display = ('user', 'text', 'notification_time', 'id')
    list_filter = ('user', 'created_time')