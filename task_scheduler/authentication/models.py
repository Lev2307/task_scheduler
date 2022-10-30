from django.db import models
from django.contrib.auth.models import AbstractUser
from notifications.models import NotificationType
from django.utils.translation import gettext_lazy as _

class MyUser(AbstractUser):
    class SendingChoices(models.Choices):
        EMAIL = _('email')
        TELEGRAM = _('telegram')

    notification_type = models.ManyToManyField(NotificationType)
    is_subscribed = models.BooleanField(default=False)
    choose_sending = models.CharField(max_length=35, choices=SendingChoices.choices, default='email')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        study = NotificationType.objects.get_or_create(name_type='study', color='#107a8b')
        work = NotificationType.objects.get_or_create(name_type='work', color='#ba2121')
        general = NotificationType.objects.get_or_create(name_type='general', color='#e0c45c')
        self.notification_type.add(study[0])
        self.notification_type.add(work[0])
        self.notification_type.add(general[0])




