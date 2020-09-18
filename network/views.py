from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from network.models import User, Post, Follower, Like
from django import forms
from django.db.models import OuterRef, Subquery, Count, Exists
from django.views.generic import ListView
from django.core.paginator import Paginator
import time

MAX_POSTS_PER_PAGE = 10

## TODO
# input box not hiding
# tidy up the posts 


class Create_Post_Form(forms.Form):
    post_text = forms.Field(widget=forms.Textarea(
                            {"rows": "3", 
                            "maxlength": 160, 
                            "class": "ui field", 
                            "placeholder": "Write something..."}), 
                            label="New Post", 
                            required=True)

class Edit_Post_Form(forms.Form):
    id_edit_text = forms.Field(widget=forms.Textarea(
                                    {"rows": "3", 
                                    "maxlength": 160, 
                                    "class": "ui field", 
                                    "placeholder": "", 
                                    "id": "id_edit_text"}), 
                                    label="New Post", 
                                    required=True)

def index(request):
    if request.user.is_authenticated:
        user = request.session["_auth_user_id"]
        likes = Like.objects.filter(post=OuterRef("id"), 
                                    user_id=user)
        posts = Post.objects.filter().order_by(
                                "-post_date")
    else:
        posts = Post.objects.order_by("-post_date").all()

    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
                    "posts": page_obj,
                    "form": Create_Post_Form(),
                    "form_edit": Edit_Post_Form()
    })

def following(request):
    if request.user.is_authenticated:
        user = request.session["_auth_user_id"]
        followers = Follower.objects.filter(follower=user)
        likes = Like.objects.filter(post=OuterRef("id"),
                                    user_id=user)
        posts = Post.objects.filter(user_id__in=followers.values("following_id")).order_by(
                                    "-post_date")
    else:
        return HttpResponseRedirect(reverse("login"))

    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
                    "posts": page_obj
    })

def create(request):
    if request.method == "POST":
        form = Create_Post_Form(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.session["_auth_user_id"])
            text = form.cleaned_data["post_text"]
            post = Post(user=user, 
                        text=text)
            post.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

def edit_post(request, id):
    if request.is_ajax and request.method == "POST":
        form = Edit_Post_Form(request.POST)
        if form.is_valid():
            text = form.cleaned_data["id_edit_text"]
            Post.objects.filter(
                                id=id, 
                                user_id=request.session["_auth_user_id"]).update(text=text)
            return JsonResponse({"result": "ok", 
                                "text": text})
        else:
            return JsonResponse({"error": form.errors}, 
                                status=400)

    return JsonResponse({"error": HttpResponseBadRequest("Bad Request: no like chosen")}, 
                        status=400)

def follow(request, id):
    try:
        result = "follow"
        current_user = request.user
        user = User.objects.get(username=current_user)      
        target_user = User.objects.get(id=id)

        # check follow exists. if doesn't exist, create it. 
        follower = Follower.objects.get_or_create(
                                    follower=user, 
                                    following=target_user) 
        print(f"{user} is now following {target_user}")                            
        
        # if exists, remove
        if not follower[1]: 
            Follower.objects.filter(follower=user, following=target_user).delete()
            print("follow removed")
            result = "unfollow"
            
        # count all the follows 
        following_target = Follower.objects.filter(following=target_user)
        all_following_target = following_target.count()
        print(f"total folos on this user: {all_following_target}")
        
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Bad Request: Unable to follow")
        
    return JsonResponse({
                    "result": result, 
                    "total_followers": all_following_target
    })

def like(request, id):
    try:
        current_user = request.user
        user = User.objects.get(username=current_user)
        post = Post.objects.get(id=id)

        # check like exists. if doesn't exist, create it. 
        like = Like.objects.get_or_create(user=user, post=post)
        print("like added")
        
        # if exists, remove
        if not like[1]: 
            Like.objects.filter(user=user, post=post).delete()
            print("like deleted")
               
        # count all the likes       
        likes_on_post = Like.objects.filter(post=post)
        all_likes_on_post = likes_on_post.count()      
        print(f"total likes on this post: {all_likes_on_post}")
        
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Bad Request: Error liking this post")
        
    return JsonResponse({
                    "like": id, 
                    "total_likes": all_likes_on_post
    })

def profile(request, username):
    is_following = 0
    profile_user = User.objects.get(username=username)
    if request.user.is_authenticated:
        logged_user = request.session["_auth_user_id"]
        is_following = Follower.objects.filter(
                                follower = logged_user, 
                                following = profile_user).count()
        likes = Like.objects.filter(post = OuterRef("id"), 
                                user_id = logged_user)
        posts = Post.objects.filter(user = profile_user).order_by(
                                    "post_date")
    else:
        posts = Post.objects.filter(
            user=profile_user).order_by("post_date").all()
    
    total_following = Follower.objects.filter(
        follower=profile_user).count()
    total_followers = Follower.objects.filter(
        following=profile_user).count()

    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
                    "profile_user": profile_user, 
                    "posts": page_obj, 
                    "is_following": is_following, 
                    "total_following": total_following, 
                    "total_followers": total_followers, 
                    "form": Create_Post_Form(), 
                    "form_edit": Edit_Post_Form()
    })

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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")