# Generated by Django 3.0 on 2019-12-05 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0091_auto_20191128_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='entry_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='waiting1_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='waiting2_time',
            field=models.DateTimeField(null=True),
        ),
    ]
