from datetime import datetime
from django.db import models

class NotificationType(models.Model):
    name_type = models.CharField(max_length=45)
    color = models.CharField(max_length=15)
    def __str__(self):
        return self.name_type

class Notification(models.Model):
    class Meta:
        ordering = ['-created_time']
    user = models.ForeignKey('authentication.MyUser', null=True, on_delete=models.SET_NULL)
    notification_task_type = models.CharField(max_length=45)
    notification_color = models.CharField(max_length=15)
    text = models.TextField(max_length=350)
    created_time = models.DateTimeField(auto_now_add=True)
    notification_date = models.DateField(default=datetime.now)
    notification_time = models.TimeField(default=datetime.now)
    notification_periodicity = models.BooleanField(default=False)
    notification_periodicity_num = models.IntegerField(default=1)

    def check_if_date_is_earlier(created_time, notification_date, notification_time):
        print(created_time.date(), notification_date)
        print(created_time.time(), notification_time)
        if created_time.date() < notification_date:
            return True
        elif created_time.date() == notification_date:
            if created_time.time() < notification_time:
                return True
            else:
                return False
        return False

    def __str__(self):
        return self.text.capitalize()