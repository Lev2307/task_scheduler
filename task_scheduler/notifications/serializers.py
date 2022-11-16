from .models import Notification, NotificationType
from rest_framework import serializers
from datetime import datetime
from authentication.models import MyUser
from django.db.models import Q


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_task_type', 'text', 'notification_date', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']

    def validate(self, attrs):
        notification_date = attrs['notification_date']
        notification_time = attrs['notification_time']
        two_times = str(notification_date) + ' ' + str(notification_time)
        notif_time = datetime.strptime(two_times, '%Y-%m-%d %H:%M:%S')
        created_time = datetime.now()
        if Notification.check_if_date_is_earlier(created_time, notif_time) != True:
            raise serializers.ValidationError('Дата оповещения не может быть в прошлом!!!')
        return attrs

class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ['name_type', 'color']
    
    def validate(self, attrs):
        name_type = attrs['name_type']
        color = attrs['color']
        if MyUser.objects.get(id=self.context['request'].user.id).notification_type.filter(Q(name_type=name_type) | Q(color=color)).exists():
            raise serializers.ValidationError('Выберите другой цвет или другое название для типа оповещения, так как такое уже существует ;>')
        return attrs