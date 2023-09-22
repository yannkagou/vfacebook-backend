# Generated by Django 4.2.3 on 2023-08-23 12:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0003_notification_page_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='created_for',
        ),
        migrations.AddField(
            model_name='notification',
            name='created_for',
            field=models.ManyToManyField(related_name='received_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]