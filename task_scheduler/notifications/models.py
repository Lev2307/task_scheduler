from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class NotificationType(models.Model):
    user = models.ForeignKey('authentication.MyUser', null=True, on_delete=models.SET_NULL)
    name_type = models.CharField(max_length=45)
    color = models.CharField(max_length=15)
    def __str__(self):
        return self.name_type


class NotificationStatus(models.Model):
    time_stamp = models.DateTimeField()
    status = models.BooleanField(default=False)

class NotificationPeriodicity(models.Model):
    HOURS_CHOICES = [
        (0, 0),
        (1, 1),
        (5, 5),
        (12, 12),
        (24, 24)
    ]
    DAYS_CHOICES = [
        (0, 0),
        (1, 1),
        (5, 5),
        (15, 15),
        (28, 28)
    ]
    MONTHS_CHOICES = [
        (0, 0),
        (1, 1),
        (3, 3),
        (6, 6),
        (12, 12)
    ]
    notification_periodicity_num = models.IntegerField(default=1)
    frequency_hours = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(24)], choices=HOURS_CHOICES)
    frequency_days = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(28)], choices=DAYS_CHOICES)
    frequency_months = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], choices=MONTHS_CHOICES)

class NotificationBase(models.Model):
    notification_task_type = models.ForeignKey(NotificationType, null=True, on_delete=models.SET_NULL, related_name='notification_task_type', default='study')
    text = models.TextField(max_length=350)
    created_time = models.DateTimeField(auto_now_add=True)
    notification_date = models.DateField(default=datetime.now)
    notification_time = models.TimeField(default=datetime.now)
    notification_status = models.ManyToManyField(NotificationStatus)
    notification_type_periodicity = models.ForeignKey(NotificationPeriodicity, null=True, blank=True, on_delete=models.SET_NULL)

    def check_if_date_is_earlier(created_time, notification_date):
        if created_time <=  notification_date:
            return True
        return False

    def __str__(self):
        return self.text.capitalize()


class Notification(models.Model):
    user = models.ForeignKey('authentication.MyUser', null=True, on_delete=models.SET_NULL)
    notifications = models.ForeignKey(NotificationBase, null=True, on_delete=models.SET_NULL)

