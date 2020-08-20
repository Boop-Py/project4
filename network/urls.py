
from django.urls import path

from . import views

app_name = "stronk"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following_list", views.following_list, name="following_list"),
    path("follow_action", views.follow_action, name="follow_action"),
    path("todolist", views.todolist, name="todolist"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<str:username>", views.profile, name="profile")
]
