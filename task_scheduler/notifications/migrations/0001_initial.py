# Generated by Django 4.1.1 on 2022-11-13 11:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_type', models.CharField(max_length=45)),
                ('color', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=350)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('notification_date', models.DateField(default=datetime.datetime.now)),
                ('notification_time', models.TimeField(default=datetime.datetime.now)),
                ('notification_periodicity', models.BooleanField(default=False)),
                ('notification_periodicity_num', models.IntegerField(default=1)),
                ('notification_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_color', to='notifications.notificationtype')),
                ('notification_task_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_task_type', to='notifications.notificationtype')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
    ]
