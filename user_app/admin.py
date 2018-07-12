# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from user_app.models import User, Uploads, Commend

admin.site.register(User)
admin.site.register(Uploads)
admin.site.register(Commend)
# Register your models here.
