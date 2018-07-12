from django.conf.urls import url

from user_app.views import SignUpView, LogOutView, LogInView, HomeView, UserListView

urlpatterns = [
    url(r'^sign-up$', SignUpView.as_view()),
    url(r'^logout$', LogOutView.as_view()),
    url(r'^login', LogInView.as_view()),
    url(r'^user-list', UserListView.as_view()),
    url(r'^', HomeView.as_view()),
]