from django.test import TestCase
from .models import MyUser

# Create your tests here.
class MyUserTests(TestCase):
    def setUp(self):
        self.myuser = MyUser.objects.create(username='admin', password='123', email='a@a.com', is_subscribed=False, is_staff=True, is_active=True, choose_sending='telegram')
        self.myuser.save()
    def test_created_user(self):
        '''Проверка создания пользователя'''
        myusers_old = MyUser.objects.count()
        myuser = MyUser.objects.create(username='admin_fake', password='123fake', email='a_fake@a.com', is_subscribed=False, is_staff=False, is_active=True, choose_sending='email')
        myusers_new = MyUser.objects.count()
        self.assertTrue(myusers_old+1 == myusers_new)
    
    def test_user_choosesending_exists(self):
        myuser = MyUser.objects.get(id=1)
        choices = []
        for choice in MyUser.SendingChoices.choices:
            choices.append(choice[0])
        self.assertTrue(myuser.choose_sending in choices)
