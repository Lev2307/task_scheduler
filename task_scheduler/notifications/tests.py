from django.test import TestCase
from .models import Notification
from authentication.models import MyUser
import datetime

# Create your tests here.
class NotificationTest(TestCase):
    def setUp(self):
        self.basic_user = MyUser(username='admin', email='a@a.com')
        self.basic_user.save()
        Notification.objects.create(user=self.basic_user, notification_task_type='по работе', text='сделать отсчёт за месяц', notification_time='2022-10-17', notification_periodicity=False, notification_periodicity_num=0)
    def test_created_notification(self):
        '''Проверка создания напоминалки'''
        notification_objects_old = Notification.objects.count()
        notification = Notification.objects.create(user=self.basic_user, notification_task_type='общее', text='сходить в магаз', notification_time='2022-09-28', notification_periodicity=False, notification_periodicity_num=0)
        notification_objects_new = Notification.objects.count()
        self.assertTrue(notification_objects_old+1 == notification_objects_new)

    def test_get_notification_data(self):
        '''Проверка получения данных напоминалки'''
        notification = Notification.objects.get(id=1)
        date = datetime.datetime(2022, 10, 17)
        self.assertEqual(notification.notification_task_type, 'по работе')
        self.assertEqual(notification.text, 'сделать отсчёт за месяц')
        self.assertEqual(notification.notification_time, date.date())
        self.assertEqual(notification.created_time.date(), datetime.datetime.now().date())
        self.assertEqual(notification.notification_periodicity, False)
        self.assertEqual(notification.notification_periodicity_num, 0)          

    def test_notification_date_isnot_earlier_than_created(self):
        '''Проверка, если поставленная дата напоминалки не раньше её создания'''
        notification = Notification.objects.get(id=1)
        notification_prev_date = notification.notification_time
        notification.notification_time = datetime.datetime(2018, 5, 7).date()
        self.assertEqual(Notification.check_if_date_is_earlier(notification.created_time.date(), notification_prev_date), True)
        self.assertEqual(Notification.check_if_date_is_earlier(notification.created_time.date(), notification.notification_time), False)

    def test_notification_textlength(self):
        '''Проверка макс. кол-ва символов в тексте напоминалки'''
        notification = Notification.objects.get(id=1)
        notification_text = notification.text
        self.assertTrue(len(notification_text) <= 350)
        notification_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed egestas egestas fringilla phasellus faucibus scelerisque eleifend donec pretium. Ut enim blandit volutpat maecenas volutpat blandit aliquam. Nec sagittis aliquam malesuada bibendum arcu. Diam quam nulla porttitor massa. Nunc non blandit massa enim nec dui. Et odio pellentesque diam volutpat commodo sed egestas egestas fringilla. Pretium viverra suspendisse potenti nullam. Et netus et malesuada fames ac. Tincidunt tortor aliquam nulla facilisi cras fermentum odio. Quisque egestas diam in arcu cursus euismod. Fermentum iaculis eu non diam phasellus vestibulum lorem sed. Arcu dui vivamus arcu felis bibendum ut. Tincidunt arcu non sodales neque sodales ut etiam sit amet. Urna porttitor rhoncus dolor purus non enim praesent elementum. Volutpat odio facilisis mauris sit amet massa vitae. Lacinia at quis risus sed vulputate. Fusce ut placerat orci nulla. Metus dictum at tempor commodo ullamcorper a lacus vestibulum sed. Non pulvinar neque laoreet suspendisse interdum consectetur libero. Eget nulla facilisi etiam dignissim diam quis enim lobortis. Ornare arcu odio ut sem. Gravida dictum fusce ut placerat orci nulla pellentesque. Nunc eget lorem dolor sed viverra ipsum nunc. Aliquam ultrices sagittis orci a scelerisque purus semper. At imperdiet dui accumsan sit amet nulla facilisi morbi. Amet nulla facilisi morbi tempus iaculis. Velit dignissim sodales ut eu sem. Malesuada pellentesque elit eget gravida cum sociis. Vitae et leo duis ut diam quam nulla. Diam volutpat commodo sed egestas egestas. Scelerisque eu ultrices vitae auctor eu augue ut lectus arcu. Sem nulla pharetra diam sit amet nisl suscipit. Sed id semper risus in hendrerit gravida rutrum. Enim praesent elementum facilisis leo vel fringilla est ullamcorper eget.'
        self.assertFalse(len(notification_text) <= 350)
    
    def test_notification_type_exists(self):
        '''Проверка существует ли тип напоминалки'''
        notification = Notification.objects.get(id=1)
        choices = []
        for choice in Notification.TaskTypeChoices.choices:
            choices.append(choice[0])
        self.assertTrue(notification.notification_task_type in choices)