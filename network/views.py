from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow



def index(request):
    return render(request, "network/index.html", {
                    "posts": Post.objects.all().order_by("-post_time")
                    })

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

def profile(request, username): 
    try:
        #all_info = User.objects.get()
       # print(all_info)

        # fetch the user      
        user_target = User.objects.get(username=username)
        print(user_target)
        print(user_target.id)

        # retrieve profile info using the username
        #profile = Profile.objects.get(user=user_target)
        #print(profile)
        
    except Exception as e:
        print(e)
        # if no user return error
        return render(request, "network/profile.html", {
            "user_target": "exception error",
            "name_error": True
            })

    return render(request, "network/profile.html", {
                    "user_target": user_target, 
                    "profile": "fghn"
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
        return HttpResponseRedirect(reverse("stronk:index"))
    else:
        return render(request, "network/register.html")

def following_list(request):
    return render(request, "network/following.html")

def follow_action(request, username):
    if request.method == "POST":
        current_user = request.POST.get("user")
        action = request.POST.get("action")

        if action == "Follow":
            try:      
                # retrieve self user ID                
                current_user = request.user
                current_user_id = current_user.id
                print(current_user_id)

                # retrieve the target user ID   
                user_target = User.objects.get(username=username)
                user_target_id = user_target.id
                print(user_target_id)

                Follow.objects.create(
                        user = current_user_id, 
                        following = user_target_id) 
                print("save successful")


                
            except Exception as e: 
                print(e)
                return render(request, "network/profile.html")

        elif action == "Unfollow":
           # try:
                # remove user from list
               # user = User.objects.get(username=user)
              #  profile = Profile.objects.get(user=request.user)
               # profile.following.remove(user)
               # profile.save()

                # remove user from list
              #  profile = Profile.objects.get(user=user)
              #  profile.follower.remove(request.user)
              #  profile.save()  

            #except: 
                r#eturn render(request, "network/profile.html")    

    else: 
            return render(request, "network/profile.html")



    return JsonResponse({}, status=400)

def todolist(request):
    return render(request, "network/todolist.html")



