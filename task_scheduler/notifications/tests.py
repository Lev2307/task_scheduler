from django.test import TestCase, Client
from django.utils import timezone
from .models import Notification, NotificationType
from authentication.models import MyUser
from datetime import datetime, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

# Create your tests here.

class NotificationTests(TestCase):
    def setUp(self):
        self.datetime_now = datetime.now()
        self.datetime_past_date = self.datetime_now - timedelta(days=5)
        self.username = 'admin_name'
        self.email = 'admin_email@gmail.com'
        self.password = 'admin'
        self.second_user_username = 'second_user'
        self.second_user_email = 'second_user@gmail.com'
        self.second_user_password = 'second_user123'
        self.notification_test_type = 'test type'
        self.test_color = '#000'    
        self.test_text = 'test text'
        self.notification_edit_type = 'edit type'
        self.edit_color = '#bababa'
        self.basic_user = MyUser(username=self.username, email=self.email)
        self.basic_user.set_password(self.password)
        self.basic_user.save()
        self.second_user = MyUser(username=self.second_user_username, email=self.second_user_email)
        self.second_user.set_password(self.second_user_password)
        self.second_user.save()
        self.test_type = NotificationType.objects.create(name_type=self.notification_test_type, color=self.test_color)
        self.basic_user.notification_type.add(self.test_type)
        self.edit_type = NotificationType.objects.create(name_type=self.notification_edit_type, color=self.edit_color)
        self.basic_user.notification_type.add(self.edit_type)
        self.c = Client()
        Notification.objects.create(
            user=self.basic_user,
            notification_task_type=self.test_type, 
            text=self.test_text, 
            notification_date=self.datetime_now.date(), 
            notification_time=self.datetime_now.time(), 
            notification_periodicity=False, 
            notification_periodicity_num=0
        )
        
    def test_created_and_added_notificationtype(self):
        '''Проверка создания и добавление типа напоминалки к пользовательским'''
        notification_type_objects = NotificationType.objects.all().count()
        user_notification_type_objects = MyUser.objects.get(username=self.username).notification_type.all().count()
        self.assertEqual(notification_type_objects, 5)
        self.assertEqual(user_notification_type_objects, 5)

    def test_create_notificationtype_to_differentusers(self):
        first_user = MyUser.objects.get(id=1)
        second_user = MyUser.objects.get(id=2)
        second_user.notification_type.add(self.test_type)
        self.assertEqual(first_user.notification_type.get(name_type=str(self.test_type)), second_user.notification_type.get(name_type=str(self.test_type)))

    def test_created_notification(self):
        '''Проверка создания напоминалки'''
        notification_objects = Notification.objects.all().count()
        self.assertEqual(notification_objects, 1)

    # def test_get_notification_data(self):
    #     '''Проверка получения данных напоминалки'''
    #     notification = Notification.objects.get(id=1)
    #     self.assertEqual(notification.notification_task_type.name_type, self.notification_test_type)
    #     self.assertEqual(notification.text, self.test_text)
    #     self.assertEqual(notification.notification_task_type.color, self.test_color)
    #     self.assertEqual(notification.notification_date, self.datetime_now.date())
    #     self.assertEqual(notification.notification_time, self.datetime_now.time())
    #     self.assertEqual(notification.created_time.date(), self.datetime_now.date())
    #     self.assertEqual(notification.notification_periodicity, False)
    #     self.assertEqual(notification.notification_periodicity_num, 0)          

    def test_notification_date_isnot_earlier_than_created(self):
        '''Проверка, если поставленная дата напоминалки не раньше её создания'''
        notification = Notification.objects.get(id=1)
        notification_date = timezone.make_aware(self.datetime_now) 
        notification_date_past = timezone.make_aware(self.datetime_past_date) 
        # если дата напоминания > чем дата создания
        self.assertEqual(Notification.check_if_date_is_earlier(notification.created_time, notification_date), True)

        # если дата напоминания < дата создания
        self.assertEqual(Notification.check_if_date_is_earlier(notification.created_time, notification_date_past), False)
        
    def test_notification_textlength(self):
        '''Проверка макс. кол-ва символов в тексте напоминалки'''
        notification = Notification.objects.get(id=1)
        notification_text = notification.text
        self.assertTrue(len(notification_text) <= 350)
        notification_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed egestas egestas fringilla phasellus faucibus scelerisque eleifend donec pretium. Ut enim blandit volutpat maecenas volutpat blandit aliquam. Nec sagittis aliquam malesuada bibendum arcu. Diam quam nulla porttitor massa. Nunc non blandit massa enim nec dui. Et odio pellentesque diam volutpat commodo sed egestas egestas fringilla. Pretium viverra suspendisse potenti nullam. Et netus et malesuada fames ac. Tincidunt tortor aliquam nulla facilisi cras fermentum odio. Quisque egestas diam in arcu cursus euismod. Fermentum iaculis eu non diam phasellus vestibulum lorem sed. Arcu dui vivamus arcu felis bibendum ut. Tincidunt arcu non sodales neque sodales ut etiam sit amet. Urna porttitor rhoncus dolor purus non enim praesent elementum. Volutpat odio facilisis mauris sit amet massa vitae. Lacinia at quis risus sed vulputate. Fusce ut placerat orci nulla. Metus dictum at tempor commodo ullamcorper a lacus vestibulum sed. Non pulvinar neque laoreet suspendisse interdum consectetur libero. Eget nulla facilisi etiam dignissim diam quis enim lobortis. Ornare arcu odio ut sem. Gravida dictum fusce ut placerat orci nulla pellentesque. Nunc eget lorem dolor sed viverra ipsum nunc. Aliquam ultrices sagittis orci a scelerisque purus semper. At imperdiet dui accumsan sit amet nulla facilisi morbi. Amet nulla facilisi morbi tempus iaculis. Velit dignissim sodales ut eu sem. Malesuada pellentesque elit eget gravida cum sociis. Vitae et leo duis ut diam quam nulla. Diam volutpat commodo sed egestas egestas. Scelerisque eu ultrices vitae auctor eu augue ut lectus arcu. Sem nulla pharetra diam sit amet nisl suscipit. Sed id semper risus in hendrerit gravida rutrum. Enim praesent elementum facilisis leo vel fringilla est ullamcorper eget.'
        self.assertFalse(len(notification_text) <= 350)
    
    def test_notification_type_exists(self):
        '''Проверка существует ли тип напоминалки у определённого пользователя'''
        notification = Notification.objects.get(id=1)
        exists = False
        for notif_type in MyUser.objects.get(username=self.username).notification_type.all():
            if notification.notification_task_type == notif_type:
                exists = True
        self.assertEqual(exists, True)
    
    def test_homepage_get_response(self):
        '''Проверка url у homepage'''
        self.c.login(username=self.username, password=self.password)

        response = self.c.get('')
        self.assertEqual(response.status_code, 200)

    def test_notifications_list_get_response(self):
        '''Проверка url у notifications_list если он залогинен или незалогинен'''
        unlogged_response = self.c.get('/notifications/read/')
        self.assertEqual(unlogged_response.status_code, 302)
        #logged user
        self.c.login(username=self.username, password=self.password)

        logged_response = self.c.get('/notifications/read/')

        self.assertEqual(logged_response.status_code, 200)
    
    def test_create_notification_get_response(self):
        '''Проверка url у notification_create если он залогинен или незалогинен'''
        unlogged_response = self.c.get('/notifications/create/')
        self.assertEqual(unlogged_response.status_code, 302)
        #logged user
        self.c.login(username=self.username, password=self.password)

        logged_response = self.c.get('/notifications/create/')

        self.assertEqual(logged_response.status_code, 200)

    def test_create_notification_post_response(self):
        '''Проверка post запроса у notification_create'''
        self.c.login(username=self.username, password=self.password)
        notif_time = self.datetime_now.strftime("%H:%M:%S")
        old_notif = Notification.objects.all().count()
        data = {
            'user': self.username,
            'notification_task_type': str(self.test_type),
            'text': 'new test text',
            'notification_date': self.datetime_now.date(),
            'notification_time': self.datetime_now.strptime(notif_time, "%H:%M:%S").time(),
            'notification_periodicity': False,
            'notification_periodicity_num': 0
        }
        response = self.c.post('/notifications/create/', data)
        new_notif = Notification.objects.all().count()

        self.assertEqual(response.status_code, 200)

    def test_edit_notification_get_response(self):
        '''Проверка url у notification_create если он залогинен или незалогинен'''
        notification = Notification.objects.get(id=1)
        unlogged_response = self.c.get(f'/notifications/edit/{notification.id}/')
        self.assertEqual(unlogged_response.status_code, 302)
        #logged user
        self.c.login(username=self.username, password=self.password)
        logged_response = self.c.get(f'/notifications/edit/{notification.id}/')

        self.assertEqual(logged_response.status_code, 200)
        
    def test_edit_notification_post_response(self):
        '''Проверка post запроса у notification_create'''
        self.c.login(username=self.username, password=self.password)
        notif_time = self.datetime_now.strftime("%H:%M:%S")
        notification = Notification.objects.get(id=1)
        data = {
            'user': self.username,
            'notification_task_type': str(self.edit_type),
            'text': 'edit test text',
            'notification_date': self.datetime_now.date(),
            'notification_time': self.datetime_now.strptime(notif_time, "%H:%M:%S").time(),
            'notification_periodicity': True,
            'notification_periodicity_num': 4
        }
        response = self.c.post(f'/notifications/edit/{notification.id}/', data)

        self.assertEqual(response.status_code, 200)

    def test_notification_delete_get_response(self):
        '''Проверка post запроса у notification_delete'''
        notification = Notification.objects.get(id=1)
        # unlogged user
        unlogged_response = self.c.get(f'/notifications/delete/{notification.id}/')
        self.assertEqual(unlogged_response.status_code, 302)

        #logged user
        self.c.login(username=self.username, password=self.password)
        logged_response = self.c.get(f'/notifications/delete/{notification.id}/')

        self.assertEqual(logged_response.status_code, 200)

    def test_notification_delete_post_response(self):
        '''Проверка post запроса у notification_delete'''
        self.c.login(username=self.username, password=self.password)

        old_notifications = Notification.objects.all().count()
        notification = Notification.objects.get(id=1)
        response = self.c.post(f'/notifications/delete/{notification.id}/', follow=True)
        new_notifications = Notification.objects.all().count()

        self.assertEqual(old_notifications-1, new_notifications)
        self.assertEqual(response.status_code, 200)

class NotificationTypeTests(TestCase):
    def setUp(self):
        self.username = 'admin_name'
        self.email = 'admin_email@gmail.com'
        self.password = 'admin'
        self.notification_test_type = 'test type'
        self.test_color = '#000'    
        self.c = Client()
        self.basic_user = MyUser(username=self.username, email=self.email)
        self.basic_user.set_password(self.password)
        self.basic_user.save()
        self.test_type = NotificationType.objects.create(name_type=self.notification_test_type, color=self.test_color)
        self.test_type.save()
        self.basic_user.notification_type.add(self.test_type)

    def test_notificationtype_create_get_response(self):        
        '''Проверка url у notificationtype_create если он залогинен или незалогинен'''
        unlogged_response = self.c.get('/notifications/add_notification_type/')
        self.assertEqual(unlogged_response.status_code, 302)
        #logged user
        self.c.login(username=self.username, password=self.password)
        logged_response = self.c.get('/notifications/add_notification_type/')

        self.assertEqual(logged_response.status_code, 200)

    def test_notificationtype_create_post_response(self):        
        '''Проверка post запроса у add_notification_type'''
        self.c.login(username=self.username, password=self.password)
        old_notification_types = NotificationType.objects.all().count()
        # если есть такой тип напоминалки
        exists_data = {
            'name_type': self.notification_test_type,
            'color': self.test_color,
        }
        response = self.c.post('/notifications/add_notification_type/', exists_data, follow=True)
        new_notification_types = NotificationType.objects.all().count()
        self.assertEqual(old_notification_types, new_notification_types)
        self.assertEqual(response.status_code, 200)

        # если нет такого типа напоминалки
        data = {
            'name_type': 'new_one',
            'color': '#8e8e8e',
        }
        response = self.c.post('/notifications/add_notification_type/', data, follow=True)
        new_notification_types = NotificationType.objects.all().count()

        self.assertEqual(old_notification_types+1, new_notification_types)
        self.assertEqual(response.status_code, 200)


class NotificationsApiTests(APITestCase):
    def setUp(self):
        self.notifications_list_api_url = reverse('notification_list_api_view')
        self.create_notification_url_api = reverse('create_notification_api_view')
        self.datetime_now = datetime.now()
        self.datetime_past_date = self.datetime_now - timedelta(days=5)
        self.username_api = 'testcase_api_name'
        self.email_api = 'testcase_api_email@gmail.com'
        self.password_api = 'testcase_api'
        self.notification_test_type_api = 'test type'
        self.test_color_api = '#bababa'    
        self.test_text_api = 'api test text'
        self.basic_user = MyUser(username=self.username_api, email=self.email_api)
        self.basic_user.set_password(self.password_api)
        self.basic_user.save()
        self.test_type = NotificationType.objects.create(name_type=self.notification_test_type_api, color=self.test_color_api)
        self.basic_user.notification_type.add(self.test_type)

        Notification.objects.create(
            user=self.basic_user,
            notification_task_type=self.test_type, 
            text=self.test_text_api, 
            notification_date=self.datetime_now.date(), 
            notification_time=self.datetime_now.time(), 
            notification_periodicity=True, 
            notification_periodicity_num=2
        )
    
    def test_notifications_list_url(self):
        '''Проверка url notifications_list api'''

        #unlogged user
        unlogged_response = self.client.get(self.notifications_list_api_url)
        self.assertEqual(unlogged_response.status_code, status.HTTP_403_FORBIDDEN)

        #logged in user
        self.client.login(username=self.username_api, password=self.password_api)

        logged_response = self.client.get(self.notifications_list_api_url)
        self.assertEqual(logged_response.status_code, status.HTTP_200_OK)

    def test_create_notification_url(self):
        '''Проверка url notification_create api'''

        #unlogged user
        unlogged_response = self.client.get(self.create_notification_url_api)
        self.assertEqual(unlogged_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username=self.username_api, password=self.password_api)
        logged_response = self.client.get(self.create_notification_url_api)
        self.assertEqual(logged_response.status_code, status.HTTP_200_OK)
    
    def test_create_notification_request(self):
        '''Проверка post запроса у notification_create api'''

        self.client.login(username=self.username_api, password=self.password_api)
        notif_time = self.datetime_now.strftime("%H:%M:%S")
        data = {
            'user': self.username_api,
            "notification_task_type": MyUser.objects.get(id=1).notification_type.get(name_type=self.test_type).id,
            "text": 'new test text',
            "notification_date": (self.datetime_now + timedelta(days=5)).date(),
            "notification_time": self.datetime_now.strptime(notif_time, "%H:%M:%S").time(),
            "notification_periodicity": False,
            "notification_periodicity_num": 0
        }
        old_notifications = Notification.objects.all().count()

        response = self.client.post(self.create_notification_url_api, data, format='json')
        new_notifications = Notification.objects.all().count()

        self.assertEqual(old_notifications+1, new_notifications)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_notification_url(self):
        '''Проверка url notification_edit api'''
    
        #unlogged user
        notification = Notification.objects.get(id=1)
        unlogged_response = self.client.get(f'/api/notifications/detail/{notification.id}/')
        self.assertEqual(unlogged_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username=self.username_api, password=self.password_api)
        logged_response = self.client.get(f'/api/notifications/detail/{notification.id}/')
        self.assertEqual(logged_response.status_code, status.HTTP_200_OK)

    def test_detail_edit_notification_request(self):
        self.client.login(username=self.username_api, password=self.password_api)
        notification = Notification.objects.get(id=1)
        notif_time = self.datetime_now.strftime("%H:%M:%S")
        data = {
            'user': self.username_api,
            "notification_task_type": MyUser.objects.get(id=1).notification_type.get(name_type=self.test_type).id,
            "text": 'edited test text',
            "notification_date": (self.datetime_now + timedelta(days=10)).date(),
            "notification_time": self.datetime_now.strptime(notif_time, "%H:%M:%S").time(),
            "notification_periodicity": True,
            "notification_periodicity_num": 4
        }
        response = self.client.put(f'/api/notifications/detail/{notification.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_delete_notification_request(self):
        self.client.login(username=self.username_api, password=self.password_api)
        notification = Notification.objects.get(id=1)

        old_notifications = Notification.objects.all().count()
        response = self.client.delete(f'/api/notifications/detail/{notification.id}/')
        new_notifications = Notification.objects.all().count()
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(old_notifications-1, new_notifications)

class NotificationTypesApiTests(APITestCase):
    def setUp(self):
        self.create_notification_type_url = reverse('create_notificationtype_api_view')
        self.username_api = 'admin_api_name'
        self.email_api = 'admin_api_email@gmail.com'
        self.password_api = 'admin_api'
        self.notification_test_type = 'api test type'
        self.test_color = '#581b98'    
        self.c = Client()
        self.basic_user = MyUser(username=self.username_api, email=self.email_api)
        self.basic_user.set_password(self.password_api)
        self.basic_user.save()

    def test_create_notification_type_url(self):
        '''Проверка url notification_edit api'''
        #unlogged user
        unlogged_response = self.client.get(self.create_notification_type_url)
        self.assertEqual(unlogged_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username=self.username_api, password=self.password_api)
        logged_response = self.client.get(self.create_notification_type_url)
        self.assertEqual(logged_response.status_code, status.HTTP_200_OK)

    def test_create_notification_type_request(self):
        self.client.login(username=self.username_api, password=self.password_api)
        old_notification_types = NotificationType.objects.all().count()
        data = {
            'user': self.username_api,
            'name_type': self.notification_test_type,
            'color': self.test_color
        }
        response = self.client.post(self.create_notification_type_url, data)
        new_notification_types = NotificationType.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(old_notification_types+1, new_notification_types)