from django.conf import settings
from django.urls import include, path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("create", views.create, name="create"),
    path("like/<int:id>", views.like, name="like"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("todolist", views.todolist, name="todolist"),
    path("edit/<int:id>", views.edit_post, name="edit_post")

]