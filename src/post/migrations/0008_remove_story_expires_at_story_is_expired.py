# Generated by Django 4.2.3 on 2023-08-21 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_story_expires_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='expires_at',
        ),
        migrations.AddField(
            model_name='story',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]