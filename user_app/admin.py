# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from user_app.models import User, Uploads

admin.site.register(User)
admin.site.register(Uploads)
# Register your models here.
