# Generated by Django 4.1.1 on 2022-11-13 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='notification_color',
        ),
    ]
