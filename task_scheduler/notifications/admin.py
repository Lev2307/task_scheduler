from django.contrib import admin
from .models import NotificationType, NotificationSingle, NotificationPeriodicity, NotificationStatus, NotificationBase

# # Register your models here.
# admin.site.register(NotificationStatus)
# admin.site.register(NotificationBase)
# admin.site.register(NotificationPeriodicity)
@admin.register(NotificationType)
class AdminNotificationTaskTypeName(admin.ModelAdmin):
    list_display = ('name_type', )


@admin.register(NotificationBase)
class AdminNotificationType(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
    