from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

# Create your views here.
class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'auth/registration.html'

class LoginView(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    template_name = 'auth/login.html'

class LogoutView(LogoutView):
    redirect_field_name = reverse_lazy("login")