# Generated by Django 3.1.2 on 2020-11-02 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0105_auto_20201102_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='report',
        ),
    ]