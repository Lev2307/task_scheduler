# Generated by Django 4.1.1 on 2022-10-04 20:04

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
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_task_type', models.CharField(choices=[('по работе', 'Work'), ('по учёбе', 'Study'), ('общее', 'General')], default='по работе', max_length=30)),
                ('text', models.TextField(max_length=350)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('notification_time', models.DateField()),
                ('notification_periodicity', models.BooleanField(default=False)),
                ('notification_periodicity_num', models.IntegerField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
