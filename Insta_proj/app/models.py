# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
# Create your models here.

class user_details(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    username = models.CharField(max_length=120 ,)
    password = models.CharField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class session_token(models.Model):
    username=models.ForeignKey(user_details)
    token=models.CharField(max_length=250)
    created_on=models.DateTimeField(auto_now_add=True)
    valid=models.BooleanField(default=True)

    def create_token(self):
        self.token=uuid.uuid4()


class post_model(models.Model):
    username=models.ForeignKey(user_details)
    image=models.FileField(upload_to='user_images')
    image_url=models.CharField(max_length=250)
    caption=models.CharField(max_length=400)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)