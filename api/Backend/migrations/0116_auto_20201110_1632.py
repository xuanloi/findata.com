# Generated by Django 3.1.2 on 2020-11-10 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0115_task_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='foreigner_order',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock_order',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock_price',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task'),
            preserve_default=False,
        ),
    ]
