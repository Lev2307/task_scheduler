from django import forms
from .models import Notification

class NotificationCreateForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['notification_task_type', 'text', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']