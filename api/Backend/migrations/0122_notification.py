# Generated by Django 3.1.2 on 2020-11-15 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0121_task_stock_data_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('seen', models.BooleanField(default=False)),
                ('refid', models.PositiveIntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.classification')),
            ],
            options={
                'db_table': 'notification',
            },
        ),
    ]