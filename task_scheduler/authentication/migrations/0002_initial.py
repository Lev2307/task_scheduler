# Generated by Django 4.1.1 on 2022-10-24 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='notification_type',
            field=models.ManyToManyField(to='notifications.notificationtype'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]