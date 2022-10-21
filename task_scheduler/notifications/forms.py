from datetime import datetime
from django import forms
from .models import Notification, NotificationType

class NotificationCreateForm(forms.ModelForm):
    def clean(self):
        notification_date = self.cleaned_data['notification_date']
        notification_time = self.cleaned_data['notification_time']
        created_time = datetime.now()
        print(notification_date, notification_time)
        if Notification.check_if_date_is_earlier(created_time, notification_date, notification_time) != True:
            raise forms.ValidationError('You`ve entered wrong notification date. Please try again!!!')

    class Meta:
        model = Notification
        fields = ['text', 'notification_date', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']
        widgets = {
            'notification_date': forms.SelectDateWidget(),
            'notification_time': forms.TimeInput(attrs={'type': 'time'})
        }
        labels = {
            'notification_task_type' : 'тип оповещения',
            'text' : 'текст',
            'notification_date' : 'дата оповещения ( день, месяц, год )',
            'notification_time' : 'дата оповещения ( часы, минуты )',
            'notification_periodicity' : 'повторять ли оповещение',
            'notification_periodicity_num' : 'сколько раз напомнить',
        }
    
    
class NotificationEditForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['text', 'notification_date', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']
        widgets = {
            'notification_date': forms.SelectDateWidget(),
            'notification_time': forms.TimeInput(attrs={'type': 'time'})
        }
        labels = {
            'notification_task_type' : 'тип оповещения',
            'text' : 'текст',
            'notification_date' : 'дата оповещения ( день, месяц, год )',
            'notification_time' : 'дата оповещения ( часы, минуты )',
            'notification_periodicity' : 'повторять ли оповещение',
            'notification_periodicity_num' : 'сколько раз напомнить',
        }

class AddNotificationTypeForm(forms.ModelForm):
    class Meta:
        model = NotificationType
        fields = ['name_type']        
        labels = {
            'name_type' : 'имя новой категории',
        }