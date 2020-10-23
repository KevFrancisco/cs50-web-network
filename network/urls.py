
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("user/<int:user_id>", views.user_profile, name="user_profile"),
    path("user/follow/<int:user_id>", views.follow_toggle, name="follow_toggle"),
]