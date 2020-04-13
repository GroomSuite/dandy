# Generated by Django 2.2.6 on 2020-04-13 09:57

import dandy.content.utils
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='alter_image',
        ),
        migrations.RemoveField(
            model_name='article',
            name='content',
        ),
        migrations.RemoveField(
            model_name='article',
            name='keywords',
        ),
        migrations.RemoveField(
            model_name='article',
            name='label',
        ),
        migrations.RemoveField(
            model_name='article',
            name='lead_text',
        ),
        migrations.RemoveField(
            model_name='article',
            name='main_image',
        ),
        migrations.RemoveField(
            model_name='article',
            name='publish_from',
        ),
        migrations.RemoveField(
            model_name='article',
            name='publish_to',
        ),
        migrations.RemoveField(
            model_name='article',
            name='section',
        ),
        migrations.AlterField(
            model_name='article',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dandy.content.utils.get_default_article_data),
        ),
    ]
