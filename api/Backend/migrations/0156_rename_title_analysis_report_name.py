# Generated by Django 3.2.6 on 2022-03-21 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0155_analysis_report_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysis_report',
            old_name='title',
            new_name='name',
        ),
    ]
