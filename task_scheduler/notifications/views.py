from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Notification
from .forms import NotificationCreateForm
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

# Create your views here.
class HomeView(View):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {'user': user})
        
class NotificationListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Notification
    context_object_name = 'notifications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Notification
    form_class = NotificationCreateForm
    template_name = 'notifications/create_notification.html'
    success_url = reverse_lazy('notification_list')

    def form_valid(self, form):
        notification_form = form.save(commit=True)
        notification_form.user = self.request.user
        notification_form.save()
        return HttpResponseRedirect(self.success_url)