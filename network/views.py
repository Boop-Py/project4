from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Post, Follow


## TODO 
# page of posts from followed people
# like 
# unliked
# edit post

@login_required(login_url="stronk:login")
def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, "network/index.html", {
                    "posts": posts
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
                      
        # other people following this person
        followers = Follow.objects.filter(user=user_target)
        
        # people this person follows
        following = Follow.objects.filter(following=user_target)
               
        followers_count = followers.count()
        following_count = following.count()

        print(f"{user_target} follows: {followers_count}")
        print(f"{user_target} is followed by {following_count}")
        
        # posts in reverse id order
        posts = Post.objects.filter(user=user_target).order_by("id").reverse()
        paginator = Paginator(posts, 10)
        if request.GET.get("page") != None:
            try:
                posts = paginator.page(request.GET.get("page"))
            except:
                posts = paginator.page(1)
        else:
            posts = paginator.page(1)

    except Exception as e:
        print(e)
        # if no user return error
        return render(request, "network/profile.html", {
            "user_target": "exception error",
            "message": "Unable to find user."
            })

    return render(request, "network/profile.html", {
                    "user_target": user_target,
                    "posts": posts,
                    "following_count": following_count,
                    "followers_count": followers_count                   
                    })
                     
@login_required(login_url="stronk:login")
def following_list(request):
    # retrieve current user
    current_user = request.user 
    
    current_user_object = User.objects.get(username=current_user)
    
    # all people person is following
    followed = Follow.objects.filter(user=current_user)

    followed_count = followed.count()
    print(f"Following: {followed_count} people")
    print(followed)
    posts = []
    #for follow in followed:
    
    follow_users = [4,2,6] # DO NOT GIVE ME USER OBJECTS - DO A TYPE INPSECTION!
    
    all_posts = Post.objects.all().filter(user_id__in=follow_users).order_by("id").reverse()
    for post in all_posts:
        posts.append(post)
    # all posts by those people
    print(f"{posts.count} posts by: {followed.count} users")
    
    return render(request, "network/following.html", {
                    "posts": posts
                    })

@login_required(login_url="stronk:login")
def follow(request, username):
    try:  
        # retrieve self user ID                
        current_user = request.user

        # retrieve the target user ID   
        user_target = User.objects.get(username=username)
        
        # ensure user can't follow themselves 
        if current_user == user_target:
            return HttpResponseRedirect("/stronk/profile/" + username, {
                                        "message": "You can't follow yourself!."
                                        })
        else:
            # check if follow entry already exists
            follow_exists = Follow.objects.filter(user=current_user, following=user_target).count()   
            
            # if already following present error
            if follow_exists > 0:
                return HttpResponseRedirect("/stronk/profile/" + username, {
                                            "message": "You are already following this user."
                                            })
            
            # if not following, save the follow
            else:
                Follow.objects.create(
                    user = current_user, 
                    following = user_target)   
                # show success message
                return HttpResponseRedirect("/stronk/profile/" + username, {
                                            "message": "You are now following this user!"
                                            })
            
    except Exception as e: 
        print(e)
        return HttpResponseRedirect("/stronk/profile/" + username, {
                                        "message": "An error occured."
                                        })

    return HttpResponseRedirect("/stronk/profile/" + username)

@login_required(login_url="stronk:login")
def unfollow(request, username):
    try:  
        # retrieve self user ID               
        current_user = request.user

        # retrieve the target user ID   
        user_target = User.objects.get(username=username)

        # check if follow entry already exists
        follow_exists = Follow.objects.filter(user=current_user, following=user_target).count()       
        # if not following, display error message 
        if follow_exists == 0:
            return HttpResponseRedirect("/stronk/profile/" + username, {
                                        "message": "You are not following this user."
                                        })

        # if following, remove object
        else: 
            Follow.objects.filter(user=current_user, following=user_target).delete()
            return HttpResponseRedirect("/stronk/profile/" + username)
    
    except Exception as e: 
        print(e)
        return HttpResponseRedirect("/stronk/profile/" + username, {
                                        "message": "An error occured."
                                        })

    return HttpResponseRedirect("/stronk/profile/" + username)

def like(request):
    if request.method == "POST":
        # get name of current user
        current_user = request.user
        # retrieve id of the post that's been like/unliked
        post_id = request.POST.get("id")
        # check if post has likes 
        like_status = request.POST.get("liked_by")
        try:        
            post = Post.objects.get(id=liked_post)
            # if clicked on unliked post, add the like
            if like_status == "unliked":
                post.liked_by.add(current_user)
                like_status = "liked"
            # if clicked on liked post, add the like    
            elif like_status == "liked":
                post.liked_by.remove(current_user)
                like_status = "unliked"
            post.save()
            return HttpResponseRedirect(reverse("stronk:index"))
        except:
            return HttpResponseRedirect(reverse("stronk:index"))
    else: 
        return HttpResponseRedirect(reverse("stronk:index"))

def todolist(request):
    return render(request, "network/todolist.html")

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


