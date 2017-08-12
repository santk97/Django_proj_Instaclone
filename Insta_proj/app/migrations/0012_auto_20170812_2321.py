# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_post_model_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post_model',
            old_name='tags',
            new_name='tag1',
        ),
        migrations.AddField(
            model_name='post_model',
            name='tag2',
            field=models.CharField(default='products', max_length=1000),
        ),
        migrations.AddField(
            model_name='post_model',
            name='tag3',
            field=models.CharField(default='products', max_length=1000),
        ),
    ]
