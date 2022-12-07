from django.contrib import admin
from .models import Notification, NotificationType, NotificationBase, NotificationPeriodicity, NotificationStatus

# Register your models here.
admin.site.register(NotificationStatus)
admin.site.register(NotificationPeriodicity)
admin.site.register(NotificationBase)
admin.site.register(Notification)

@admin.register(NotificationType)
class AdminNotificationTypeName(admin.ModelAdmin):
    list_display = ('name_type', )