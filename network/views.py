from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
    return render(request, "network/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("stronk:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("stronk:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("stronk:index"))
    else:
        return render(request, "network/register.html")

def following(request):
    return render(request, "network/following.html")

def todolist(request):
    return render(request, "network/todolist.html")

def profile(request, user):
     # retrieve details from db using name
    User = User.objects.filter(user=user).first()

    # retrieve posts in order of date    
    posts = Post.objects.filter(post=posting).order_by("-post_date")
    post_list = []

    #list of all posts
    for p in posts:
        post = p.posts
        posts_list.append(post)
                     
    return render(request, "network/profile.html",
                      {"u": user, 
                       "post": Post.objects.filter(post=posting)
                       })                      
     
    return render(request, "network/profile.html")