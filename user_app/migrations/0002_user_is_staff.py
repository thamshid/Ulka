# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-12 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]