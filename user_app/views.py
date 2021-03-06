# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geoip import GeoIP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import now
from django.views import View

from ulka.custom_mixin import AdminCheckMixin, NormalUserCheckMixin
from user_app.forms import SignUpForm, LogInForm, UploadForm, ReplyForm, CommendForm, EmailForm
from user_app.models import User, Uploads, Commend, Email


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

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        form = self.form_class(request.POST)
        if form.is_valid():
            if Email.objects.filter(email=form.data['email']).exists():
                return render(request, self.template_name, {'form': self.form_class, 'errors': "Email Already Exist!"})
            email = Email.objects.create(email=form.data['email'])
            user = User.objects.create(email=form.data['email'], name=form.data['name'], primary_email=email)
            user.set_password(form.data['password'])
            user.emails.add(email)
            g = GeoIP()
            ip = self.get_client_ip(request)
            user.location = g.country(ip)['country_code']
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
            user = User.objects.filter(primary_email__email=form.data['email']).last()
            if user and not user.check_password(form.data['password']):
                user = None
            login_try = User.objects.filter(primary_email__email=form.data['email']).last()
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

        return render(request, self.template_name, {'form': self.form_class})


class UserListView(AdminCheckMixin, View):
    login_url = '/'
    template_name = 'user_list.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_superuser=False)
        return render(request, self.template_name, {'users': users})


class UserInfoView(AdminCheckMixin, View):
    login_url = '/'
    template_name = 'user_info.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        return render(request, self.template_name, {'user': user, 'commend_form': CommendForm})


class DashboardView(NormalUserCheckMixin, View):
    login_url = '/'
    template_name = 'dashboard.html'
    form_class = UploadForm

    def get(self, request, *args, **kwargs):
        files = Uploads.objects.filter(user=request.user)
        return render(request, self.template_name,
                      {'user': request.user, 'form': self.form_class, 'files': files, 'reply_form': ReplyForm})


class UploadView(NormalUserCheckMixin, View):
    form_class = UploadForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            Uploads.objects.create(user=request.user, file=form.files['file'])
        return HttpResponseRedirect('/dashboard')


class ReplyView(NormalUserCheckMixin, View):
    form_class = ReplyForm

    def post(self, request, *args, **kwargs):
        commend = Commend.objects.get(id=kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            commend.reply = form.data['reply']
            commend.save()
        return HttpResponseRedirect('/dashboard')


class CommendView(AdminCheckMixin, View):
    form_class = CommendForm

    def post(self, request, *args, **kwargs):
        upload = Uploads.objects.get(id=kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            Commend.objects.create(comment=form.data['commend'], upload=upload)
        return HttpResponseRedirect('/user-info/' + str(upload.user.id))


class ProfileView(NormalUserCheckMixin, View):
    template_name = 'profile.html'
    form_class = EmailForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'user': request.user, 'email_form': self.form_class})


class EmailView(NormalUserCheckMixin, View):
    template_name = 'profile.html'
    form_class = EmailForm

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)
        if Email.objects.filter(email=form.data['email']).exists():
            return render(request, self.template_name,
                          {'user': request.user, 'email_form': self.form_class, 'error': "Email already exist!"})
        if form.is_valid():
            email = Email.objects.create(email=form.data['email'])
            user.emails.add(email)
            email.save()
            user.save()
        return render(request, self.template_name,
                      {'user': request.user, 'email_form': self.form_class})


class PrimaryView(NormalUserCheckMixin, View):
    template_name = 'profile.html'
    form_class = EmailForm

    def get(self, request, *args, **kwargs):
        user = request.user
        email = user.emails.get(id=kwargs['pk'])
        user.primary_email = email
        user.save()
        return render(request, self.template_name,
                      {'user': request.user, 'email_form': self.form_class})
