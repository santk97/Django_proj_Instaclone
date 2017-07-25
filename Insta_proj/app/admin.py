# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from models import user_details,session_token

admin.site.register(user_details)
admin.site.register(session_token)