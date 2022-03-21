# Generated by Django 3.1.2 on 2021-02-08 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0142_auto_20210129_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foreign_deal',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.company'),
        ),
        migrations.AlterField(
            model_name='foreign_order',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.company'),
        ),
        migrations.AlterField(
            model_name='price_live',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.company'),
        ),
        migrations.AlterField(
            model_name='stock_order',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.company'),
        ),
        migrations.AlterField(
            model_name='stock_price',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.company'),
        ),
    ]
