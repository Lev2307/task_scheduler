from datetime import datetime
from django.db import models
from authentication.models import MyUser

# Create your models here.
class UserNotificationCategories(models.Model):
    user = models.ForeignKey(MyUser, null=True, on_delete=models.SET_NULL)
    user_notification_category_name = models.CharField(max_length=15)
    user_notification_category_color = models.CharField(max_length=10)

class Notification(models.Model):
    class TaskTypeChoices(models.Choices):
        WORK = 'по работе'
        STUDY = 'по учёбе'
        GENERAL = 'общее'

    user = models.ForeignKey(MyUser, null=True, on_delete=models.SET_NULL)
    notification_task_type = models.CharField(max_length=30, choices=TaskTypeChoices.choices, default='по работе')
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