# Generated by Django 2.1.5 on 2019-03-07 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0011_auto_20190301_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='bpbh',
            name='f02633',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cfgtbh',
            name='f02632',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cfttbh',
            name='f02631',
            field=models.FloatField(null=True),
        ),
    ]
