# Generated by Django 3.1.2 on 2020-11-13 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0119_auto_20201112_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='data_file',
            field=models.TextField(blank=True, null=True),
        ),
    ]
