# Generated by Django 3.0 on 2020-06-18 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0100_auto_20200609_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfttck',
            name='f02745',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cfttck',
            name='f02746',
            field=models.FloatField(null=True),
        ),
    ]
