# Generated by Django 3.1.2 on 2020-11-09 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0109_category_news_news_comment_news_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='avatar',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
