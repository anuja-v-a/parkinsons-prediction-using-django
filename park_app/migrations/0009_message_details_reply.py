# Generated by Django 4.1.3 on 2022-11-06 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('park_app', '0008_rename_message_message_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='message_details',
            name='reply',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
