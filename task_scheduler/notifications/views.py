from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Notification, NotificationType
from .forms import NotificationCreateForm, NotificationEditForm, AddNotificationTypeForm
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from authentication.models import MyUser
from .tasks import test_task, create_notification_task

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
        context['notifications_types'] = MyUser.objects.get(id=self.request.user.pk).notification_type.all()
        return context

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Notification
    form_class = NotificationCreateForm
    template_name = 'notifications/create_notification.html'
    success_url = reverse_lazy('notification_list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw

    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.user = self.request.user
        new_form.save()
        return HttpResponseRedirect(self.success_url)

class NotificationEditView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Notification
    form_class = NotificationEditForm
    template_name = 'notifications/edit_notification.html'
    success_url = reverse_lazy('notification_list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw

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
    success_url = reverse_lazy('notification_list')
    login_url = reverse_lazy('login')
    template_name = 'notifications/add_new_notification_type.html'

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw

    def form_valid(self, form):
        notif_type = self.model.objects.create(user=self.request.user, name_type=form.cleaned_data['name_type'], color=form.cleaned_data['color'])
        notif_type.save()
        MyUser.objects.get(id=self.request.user.pk).notification_type.add(notif_type)
        form.save(commit=False)
        return HttpResponseRedirect(self.success_url)

def test_view(request):
    test_task.apply_async(countdown=15)
    return HttpResponse('hi!')