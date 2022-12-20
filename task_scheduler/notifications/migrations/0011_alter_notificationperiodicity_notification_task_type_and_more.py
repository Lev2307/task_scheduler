# Generated by Django 4.1.1 on 2022-12-18 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0010_alter_notificationperiodicity_notification_type_periodicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationperiodicity',
            name='notification_task_type',
            field=models.ForeignKey(default='study', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_task_type_periodic', to='notifications.notificationtype', verbose_name='тип оповещения'),
        ),
        migrations.AlterField(
            model_name='notificationsingle',
            name='notification_task_type',
            field=models.ForeignKey(default='study', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_task_type_single', to='notifications.notificationtype', verbose_name='тип оповещения'),
        ),
    ]
