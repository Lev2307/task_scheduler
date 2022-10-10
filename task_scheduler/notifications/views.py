from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Notification, UserNotificationCategories
from .forms import NotificationCreateForm, NotificationEditForm, UserNotificationCategoriesForm
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView

# Create your views here.
class HomeView(View):
    template_name = 'mainpage.html'
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

class NotificationEditView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Notification
    form_class = NotificationEditForm
    template_name = 'notifications/edit_notification.html'
    success_url = reverse_lazy('notification_list')

class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Notification
    success_url = reverse_lazy('notification_list')
    login_url = reverse_lazy('login')
    template_name = 'notifications/delete_notification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = get_object_or_404(Notification, pk=self.kwargs['pk'])
        return context

class UserNotificationCategoriesView(LoginRequiredMixin, CreateView):
    model = UserNotificationCategories
    form_class = UserNotificationCategoriesForm
    template_name = 'notifications/create_user_notification_category.html'
    success_url = reverse_lazy('notification_list')

    def form_valid(self, form):
        new_form = form.save(commit=True)
        new_form.user = self.request.user
        new_form.save()
        return HttpResponseRedirect(self.success_url)