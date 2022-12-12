from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class NotificationType(models.Model):
    user = models.ForeignKey('authentication.MyUser', null=True, on_delete=models.SET_NULL)
    name_type = models.CharField(max_length=45)
    color = models.CharField(max_length=15)
    def __str__(self):
        return self.name_type


class NotificationStatus(models.Model):
    time_stamp = models.DateTimeField(blank=True, null=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        if self.done == False:
            return 'Not complited'
        return 'Complited'
    
    def save(self, *args, **kwargs):
        if self.done == True:
            self.time_stamp = timezone.now()
        else:
            self.time_stamp = None
        super().save(*args, **kwargs)
    

class NotificationBase(models.Model):
    user = models.ForeignKey('authentication.MyUser', null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        created_date = self.created_time.date()
        created_time = self.created_time.time().replace(microsecond=0)
        return f'создал {self.user}, создано в {created_date} {created_time}'

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
    notification_task_type = models.OneToOneField(NotificationType, null=True, on_delete=models.SET_NULL, related_name='notification_task_type_periodic', default='study', verbose_name='тип оповещения')
    text = models.TextField(max_length=350, verbose_name='текст оповещения')
    notification_status = models.ManyToManyField(NotificationStatus, verbose_name='Выполнено')
    notification_periodicity_num = models.IntegerField(default=1, verbose_name='количество повторений оповещения')
    frequency_hours = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(24)], choices=HOURS_CHOICES, verbose_name='часы')
    frequency_days = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(28)], choices=DAYS_CHOICES, verbose_name='дни')
    frequency_months = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], choices=MONTHS_CHOICES, verbose_name='месяцы')
    notification_type_periodicity = models.OneToOneField(NotificationBase, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'periodic: {self.text.capitalize()}'

class NotificationSingle(models.Model):
    notification_task_type = models.OneToOneField(NotificationType, null=True, on_delete=models.SET_NULL, related_name='notification_task_type_single', default='study', verbose_name='тип оповещения')
    text = models.TextField(max_length=350, verbose_name='текст оповещения')
    notification_date = models.DateField(default=timezone.now(), verbose_name='Дата исполнения')
    notification_time = models.TimeField(default=timezone.now(), verbose_name='Время исполнения')
    notification_status = models.OneToOneField(NotificationStatus, null=True, on_delete=models.SET_NULL, verbose_name='Выполнено')
    notification_type_single = models.OneToOneField(NotificationBase, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'single: {self.text.capitalize()}'
