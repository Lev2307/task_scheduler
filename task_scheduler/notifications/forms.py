from datetime import datetime
from django import forms
from .models import Notification, NotificationType
from authentication.views import MyUser

class NotificationCreateForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['text', 'notification_date', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']
        widgets = {
            'notification_date': forms.SelectDateWidget(),
            'notification_time': forms.TimeInput(attrs={'type': 'time'})
        }
        labels = {
            'text' : 'текст',
            'notification_date' : 'дата оповещения ( день, месяц, год )',
            'notification_time' : 'дата оповещения ( часы, минуты )',
            'notification_periodicity' : 'повторять ли оповещение',
            'notification_periodicity_num' : 'сколько раз напомнить',
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        notification_date = cleaned_data['notification_date']
        notification_time = cleaned_data['notification_time']
        two_times = str(notification_date) + ' ' + str(notification_time)
        notif_time = datetime.strptime(two_times, '%Y-%m-%d %H:%M:%S')
        created_time = datetime.now()
        if Notification.check_if_date_is_earlier(created_time, notif_time) != True:
            raise forms.ValidationError('Дата оповещения не может быть в прошлом!!!')

    def save(self, commit=True):
        res = super().save(commit)
        response = self.request.POST.get('select_type')
        notif_type = NotificationType.objects.get(name_type=response)
        res.user = self.request.user   
        res.notification_task_type = response 
        res.notification_color = notif_type.color
        res.save()
        return res
        
class NotificationEditForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['text', 'notification_date', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']
        widgets = {
            'notification_date': forms.SelectDateWidget(),
            'notification_time': forms.TimeInput(attrs={'type': 'time'})
        }
        labels = {
            'text' : 'текст',
            'notification_date' : 'дата оповещения ( день, месяц, год )',
            'notification_time' : 'дата оповещения ( часы, минуты )',
            'notification_periodicity' : 'повторять ли оповещение',
            'notification_periodicity_num' : 'сколько раз напомнить',
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        notification_date = cleaned_data['notification_date']
        notification_time = cleaned_data['notification_time']
        two_times = str(notification_date) + ' ' + str(notification_time)
        notif_time = datetime.strptime(two_times, '%Y-%m-%d %H:%M:%S')
        created_time = datetime.now()
        if Notification.check_if_date_is_earlier(created_time, notif_time) != True:
            raise forms.ValidationError('Дата оповещения не может быть в прошлом!!!')

    def save(self, commit=True):
        res = super().save(commit)
        response = self.request.POST.get('select_type')
        notif_type = NotificationType.objects.get(name_type=response)
        res.user = self.request.user   
        res.notification_task_type = response
        res.notification_color = notif_type.color
        res.save()
        return res
        

class AddNotificationTypeForm(forms.ModelForm):
    class Meta:
        model = NotificationType
        fields = ['name_type', 'color']        
        labels = {
            'name_type' : 'имя новой категории',
        }
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'})
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        name_type = self.cleaned_data['name_type']
        if MyUser.objects.get(id=self.request.user.pk).notification_type.filter(name_type=name_type).exists():
            raise forms.ValidationError('Данный тип оповещения УЖЕ существует. Попробуйте ввести другое ;>')
