# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 05:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_session_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='post_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='user_images')),
                ('image_url', models.CharField(max_length=250)),
                ('caption', models.CharField(max_length=400)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user_details')),
            ],
        ),
    ]