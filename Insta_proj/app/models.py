# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
# Create your models here.

class user_details(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.username

class session_token(models.Model):
    username=models.ForeignKey(user_details)
    token=models.CharField(max_length=250)
    created_on=models.DateTimeField(auto_now_add=True)
    valid=models.BooleanField(default=True)

    def create_token(self):
        self.token=uuid.uuid4()

    def __str__(self):
        return self.username


class post_model(models.Model):
    username=models.ForeignKey(user_details)
    image=models.FileField(upload_to='user_images')
    image_url=models.CharField(max_length=250)
    caption=models.CharField(max_length=400)
    has_liked=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return len(likes.objects.filter(post=self))

    @property
    def comments(self):
        return comment.objects.filter(post=self).order_by('created_on')

    def __str__(self):
        return self.username.name + '  ' +   self.image_url


class likes(models.Model):
    username= models.ForeignKey(user_details)
    post=models.ForeignKey(post_model)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return len(likes.objects.filter(post=self))

    def __str__(self):
        return self.username.name + '  has liked  '


class comment(models.Model):
    username=models.ForeignKey(user_details)
    post=models.ForeignKey(post_model)
    comment_text=models.CharField(max_length=600)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username.name + '  has commented  '

