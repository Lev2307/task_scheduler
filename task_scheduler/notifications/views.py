from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Notification, NotificationType
from .forms import NotificationCreateForm, NotificationEditForm, AddNotificationTypeForm
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from authentication.models import MyUser

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

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['notifications_types'] = MyUser.objects.get(id=self.request.user.pk).notification_type.all()
        return c

    def form_valid(self, form):
        response = self.request.POST.get('select_type')
        notification_form = form.save(commit=True)
        notification_form.user = self.request.user   
        notification_form.notification_task_type = response   
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

class AddNotificationTypeView(LoginRequiredMixin, CreateView):
    model = NotificationType
    form_class = AddNotificationTypeForm
    success_url = reverse_lazy('profile')
    login_url = reverse_lazy('login')
    template_name = 'notifications/add_new_notification_type.html'

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request # the trick!
        return kw

    def form_valid(self, form):
        new_type = MyUser.objects.get(id=self.request.user.pk).notification_type.create(name_type=form.cleaned_data['name_type'])
        new_type.save()
        form.save(commit=False)
        return HttpResponseRedirect(self.success_url)