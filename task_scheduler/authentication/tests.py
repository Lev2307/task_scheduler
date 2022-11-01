from django.test import TestCase, Client
from .models import MyUser

# Create your tests here.
class MyUserTests(TestCase):
    def setUp(self):
        self.username = 'admin_name'
        self.password = 'admin'
        self.email = 'admin_email@gmail.com'
        self.choose_sending = 'telegram'
        self.myuser = MyUser.objects.create(username=self.username, password=self.password, email=self.email, is_subscribed=False, is_staff=True, is_active=True, choose_sending=self.choose_sending)
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
        response = self.c.get('/auth/registration/')
        self.assertEqual(response.status_code, 200)

    def test_registration_request(self):
        '''Проверка регистрации пользователя'''
        myusers_old = MyUser.objects.all().count()
        data = {
            'username': 'new_user',
            'email': 'new_user@gmail.com',
            'password1': 'new_userpassword',
            'password2': 'new_userpassword',
            'choose_sending': 'telegram'
        }
        response = self.c.post('/auth/registration/', data, follow=True)
        myusers_new = MyUser.objects.all().count()
        self.assertEqual(myusers_old+1, myusers_new)
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
        self.assertTrue(response.context['user'].is_active, True)
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        '''Проверка выхода пользователя из аккаунта'''
        logout_url = '/auth/logout/'
        response = self.c.post(logout_url)
        self.assertTrue(response.status_code == 302)
        