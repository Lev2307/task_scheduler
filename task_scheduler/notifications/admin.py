from django.contrib import admin
from .models import NotificationType, NotificationSingle, NotificationPeriodicity, NotificationStatus, NotificationBase

# Register your models here.
admin.site.register(NotificationStatus)
admin.site.register(NotificationBase)
admin.site.register(NotificationPeriodicity)

@admin.register(NotificationSingle)
class AdminNotificationSingle(admin.ModelAdmin):
    readonly_fields = ('notification_status', )

@admin.register(NotificationType)
class AdminNotificationTypeName(admin.ModelAdmin):
    list_display = ('name_type', )