# Generated by Django 4.2.3 on 2023-08-10 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_of_notification',
            field=models.CharField(choices=[('new_friendrequest', 'New friendrequuest'), ('accepted_friendrequest', 'Accepted friendrequest'), ('rejected_friendrequest', 'Rejected friendrequest'), ('post_like', 'Post like'), ('post_comment', 'Post comment')], max_length=50),
        ),
    ]
