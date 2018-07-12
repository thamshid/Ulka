# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import now
from django.views import View

from ulka.custom_mixin import AdminCheckMixin
from user_app.forms import SignUpForm, LogInForm
from user_app.models import User


class HomeView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponseRedirect('/user-list')
        else:
            return HttpResponseRedirect('/dashboard')


class SignUpView(View):
    template_name = 'sign_up.html'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        form = self.form_class(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.data['email']).exists():
                return render(request, self.template_name, {'form': self.form_class, 'errors': "Email Already Exist!"})
            user = User.objects.create(email=form.data['email'], name=form.data['name'])
            user.set_password(form.data['password'])
            user.save()
            user = authenticate(email=form.data['email'], password=form.data['password'])
            login(request, user)
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class LogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class LogInView(View):
    template_name = 'login.html'
    form_class = LogInForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(email=form.data['email'], password=form.data['password'])
            login_try = User.objects.filter(email=form.data['email']).last()
            if user is None:
                if login_try:
                    login_try.invalid_attempts_count = login_try.invalid_attempts_count + 1
                    login_try.last_invalid_attempt = now()
                    login_try.save()
                    if (now() - login_try.last_invalid_attempt).seconds < 300 and login_try.invalid_attempts_count > 3:
                        return render(request, self.template_name, {'form': form, "errors": "Your account is blocked"})

                return render(request, self.template_name, {'form': form, "errors": "Invalid email or password!"})
            if (now() - user.last_invalid_attempt).seconds < 300 and user.invalid_attempts_count > 3:
                return render(request, self.template_name, {'form': form, "errors": "Your account is blocked"})
            login(request, user)
            user.invalid_attempts_count = 0
            user.save()
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class UserListView(AdminCheckMixin, View):
    template_name = 'user_list.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_superuser=False)
        return render(request, self.template_name, {'users': users})