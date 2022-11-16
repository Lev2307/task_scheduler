from datetime import datetime
from django.db import models

class NotificationType(models.Model):
    user = models.ForeignKey('authentication.MyUser', null=True, on_delete=models.SET_NULL)
    name_type = models.CharField(max_length=45)
    color = models.CharField(max_length=15)
    def __str__(self):
        return self.name_type

class Notification(models.Model):
    class Meta:
        ordering = ['user', '-created_time']

    user = models.ForeignKey('authentication.MyUser', null=True, on_delete=models.SET_NULL)
    notification_task_type = models.ForeignKey(NotificationType, null=True, on_delete=models.SET_NULL, related_name='notification_task_type', default='study')
    text = models.TextField(max_length=350)
    created_time = models.DateTimeField(auto_now_add=True)
    notification_date = models.DateField(default=datetime.now)
    notification_time = models.TimeField(default=datetime.now)
    notification_periodicity = models.BooleanField(default=False)
    notification_periodicity_num = models.IntegerField(default=1)

    def check_if_date_is_earlier(created_time, notification_date):
        if created_time <=  notification_date:
            return True
        return False

    def __str__(self):
        return self.text.capitalize()