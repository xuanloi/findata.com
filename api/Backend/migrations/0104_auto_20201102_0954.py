# Generated by Django 3.1.2 on 2020-11-02 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0103_bssx_f02747'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=200)),
                ('size', models.IntegerField()),
                ('caption', models.CharField(max_length=200, null=True)),
                ('used', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account')),
            ],
            options={
                'db_table': 'image',
            },
        ),
        migrations.AlterUniqueTogether(
            name='bpbh',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='bpck',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='bpnh',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='bpsx',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='bsbh',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='bsck',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='bsnh',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='bssx',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='cfgtbh',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='cfgtck',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='cfgtnh',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='cfgtsx',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='cfttbh',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='cfttck',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='cfttnh',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='cfttsx',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='estimated',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='plan',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=200)),
                ('size', models.IntegerField()),
                ('caption', models.CharField(max_length=200, null=True)),
                ('used', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.account')),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.RemoveField(
            model_name='bpbh',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='bpbh',
            name='company',
        ),
        migrations.RemoveField(
            model_name='bpbh',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='bpbh',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='bpbh',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='bpbh',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='bpbh',
            name='year',
        ),
        migrations.RemoveField(
            model_name='bpck',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='bpck',
            name='company',
        ),
        migrations.RemoveField(
            model_name='bpck',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='bpck',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='bpck',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='bpck',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='bpck',
            name='year',
        ),
        migrations.RemoveField(
            model_name='bpnh',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='bpnh',
            name='company',
        ),
        migrations.RemoveField(
            model_name='bpnh',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='bpnh',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='bpnh',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='bpnh',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='bpnh',
            name='year',
        ),
        migrations.RemoveField(
            model_name='bpsx',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='bpsx',
            name='company',
        ),
        migrations.RemoveField(
            model_name='bpsx',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='bpsx',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='bpsx',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='bpsx',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='bpsx',
            name='year',
        ),
        migrations.RemoveField(
            model_name='bsbh',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='bsbh',
            name='company',
        ),
        migrations.RemoveField(
            model_name='bsbh',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='bsbh',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='bsbh',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='bsbh',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='bsbh',
            name='year',
        ),
        migrations.RemoveField(
            model_name='bsck',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='bsck',
            name='company',
        ),
        migrations.RemoveField(
            model_name='bsck',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='bsck',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='bsck',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='bsck',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='bsck',
            name='year',
        ),
        migrations.RemoveField(
            model_name='bsnh',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='bsnh',
            name='company',
        ),
        migrations.RemoveField(
            model_name='bsnh',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='bsnh',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='bsnh',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='bsnh',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='bsnh',
            name='year',
        ),
        migrations.RemoveField(
            model_name='bssx',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='bssx',
            name='company',
        ),
        migrations.RemoveField(
            model_name='bssx',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='bssx',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='bssx',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='bssx',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='bssx',
            name='year',
        ),
        migrations.RemoveField(
            model_name='cfgtbh',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='cfgtbh',
            name='company',
        ),
        migrations.RemoveField(
            model_name='cfgtbh',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='cfgtbh',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='cfgtbh',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='cfgtbh',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='cfgtbh',
            name='year',
        ),
        migrations.RemoveField(
            model_name='cfgtck',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='cfgtck',
            name='company',
        ),
        migrations.RemoveField(
            model_name='cfgtck',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='cfgtck',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='cfgtck',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='cfgtck',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='cfgtck',
            name='year',
        ),
        migrations.RemoveField(
            model_name='cfgtnh',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='cfgtnh',
            name='company',
        ),
        migrations.RemoveField(
            model_name='cfgtnh',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='cfgtnh',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='cfgtnh',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='cfgtnh',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='cfgtnh',
            name='year',
        ),
        migrations.RemoveField(
            model_name='cfgtsx',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='cfgtsx',
            name='company',
        ),
        migrations.RemoveField(
            model_name='cfgtsx',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='cfgtsx',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='cfgtsx',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='cfgtsx',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='cfgtsx',
            name='year',
        ),
        migrations.RemoveField(
            model_name='cfttbh',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='cfttbh',
            name='company',
        ),
        migrations.RemoveField(
            model_name='cfttbh',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='cfttbh',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='cfttbh',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='cfttbh',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='cfttbh',
            name='year',
        ),
        migrations.RemoveField(
            model_name='cfttck',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='cfttck',
            name='company',
        ),
        migrations.RemoveField(
            model_name='cfttck',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='cfttck',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='cfttck',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='cfttck',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='cfttck',
            name='year',
        ),
        migrations.RemoveField(
            model_name='cfttnh',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='cfttnh',
            name='company',
        ),
        migrations.RemoveField(
            model_name='cfttnh',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='cfttnh',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='cfttnh',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='cfttnh',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='cfttnh',
            name='year',
        ),
        migrations.RemoveField(
            model_name='cfttsx',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='cfttsx',
            name='company',
        ),
        migrations.RemoveField(
            model_name='cfttsx',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='cfttsx',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='cfttsx',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='cfttsx',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='cfttsx',
            name='year',
        ),
        migrations.RemoveField(
            model_name='estimated',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='estimated',
            name='company',
        ),
        migrations.RemoveField(
            model_name='estimated',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='estimated',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='estimated',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='estimated',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='estimated',
            name='year',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='assigner',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='company',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='report_name',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='report_period',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='report_type',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='year',
        ),
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.file'),
        ),
        migrations.CreateModel(
            name='Task_Related',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('related', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task')),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task')),
            ],
            options={
                'db_table': 'task_related',
                'unique_together': {('task', 'related')},
            },
        ),
        migrations.CreateModel(
            name='Task_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.image')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.task')),
            ],
            options={
                'db_table': 'task_image',
                'unique_together': {('task', 'image')},
            },
        ),
    ]
