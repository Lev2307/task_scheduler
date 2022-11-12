from django.test import TestCase, Client
from .models import MyUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
# Create your tests here.
class MyUserTests(TestCase):
    def setUp(self):
        self.username = 'admin_name'
        self.password = 'admin'
        self.email = 'admin_email@gmail.com'
        self.choose_sending = 'telegram'
        self.myuser = MyUser.objects.create(username=self.username, email=self.email, is_subscribed=False, is_staff=True, is_active=True, choose_sending=self.choose_sending)
        self.myuser.set_password(self.password)
        self.myuser.save()
        self.c = Client()
    def test_created_user(self):
        '''Проверка создания пользователя'''
        myusers = MyUser.objects.all().count()
        self.assertEqual(myusers, 1)
    
    def test_user_choosesending_exists(self):
        myuser = MyUser.objects.get(id=1)
        choices = []
        for choice in MyUser.SendingChoices.choices:
            choices.append(choice[0])
        self.assertTrue(myuser.choose_sending in choices)

    def test_registration_url(self):
        ''' Проверка url регистрации '''
        url = reverse('registration')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_registration_request(self):
        '''Проверка регистрации пользователя'''
        url = reverse('registration')
        myusers_old = MyUser.objects.all().count()
        data = {
            'username': 'new_user',
            'email': 'new_user@gmail.com',
            'password1': 'new_userpassword',
            'password2': 'new_userpassword',
            'choose_sending': 'telegram'
        }
        response = self.c.post(url, data)
        myusers_new = MyUser.objects.all().count()
        self.assertEqual(myusers_old+1, myusers_new)
        self.assertEqual(response.status_code, 302)
    
    def test_login_url(self):
        '''Проверка url логина'''
        url = reverse('login')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_login_request(self):
        '''Проверка входа пользователя в аккаунт'''
        url = reverse('login')
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.c.post(url, data)
        self.assertEqual(response.status_code, 302)
    
    def test_logout(self):
        '''Проверка выхода пользователя из аккаунта'''
        url = reverse('logout')
        response = self.c.post(url)
        self.assertTrue(response.status_code == 302)

class AccountTests(APITestCase):
    def setUp(self):
        self.api_username = 'testcase_api'
        self.api_password = 'testcase_api_password'
        self.api_email = 'testcase_api@gmail.com'
        self.api_choose_sending = 'telegram'

        self.registration_api_url = reverse('user_registration_api')
        self.login_api_url = reverse('user_login_api')

        self.myuser = MyUser.objects.create(username=self.api_username, email=self.api_email, is_subscribed=False, is_staff=True, is_active=True, choose_sending=self.api_choose_sending)
        self.myuser.set_password(self.api_password)
        self.myuser.save()
        return super().setUp()

    def test_registration_url(self):
        '''Проверка url api регистрации'''
        response = self.client.get(self.registration_api_url)
        self.assertEqual(response.status_code, 200)

    def test_registration_request(self):
        '''Проверка api регистрации пользователя'''
        old_users = MyUser.objects.all().count()
        data = {
            "username": 'new_' + self.api_username,
            "email": 'new_' + self.api_email,
            "password": 'new_' + self.api_password,
            "password2": 'new_' + self.api_password,
            "choose_sending": self.api_choose_sending,
        }
        response = self.client.post(self.registration_api_url, data, format='json')
        new_users = MyUser.objects.all().count()
        self.assertEqual(old_users+1, new_users)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_url(self):
        '''Проверка url api login'''
        response = self.client.get(self.login_api_url)
        self.assertEqual(response.status_code, 200)

    def test_login_request(self):
        '''Проверка api входа пользователя в аккаунт'''
        res = self.client.post(self.login_api_url, {"username": self.api_username, "password": self.api_password})
        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)