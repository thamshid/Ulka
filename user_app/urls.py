from django.conf.urls import url

from user_app.views import SignUpView, LogOutView, LogInView, HomeView, UserListView, DashboardView, UploadView, \
    UserInfoView, ReplyView, CommendView, ProfileView, EmailView, PrimaryView

urlpatterns = [
    url(r'^sign-up$', SignUpView.as_view()),
    url(r'^logout$', LogOutView.as_view()),
    url(r'^login', LogInView.as_view()),
    url(r'^user-list', UserListView.as_view()),
    url(r'^dashboard', DashboardView.as_view()),
    url(r'^profile', ProfileView.as_view()),
    url(r'^upload', UploadView.as_view()),
    url(r'^email', EmailView.as_view()),
    url(r'^user-info/(?P<pk>[0-9]+)$', UserInfoView.as_view()),
    url(r'^reply/(?P<pk>[0-9]+)$', ReplyView.as_view()),
    url(r'^commend/(?P<pk>[0-9]+)$', CommendView.as_view()),
    url(r'^set-primary/(?P<pk>[0-9]+)$', PrimaryView.as_view()),
    url(r'^', HomeView.as_view()),
]
