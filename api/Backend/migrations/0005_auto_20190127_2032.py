# Generated by Django 2.1.5 on 2019-01-28 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0004_auto_20190127_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='f02591',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='f02604',
            field=models.TextField(blank=True, null=True),
        ),
    ]
