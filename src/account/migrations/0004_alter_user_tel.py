# Generated by Django 4.2.3 on 2023-08-24 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_tel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tel',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
