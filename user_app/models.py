# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class Email(models.Model):
    email = models.EmailField(max_length=500)

class AuthUserManager(BaseUserManager):
    """
    Customized Authentication Manager
    """

    def create_user(self, email, password=None):
        """
        Overridden create_user method
        """
        user = self.model(email=email)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Overridden create_superuser method
        """
        user = self.create_user(email=email, password=password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    class Meta(object):
        """
            Meta class
        """
        db_table = 'auth_user_manager'
        verbose_name_plural = "Auth User Manager"


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    last_invalid_attempt = models.DateTimeField(auto_now_add=True)
    invalid_attempts_count = models.IntegerField(default=0)
    location = models.CharField(max_length=25, null=True, blank=True)
    emails = models.ManyToManyField(Email)
    primary_email = models.ForeignKey(Email, related_name='primary_email', null=True)


    objects = AuthUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.name

class Uploads(models.Model):
    user = models.ForeignKey(User)
    file = models.FileField()

class Commend(models.Model):
    upload = models.ForeignKey(Uploads)
    comment = models.CharField(max_length=500)
    reply = models.CharField(max_length=500, null=True, blank=True)






