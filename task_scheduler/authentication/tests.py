from django.test import TestCase, Client
from .models import MyUser

# Create your tests here.
class MyUserTests(TestCase):
    def setUp(self):
        self.myuser = MyUser.objects.create(username='admin', password='123', email='a@a.com', is_subscribed=False, is_staff=True, is_active=True, choose_sending='telegram')
        self.myuser.set_password('123')
        self.c = Client()
        self.myuser.save()
        self.username = self.myuser.username
        self.password = self.myuser.password
    def test_created_user(self):
        '''Проверка создания пользователя'''
        myusers_old = MyUser.objects.count()
        new_user = MyUser.objects.create(username='admin_fake', password='123fake', email='a_fake@a.com', is_subscribed=False, is_staff=False, is_active=True, choose_sending='email')
        myusers_new = MyUser.objects.count()
        self.assertTrue(myusers_old+1 == myusers_new)
    
    def test_user_choosesending_exists(self):
        myuser = MyUser.objects.get(id=1)
        choices = []
        for choice in MyUser.SendingChoices.choices:
            choices.append(choice[0])
        self.assertTrue(myuser.choose_sending in choices)

    def test_registration_url(self):
        ''' Проверка url регистрации '''
        response = self.c.get('/auth/registration/')
        self.assertEqual(response.status_code, 200)

    def test_registration_request(self):
        '''Проверка регистрации пользователя'''
        data = {
            'username': 'new_user',
            'email': 'new_user@gmail.com',
            'password1': 'new_userpassword',
            'password2': 'new_userpassword',
            'choose_sending': 'telegram'
        }
        response = self.c.post('/auth/registration/', data, follow=True)
        self.assertEqual(response.status_code, 200)
    

    def test_login_url(self):
        '''Проверка url логина'''
        response = self.c.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_request(self):
        '''Проверка входа пользователя в аккаунт'''
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.c.post('/auth/login/', data, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        '''Проверка выхода пользователя из аккаунта'''
        logout_url = '/auth/logout/'
        response = self.c.post(logout_url)
        self.assertTrue(response.status_code == 302)
        