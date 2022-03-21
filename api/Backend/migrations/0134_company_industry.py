# Generated by Django 3.1.2 on 2020-12-18 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0133_industry'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.industry'),
        ),
    ]