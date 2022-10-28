from ast import Delete
import json
import profile
from types import NoneType
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from .models import User, Post, Profile, Follow

def userAisfollowinguserB(userA, userB):
    if Follow.objects.filter(user_id = userA, following_user_id = userB ).exists():
        return True
    else:
        return False



def index(request):
    allPosts = Post.objects.all()
    return render(request, "network/index.html",{
        "allPosts": allPosts
    })

@csrf_exempt
@login_required
def new_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    body = data.get("body", "")

    new_post = Post(
        poster = request.user,
        body = body
    )
    new_post.save()
    return JsonResponse({"message": "Post successful."}, status=201)

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
            profile = Profile(
                profile_owner = user
            )
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def view_profile(request, profile_owner):
    current_user = request.user
    selected_user= User.objects.get(username = profile_owner)
    selected_profile = Profile.objects.get(profile_owner = selected_user)
    name = selected_user.username
    image = selected_profile.profile_picture
    allPosts = Post.objects.filter(poster = selected_user)
    followercount = countfollowers(selected_user)
    followingcount = countfollowing(selected_user)
    if userAisfollowinguserB(current_user, selected_user) == False:
        follow_button = "follow"
    else:
        follow_button = "unfollow"
    return render(request, "network/profile.html", {
        "name": name,
        "image": image,
        "follow_button": follow_button,
        "allPosts": allPosts,
        "followercount": followercount,
        "followingcount": followingcount
    })

def createFollow(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    profile_name = data.get("body", "")

    current_user = request.user
    selected_user= User.objects.get(username = profile_name)
    if current_user != selected_user:
        if userAisfollowinguserB(current_user, selected_user) == False:
            selectedfollow = Follow.objects.create(user_id = current_user, following_user_id = selected_user)
            selectedfollow.save()
        else:
            selectedfollow = Follow.objects.get(user_id = current_user, following_user_id = selected_user)
            selectedfollow.delete()

        return JsonResponse({"message": "Follow successful."}, status=201)
    else:
        return JsonResponse({"message": "Can't Follow Yourself, Stop trying!!!."}, status=201)


def countfollowers(user):
    followercount = Follow.objects.filter(following_user_id = user).count()
    return followercount

def countfollowing(user):
    followingcount = Follow.objects.filter(user_id = user).count()
    return followingcount