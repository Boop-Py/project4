from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Post, Follow


@login_required(login_url="stronk:login")
def index(request):
    return render(request, "network/index.html", {
                    "posts": Post.objects.all().order_by("-post_time")
                    })

@login_required(login_url="stronk:login")
def create_post(request):
    if request.method == "POST":
        content = request.POST["content_input"]
        user = request.user
        Post.objects.create(
            user = user, 
            content = content)
        return HttpResponseRedirect(reverse("stronk:index"))
    else:
        return HttpResponseRedirect(reverse("stronk:index"))

@login_required(login_url="stronk:login")
def profile(request, username): 
    try:
        # fetch the user info      
        user_target = User.objects.get(username=username)
        print(user_target)
        print("test")
        #post_info = Post.objects.get(username=username)
        #print(post_info)
        #follow_info = Follow.objects.get(username=username)      
        #print(follow_info)
 
    except Exception as e:
        print(e)
        # if no user return error
        return render(request, "network/profile.html", {
            "user_target": "exception error",
            "message": "Unable to find user."
            })

    return render(request, "network/profile.html", {
                    "user_target": user_target
                    })
                  


    '''
    # retrieve posts by chosen user in time order
    posts = Post.objects.filter(user=user).order_by("-post_time")

    # django paginator to retrieve 10 at a time on a page
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)

    # get all people following the person  
    for f in profile.followed_by.all():
        print(f)
    '''      
    
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
        return HttpResponseRedirect(reverse("/stronk:index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url="stronk:login")
def following_list(request):
    return render(request, "network/following.html")

@login_required(login_url="stronk:login")
def follow(request, username):
    message = "stronk"
    try:  
        # retrieve self user ID                
        current_user = request.user
        current_user = User.objects.get(username=username)

        # retrieve the target user ID   
        user_target = User.objects.get(username=username)

        # check if follow entry already exists
        follow_exists = Follow.objects.filter(user=current_user, following=user_target).count()      
   
        # if already following present error
        if follow_exists > 0:
            return HttpResponseRedirect("/stronk/profile/" + username, {
                                        message: "You are already following this user."
                                        })
        
        # if not following, save the follow
        else:
            Follow.objects.create(
                user = current_user, 
                following = user_target)   
            # show success message
            return HttpResponseRedirect("/stronk/profile/" + username, {
                                        message: "You are now following this user!"
                                        })
        
    except Exception as e: 
        print(e)
        return HttpResponseRedirect("/stronk/profile/" + username, {
                                        message: "An error occured."
                                        })

    return HttpResponseRedirect("/stronk/profile/" + username)

@login_required(login_url="stronk:login")
def unfollow(request, username):
    message = None
    try:  
        # retrieve self user ID               
        current_user = request.user
        current_user = User.objects.get(username=username)

        # retrieve the target user ID   
        user_target = User.objects.get(username=username)

        # check if follow entry already exists
        follow_exists = Follow.objects.filter(user=current_user, following=user_target).count()       

        # if not following, display error message 
        if follow_exists == 0:
            return HttpResponseRedirect("/stronk/profile/" + username, {
                                        message: "You are not following this user."
                                        })

        # if following, remove object
        else: 
            Follow.objects.filter(user=current_user, following=user_target).delete()
            message = "test"
            return HttpResponseRedirect("/stronk/profile/" + username)
    
    except Exception as e: 
        print(e)
        return HttpResponseRedirect("/stronk/profile/" + username, {
                                        message: "An error occured."
                                        })


    return HttpResponseRedirect("/stronk/profile/" + username)

def todolist(request):
    return render(request, "network/todolist.html")



