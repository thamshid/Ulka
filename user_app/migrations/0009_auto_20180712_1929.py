# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-12 19:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0008_auto_20180712_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='is_primary',
        ),
        migrations.AddField(
            model_name='user',
            name='primary_email',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='primary_email', to='user_app.Email'),
            preserve_default=False,
        ),
    ]
