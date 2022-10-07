from datetime import datetime
from django import forms
from .models import Notification 

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
        fields = ['notification_task_type', 'text', 'notification_date', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']
        widgets = {
            'notification_date': forms.SelectDateWidget(),
            'notification_time': forms.TimeInput(attrs={'type': 'time'})
        }
    
    
class NotificationEditForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['notification_task_type', 'text', 'notification_date', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']
        widgets = {
            'notification_date': forms.SelectDateWidget(),
            'notification_time': forms.TimeInput(attrs={'type': 'time'})
        }