# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]