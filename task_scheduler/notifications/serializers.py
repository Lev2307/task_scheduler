from .models import Notification, NotificationType
from rest_framework import serializers

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ['text', 'notification_date', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']

