# Generated by Django 2.1.5 on 2019-01-31 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0005_auto_20190127_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='ESTIMATED',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(null=True)),
                ('enable', models.BooleanField(default=True)),
                ('f02605', models.FloatField(null=True)),
                ('f02606', models.FloatField(null=True)),
                ('f02607', models.FloatField(null=True)),
                ('f02608', models.TextField(blank=True, null=True)),
                ('f02609', models.FloatField(null=True)),
                ('f02610', models.FloatField(null=True)),
                ('f02611', models.FloatField(null=True)),
                ('f02612', models.FloatField(null=True)),
                ('f02613', models.FloatField(null=True)),
                ('f02614', models.FloatField(null=True)),
                ('f02615', models.FloatField(null=True)),
                ('f02616', models.FloatField(null=True)),
                ('f02617', models.FloatField(null=True)),
                ('f02618', models.FloatField(null=True)),
                ('f02619', models.FloatField(null=True)),
                ('f02620', models.FloatField(null=True)),
                ('f02621', models.TextField(blank=True, null=True)),
                ('total_fields', models.FloatField(null=True)),
                ('entered_fields', models.FloatField(null=True)),
                ('pending_fields', models.FloatField(null=True)),
                ('percentage', models.FloatField(null=True)),
                ('marked_fields', models.FloatField(null=True)),
                ('assigner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.Account')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.Company')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.Account')),
                ('report_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.Classification')),
                ('report_period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.Classification')),
                ('report_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.Classification')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.Task')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='Backend.Classification')),
            ],
            options={
                'db_table': 'ESTIMATED',
            },
        ),
        migrations.AlterUniqueTogether(
            name='estimated',
            unique_together={('company', 'report_period', 'year', 'report_type', 'report_name')},
        ),
    ]
