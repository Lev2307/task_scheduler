from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MyUser
from notifications.models import NotificationType
from .forms import RegisterForm
from django.db.models import Q

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

class UserProfileView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = MyUser
    template_name = 'auth/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.model.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_notification_types'] = NotificationType.objects.filter(Q(user=self.request.user) | Q(user=None))
        return context

