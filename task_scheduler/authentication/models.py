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
        study = NotificationType.objects.get(name_type='study')
        work = NotificationType.objects.get(name_type='work')
        general = NotificationType.objects.get(name_type='general')
        self.notification_type.add(study)
        self.notification_type.add(work)
        self.notification_type.add(general)




