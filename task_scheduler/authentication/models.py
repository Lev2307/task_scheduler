from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    class SendingChoices(models.Choices):
        EMAIL = 'email'
        TELEGRAM = 'telegram'

    is_subscribed = models.BooleanField(default=False)
    choose_sending = models.CharField(max_length=35, choices=SendingChoices.choices, default='email')