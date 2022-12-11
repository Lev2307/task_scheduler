from datetime import datetime
from django import forms
from .models import NotificationSingle, NotificationPeriodicity, NotificationType
from authentication.models import MyUser
from django.db.models import Q

HOURS_CHOICES = [
    (0, 0),
    (1, 1),
    (5, 5),
    (12, 12),
    (24, 24)
]
DAYS_CHOICES = [
    (0, 0),
    (1, 1),
    (5, 5),
    (15, 15),
    (28, 28)
]
MONTHS_CHOICES = [
    (0, 0),
    (1, 1),
    (3, 3),
    (6, 6),
    (12, 12)
]

class NotificationCreateForm(forms.ModelForm):
    notification_task_type = forms.ModelChoiceField(queryset=NotificationType.objects.all(), initial='study')
    text = forms.CharField(widget=forms.Textarea, max_length=350)
    notification_date = forms.DateField(widget=forms.SelectDateWidget(), initial=datetime.now().date())
    notification_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), initial=datetime.now().time())
    class Meta:
        model = NotificationSingle
        fields = ['notification_task_type', 'text', 'notification_date', 'notification_time']

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        notification_date = cleaned_data['notification_date']
        notification_time = cleaned_data['notification_time']
        two_times = str(notification_date) + ' ' + str(notification_time)
        notif_time = datetime.strptime(two_times, '%Y-%m-%d %H:%M:%S')
        created_time = datetime.now()
        if created_time >=  notif_time:
            raise forms.ValidationError('Дата оповещения не может быть в прошлом!!!')

class PeriodicalNotificationCreateForm(forms.ModelForm):
    notification_task_type = forms.ModelChoiceField(queryset=NotificationType.objects.all(), initial='study')
    text = forms.CharField(widget=forms.Textarea, max_length=350)
    notification_periodicity_num = forms.IntegerField(initial=1, min_value=1, max_value=15)
    frequency_hours = forms.ChoiceField(choices=HOURS_CHOICES, initial=0, widget=forms.RadioSelect)
    frequency_days = forms.ChoiceField(choices=DAYS_CHOICES, initial=0, widget=forms.RadioSelect)
    frequency_months = forms.ChoiceField(choices=MONTHS_CHOICES, initial=0, widget=forms.RadioSelect)

    class Meta:
        model = NotificationPeriodicity
        fields = ['notification_task_type', 'text', 'notification_periodicity_num', 'frequency_hours', 'frequency_days', 'frequency_months']

class NotificationEditForm(forms.ModelForm):
    pass

    # class Meta:
    #     model = Notification
    #     fields = ['notification_task_type', 'text', 'notification_date', 'notification_time', 'notification_periodicity', 'notification_periodicity_num']
    #     widgets = {
    #         'notification_date': forms.SelectDateWidget(),
    #         'notification_time': forms.TimeInput(attrs={'type': 'time'})
    #     }
    #     labels = {
    #         'text' : 'текст',
    #         'notification_date' : 'дата оповещения ( день, месяц, год )',
    #         'notification_time' : 'дата оповещения ( часы, минуты )',
    #         'notification_periodicity' : 'повторять ли оповещение',
    #         'notification_periodicity_num' : 'сколько раз напомнить',
    #     }

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request')
    #     super().__init__(*args, **kwargs)
    #     self.fields['notification_task_type'].queryset = NotificationType.objects.filter(Q(user=self.request.user) | Q(user=None))

    # def clean(self):
    #     cleaned_data = super().clean()
    #     notification_date = cleaned_data['notification_date']
    #     notification_time = cleaned_data['notification_time']
    #     two_times = str(notification_date) + ' ' + str(notification_time)
    #     notif_time = datetime.strptime(two_times, '%Y-%m-%d %H:%M:%S')
    #     created_time = datetime.now()
    #     if Notification.check_if_date_is_earlier(created_time, notif_time) != True:
    #         raise forms.ValidationError('Дата оповещения не может быть в прошлом!!!')

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
        color = self.cleaned_data['color']
        if MyUser.objects.get(id=self.request.user.pk).notification_type.filter(Q(name_type=name_type) | Q(color=color)).exists():
            raise forms.ValidationError('Выберите другой цвет или другое название для типа оповещения, так как такое уже существует ;>')
