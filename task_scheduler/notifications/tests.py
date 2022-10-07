from django.test import TestCase, Client
from .models import Notification
from authentication.models import MyUser
import datetime

# Create your tests here.
class NotificationTest(TestCase):
    def setUp(self):
        self.basic_user = MyUser(username='admin', email='a@a.com')
        self.basic_user.set_password('123')
        self.username = self.basic_user.username
        self.password = '123'
        self.c = Client()
        self.basic_user.save()
        Notification.objects.create(user=self.basic_user, notification_task_type='по работе', text='сделать отсчёт за месяц', notification_date='2022-10-17', notification_time='11:50:07', notification_periodicity=False, notification_periodicity_num=0)
    def test_created_notification(self):
        '''Проверка создания напоминалки'''
        notification_objects_old = Notification.objects.count()
        notification = Notification.objects.create(user=self.basic_user, notification_task_type='общее', text='сходить в магаз', notification_date='2022-09-28', notification_time='11:50:07', notification_periodicity=False, notification_periodicity_num=0)
        notification_objects_new = Notification.objects.count()
        self.assertTrue(notification_objects_old+1 == notification_objects_new)

    def test_get_notification_data(self):
        '''Проверка получения данных напоминалки'''
        notification = Notification.objects.get(id=1)
        date = datetime.datetime(2022, 10, 17)
        time = datetime.time(11, 50, 7)
        self.assertEqual(notification.notification_task_type, 'по работе')
        self.assertEqual(notification.text, 'сделать отсчёт за месяц')
        self.assertEqual(notification.notification_date, date.date())
        self.assertEqual(notification.notification_time, time)
        self.assertEqual(notification.created_time.date(), datetime.datetime.now().date())
        self.assertEqual(notification.notification_periodicity, False)
        self.assertEqual(notification.notification_periodicity_num, 0)          

    def test_notification_date_isnot_earlier_than_created(self):
        '''Проверка, если поставленная дата напоминалки не раньше её создания'''
        notification = Notification.objects.get(id=1)
        notification_date = datetime.datetime(2022, 12, 7).date()
        notification_date_equals = datetime.datetime(2022, 10, 7).date()
        notification_date_past = datetime.datetime(2018, 12, 7).date()
        notification_time_larger = datetime.time(17, 28, 11)
        notification_time_smaller = datetime.time(10, 28, 11)
        # если дата напоминания > чем дата создания
        self.assertEqual(Notification.check_if_date_is_earlier(notification.created_time, notification_date, notification_time_larger), True)

        # если дата напоминания равна дате создания и время напоминания в часах и минутах > чем время в часах и минутах в создании
        self.assertEqual(Notification.check_if_date_is_earlier(notification.created_time, notification_date_equals, notification_time_larger), True)

        # если дата напоминания равна дате создания и время напоминания в часах и минутах < чем время в часах и минутах в создании
        self.assertEqual(Notification.check_if_date_is_earlier(notification.created_time, notification_date_equals, notification_time_smaller), False)

        # если дата напоминания вообщем < дата создания
        self.assertEqual(Notification.check_if_date_is_earlier(notification.created_time, notification_date_past, notification_time_larger), False)
        self.assertEqual(Notification.check_if_date_is_earlier(notification.created_time, notification_date_past, notification_time_smaller), False)


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
    
    def test_homepage_getresponse(self):
        '''Проверка url у homepage'''
        self.c.login(username=self.username, password=self.password)

        response = self.c.get('')
        self.assertTrue(response.status_code == 200)

    def test_notificationslist_getresponse(self):
        '''Проверка url у notifications_list если он залогинен или незалогинен'''
        unlogged_response = self.c.get('/notifications/read/')
        self.assertTrue(unlogged_response.status_code == 302)
        #logged user
        self.c.login(username=self.username, password=self.password)

        logged_response = self.c.get('/notifications/read/')
        self.assertTrue(logged_response.status_code == 200)
    
    def test_notificationcreate_getresponse(self):
        '''Проверка url у notification_create если он залогинен или незалогинен'''
        unlogged_response = self.c.get('/notifications/create/')
        self.assertTrue(unlogged_response.status_code == 302)
        #logged user
        self.c.login(username=self.username, password=self.password)

        logged_response = self.c.get('/notifications/create/')
        self.assertTrue(logged_response.status_code == 200)

    def test_notificationcreate_postresponse(self):
        '''Проверка post запроса у notification_create'''
        self.c.login(username=self.username, password=self.password)

        data = {
            'user': self.username,
            'notification_task_type': 'по учёбе',
            'text': 'test note',
            'notification_date': '2022-10-10',
            'notification_time': '19:50:07',
            'notification_periodicity': False,
            'notification_periodicity_num': 0
        }

        notification_objects_old = Notification.objects.count()
        response = self.c.post('/notifications/create/', data, follow=True)
        notification_objects_new = Notification.objects.count()
        self.assertTrue(notification_objects_old+1 == notification_objects_new)
        self.assertTrue(response.status_code == 200)
    
    def test_notificationedit_getresponse(self):
        '''Проверка post запроса у notification_edit'''
        notification = Notification.objects.get(id=1)
        # unlogged user
        unlogged_response = self.c.get(f'/notifications/edit/{notification.id}/')
        self.assertTrue(unlogged_response.status_code == 302)
        #logged user
        self.c.login(username=self.username, password=self.password)

        logged_response = self.c.get(f'/notifications/edit/{notification.id}/')
        self.assertTrue(logged_response.status_code == 200)

    def test_notificationedit_postresponse(self):
        '''Проверка post запроса у notification_edit'''
        self.c.login(username=self.username, password=self.password)
        
        notification = Notification.objects.get(id=1)
        data = {
            'user': self.username,
            'notification_task_type': 'общее',
            'text': 'test edit note',
            'notification_date': '2022-10-15',
            'notification_time': '18:32:56',
            'notification_periodicity': True,
            'notification_periodicity_num': 2
        }
        notification_edited_date = datetime.datetime(2022, 10, 15).date()
        notification_edited_time = datetime.time(18, 32, 56)
        response = self.c.post(f'/notifications/edit/{notification.id}/', data)
        notification = Notification.objects.get(id=1)
        self.assertTrue(notification.notification_task_type, 'общее')
        self.assertTrue(notification.text, 'test edit note')
        self.assertTrue(notification.notification_time, notification_edited_date)
        self.assertTrue(notification.notification_periodicity, True)
        self.assertTrue(notification.notification_periodicity_num, 2)
        self.assertTrue(response.status_code == 302)

    def test_notificationdelete_getresponse(self):
        '''Проверка post запроса у notification_delete'''
        notification = Notification.objects.get(id=1)
        # unlogged user
        unlogged_response = self.c.get(f'/notifications/delete/{notification.id}/')
        self.assertTrue(unlogged_response.status_code == 302)
        #logged user
        self.c.login(username=self.username, password=self.password)

        logged_response = self.c.get(f'/notifications/delete/{notification.id}/')
        self.assertTrue(logged_response.status_code == 200)

    def test_notificationdelete_postresponse(self):
        '''Проверка post запроса у notification_delete'''
        self.c.login(username=self.username, password=self.password)

        old_notifications = Notification.objects.all().count()
        notification = Notification.objects.get(id=1)
        response = self.c.post(f'/notifications/delete/{notification.id}/', follow=True)
        new_notifications = Notification.objects.all().count()

        self.assertTrue(old_notifications-1 == new_notifications)
        self.assertTrue(response.status_code==200)