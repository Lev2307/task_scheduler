from django import forms
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Эта почта уже существует')
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2', 'choose_sending']
        labels = {
            'choose_sending': 'Choose where you`d like to get your notifications'
        }