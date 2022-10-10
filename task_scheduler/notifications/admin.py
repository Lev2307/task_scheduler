from django.contrib import admin
from .models import Notification, UserNotificationCategories

# Register your models here.

@admin.register(Notification)
class AdminNotification(admin.ModelAdmin):
    list_display = ('user', 'text', 'notification_time', 'id')
    list_filter = ('user', 'created_time')

@admin.register(UserNotificationCategories)
class AdminNotification(admin.ModelAdmin):
    list_display = ('user', 'user_notification_category_name', 'user_notification_category_color')