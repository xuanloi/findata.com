# Generated by Django 2.1.5 on 2019-02-27 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0009_auto_20190225_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfttnh',
            name='f02627',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cfttnh',
            name='f02628',
            field=models.FloatField(null=True),
        ),
    ]