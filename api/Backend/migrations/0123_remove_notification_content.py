# Generated by Django 3.1.2 on 2020-11-15 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0122_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='content',
        ),
    ]
