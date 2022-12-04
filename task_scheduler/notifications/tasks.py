from celery import shared_task
import time
from celery.utils.log import get_task_logger
from .models import NotificationType
from authentication.models import MyUser
from django.contrib import messages

logger = get_task_logger(__name__)


@shared_task()
def test_task():
    """
        вызываем декоратор shared_task
        Ставим time.sleep на 10 секунд и создаём новую модель NotificationType
    """
    user = MyUser.objects.get(id=1)
    new_model = NotificationType.objects.create(user=user, name_type='celery_test_apply_async_delay', color='#d8d8d8')

@shared_task()
def create_notification_task():
    return 'created'