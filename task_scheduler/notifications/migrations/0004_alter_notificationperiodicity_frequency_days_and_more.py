# Generated by Django 4.1.1 on 2022-12-16 16:41

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_alter_notificationperiodicity_notification_type_periodicity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationperiodicity',
            name='frequency_days',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (5, 5), (15, 15), (28, 28)], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(28)], verbose_name='дни'),
        ),
        migrations.AlterField(
            model_name='notificationperiodicity',
            name='frequency_hours',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (5, 5), (12, 12), (24, 24)], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)], verbose_name='часы'),
        ),
        migrations.AlterField(
            model_name='notificationperiodicity',
            name='frequency_months',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (3, 3), (6, 6), (12, 12)], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='месяцы'),
        ),
        migrations.AlterField(
            model_name='notificationperiodicity',
            name='notification_periodicity_num',
            field=models.IntegerField(default=1, verbose_name='количество повторений оповещения'),
        ),
        migrations.AlterField(
            model_name='notificationperiodicity',
            name='notification_status',
            field=models.ManyToManyField(to='notifications.notificationstatus', verbose_name='Выполнено'),
        ),
        migrations.AlterField(
            model_name='notificationperiodicity',
            name='notification_task_type',
            field=models.OneToOneField(default='study', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_task_type_periodic', to='notifications.notificationtype', verbose_name='тип оповещения'),
        ),
        migrations.AlterField(
            model_name='notificationperiodicity',
            name='text',
            field=models.TextField(max_length=350, verbose_name='текст оповещения'),
        ),
        migrations.AlterField(
            model_name='notificationsingle',
            name='notification_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 16, 16, 41, 56, 830270), verbose_name='Дата исполнения'),
        ),
        migrations.AlterField(
            model_name='notificationsingle',
            name='notification_status',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='notifications.notificationstatus', verbose_name='Выполнено'),
        ),
        migrations.AlterField(
            model_name='notificationsingle',
            name='notification_task_type',
            field=models.OneToOneField(default='study', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_task_type_single', to='notifications.notificationtype', verbose_name='тип оповещения'),
        ),
        migrations.AlterField(
            model_name='notificationsingle',
            name='notification_time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 16, 16, 41, 56, 830281), verbose_name='Время исполнения'),
        ),
        migrations.AlterField(
            model_name='notificationsingle',
            name='text',
            field=models.TextField(max_length=350, verbose_name='текст оповещения'),
        ),
    ]
