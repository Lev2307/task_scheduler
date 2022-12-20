from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import NotificationType, NotificationBase, NotificationPeriodicity, NotificationSingle, NotificationStatus
from .forms import NotificationCreateForm, NotificationEditForm, AddNotificationTypeForm, PeriodicalNotificationCreateForm
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from authentication.models import MyUser

# Create your views here.
class HomeView(View):
    template_name = 'mainpage.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {'user': user})
        
class NotificationListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = NotificationBase
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['notifications_types'] = NotificationType.objects.filter(user=self.request.user)
        return context

    def get_queryset(self):
        return NotificationBase.objects.filter(user=self.request.user)

class NotificationSingleDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = NotificationSingle
    template_name = 'notifications/notification_single_detail.html'
    context_object_name = 'notification_single'

class NotificationSingleCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = NotificationSingle
    form_class = NotificationCreateForm
    template_name = 'notifications/create_notification.html'
    success_url = reverse_lazy('notification_list')

    def form_valid(self, form):
        notif_status = NotificationStatus.objects.create()
        notif_base = NotificationBase.objects.create(
            user=self.request.user
        )
        notification_single = NotificationSingle.objects.create(
            notification_task_type=form.cleaned_data['notification_task_type'],
            text=form.cleaned_data['text'],
            notification_date=form.cleaned_data['notification_date'],
            notification_time=form.cleaned_data['notification_time'],
            notification_status=notif_status,
            notification_type_single=notif_base
        )
        notification_single.save()
        return HttpResponseRedirect(self.success_url)
        
class NotificationSingleEditView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = NotificationSingle
    form_class = NotificationEditForm
    template_name = 'notifications/edit_notification.html'
    success_url = reverse_lazy('notification_list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw


class NotificationSingleDeleteView(LoginRequiredMixin, DeleteView):
    model = NotificationSingle
    success_url = reverse_lazy('notification_list')
    login_url = reverse_lazy('login')
    template_name = 'notifications/delete_notification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = get_object_or_404(NotificationSingle, pk=self.kwargs['pk'])
        return context

class PeriodicalNotificationCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = NotificationPeriodicity
    form_class = PeriodicalNotificationCreateForm
    template_name = 'notifications/create_periodical_notification.html'
    success_url = reverse_lazy('notification_list')

    def form_valid(self, form):
        notif_status = NotificationStatus.objects.create()
        notif_base = NotificationBase.objects.create(
            user=self.request.user
        )
        periodicity_model = NotificationPeriodicity.objects.create(
            notification_task_type=form.cleaned_data['notification_task_type'],
            text=form.cleaned_data['text'],
            notification_periodicity_num=form.cleaned_data['notification_periodicity_num'],
            frequency_hours=form.cleaned_data['frequency_hours'],
            frequency_days=form.cleaned_data['frequency_days'],
            frequency_months=form.cleaned_data['frequency_months'],
            notification_type_periodicity=notif_base
        )
        periodicity_model.notification_status.add(notif_status)
        periodicity_model.save()
        return HttpResponseRedirect(self.success_url)

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

# def test_view(request):
#     test_task.apply_async(countdown=15)
#     return HttpResponse('hi!')