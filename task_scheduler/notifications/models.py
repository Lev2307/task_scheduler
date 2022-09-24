import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    class TaskTypeChoices(models.Choices):
        WORK = 'по работе'
        STUDY = 'по учёбе'
        GENERAL = 'общее'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_task_type = models.CharField(max_length=30, choices=TaskTypeChoices.choices, default='по работе')
    text = models.TextField(max_length=350)
    created_time = models.DateTimeField(auto_now_add=True)
    notification_time = models.DateField()
    notification_periodicity = models.BooleanField(default=False)
    notification_periodicity_num = models.IntegerField(default=0)

    def check_if_date_is_earlier(created_time, notification_time):
        if notification_time < created_time:
            return False
        else:
            return True