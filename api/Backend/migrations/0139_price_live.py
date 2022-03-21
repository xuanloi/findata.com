# Generated by Django 3.1.2 on 2021-01-01 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0138_auto_20201223_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price_Live',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_date', models.DateField()),
                ('time', models.TimeField()),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('f02797', models.FloatField(null=True)),
                ('f02798', models.FloatField(null=True)),
                ('f02799', models.FloatField(null=True)),
                ('f02800', models.FloatField(null=True)),
                ('f02801', models.FloatField(null=True)),
                ('f02802', models.FloatField(null=True)),
                ('f02803', models.FloatField(null=True)),
                ('f02804', models.FloatField(null=True)),
                ('f02805', models.FloatField(null=True)),
                ('f02806', models.FloatField(null=True)),
                ('f02807', models.FloatField(null=True)),
                ('f02808', models.FloatField(null=True)),
                ('f02809', models.FloatField(null=True)),
                ('f02810', models.FloatField(null=True)),
                ('f02811', models.FloatField(null=True)),
                ('f02812', models.FloatField(null=True)),
                ('f02813', models.FloatField(null=True)),
                ('f02814', models.FloatField(null=True)),
                ('f02815', models.FloatField(null=True)),
                ('f02816', models.FloatField(null=True)),
                ('f02817', models.FloatField(null=True)),
                ('f02818', models.FloatField(null=True)),
                ('f02819', models.FloatField(null=True)),
                ('f02820', models.FloatField(null=True)),
                ('f02821', models.FloatField(null=True)),
                ('f02822', models.FloatField(null=True)),
                ('f02823', models.FloatField(null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.company')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task_stock')),
            ],
            options={
                'db_table': 'price_live',
                'unique_together': {('stock_date', 'time', 'company')},
            },
        ),
    ]