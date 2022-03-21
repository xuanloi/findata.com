# Generated by Django 3.2 on 2021-06-18 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0145_auto_20210611_1823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock_price',
            old_name='bv',
            new_name='f02966',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='eps',
            new_name='f02967',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='number_share',
            new_name='f02968',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='pb',
            new_name='f02969',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='pbi',
            new_name='f02970',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='pbm',
            new_name='f02971',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='pe',
            new_name='f02972',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='pei',
            new_name='f02973',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='pem',
            new_name='f02974',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='valuation_pbi',
            new_name='f02975',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='valuation_pbm',
            new_name='f02976',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='valuation_pei',
            new_name='f02977',
        ),
        migrations.RemoveField(
            model_name='stock_price',
            name='valuation_pem',
        ),
    ]