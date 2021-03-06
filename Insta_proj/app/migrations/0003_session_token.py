# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 12:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170723_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='session_token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=250)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('valid', models.BooleanField(default=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user_details')),
            ],
        ),
    ]
