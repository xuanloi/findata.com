# Generated by Django 3.1.2 on 2020-11-08 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0106_remove_task_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(max_length=500, null=True)),
                ('content', models.TextField()),
                ('expiry', models.BooleanField(default=False)),
                ('valid_from', models.DateTimeField(null=True)),
                ('valid_to', models.DateTimeField(null=True)),
                ('image', models.CharField(max_length=200, null=True)),
                ('note', models.TextField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(null=True)),
                ('approve_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.classification')),
                ('approver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account')),
            ],
            options={
                'db_table': 'help',
            },
        ),
        migrations.CreateModel(
            name='Help_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=30, unique=True)),
                ('value', models.CharField(max_length=100)),
                ('level', models.PositiveIntegerField()),
                ('parent', models.CharField(max_length=30, null=True)),
                ('index', models.PositiveIntegerField(default=0)),
                ('icon', models.CharField(max_length=50, null=True)),
                ('image', models.CharField(max_length=500, null=True)),
                ('link', models.CharField(max_length=500, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'help_category',
            },
        ),
        migrations.CreateModel(
            name='Help_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('image', models.CharField(max_length=200, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('parent', models.BigIntegerField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account')),
                ('delete_reason', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.classification')),
                ('help', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.help')),
                ('updater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account')),
            ],
            options={
                'db_table': 'help_comment',
            },
        ),
        migrations.AddField(
            model_name='help',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.help_category'),
        ),
        migrations.AddField(
            model_name='help',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account'),
        ),
        migrations.AddField(
            model_name='help',
            name='display_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.classification'),
        ),
        migrations.AddField(
            model_name='help',
            name='updater',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account'),
        ),
        migrations.CreateModel(
            name='Help_Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(null=True)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.help_comment')),
                ('help', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.help')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.classification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account')),
            ],
            options={
                'db_table': 'help_like',
                'unique_together': {('user', 'help', 'comment')},
            },
        ),
    ]
