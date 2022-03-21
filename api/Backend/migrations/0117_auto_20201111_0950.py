# Generated by Django 3.1.2 on 2020-11-11 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0116_auto_20201110_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foreigner_order',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task_stock'),
        ),
        migrations.AlterField(
            model_name='stock_order',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task_stock'),
        ),
        migrations.AlterField(
            model_name='stock_price',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task_stock'),
        ),
    ]
