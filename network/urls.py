
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("user/<int:user_id>", views.user_profile, name="user_profile"),
    path("user/follow", views.follow_toggle, name="follow_toggle"),
    path("post/like", views.like_post, name="like_post"),
    path("post/edit", views.edit_post, name="edit_post"),
    path("post/delete", views.delete_post, name="delete_post"),
    path("following", views.following, name="following"),
]