# Generated by Django 3.2.8 on 2022-11-02 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('park_app', '0002_register_details_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register_details',
            name='job_level',
        ),
    ]
