from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.core import serializers


logger = get_task_logger(__name__)


# @shared_task()
# def test_task():
#     """
#         вызываем декоратор shared_task
#         Ставим time.sleep на 10 секунд и создаём новую модель NotificationType
#     """
#     user = MyUser.objects.get(id=1)
#     new_model = NotificationType.objects.create(user=user, name_type='celery_test_apply_async_delay', color='#d8d8d8')

@shared_task()
def create_notification_task(instance_id):  
   from .models import NotificationSingle
   print('created')
   notif_single = NotificationSingle.objects.filter(id=instance_id)
   print(notif_single.model)
   print(dir(notif_single))
   # notif_single.update(notification_status__done=True, notification_status__time_stamp=timezone.now())



