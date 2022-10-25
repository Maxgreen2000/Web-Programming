from ast import Delete
import json
import profile
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from .models import User, Post, Follow, Profile


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
            follow = Follow(
                user = user
            )
            follow.save()
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
    selected_follow = Follow.objects.get(user = selected_user)
    follower_profiles = selected_follow.followers.all()
    if current_user in follower_profiles:
        follow_unfollow  = "unfollow"
    else:
        follow_unfollow  = "follow"
    return render(request, "network/profile.html", {
        "name": name,
        "image": image,
        "follow_unfollow": follow_unfollow,
        "username": selected_user.username

    })


def add_follow(request):
    current_user = request.user
    data = json.loads(request.body)
    profile_name = data.get("profile_name")
    selected_user = User.objects.get(username = profile_name)
    selected_follow = Follow.objects.get(user = selected_user)
    follower_profiles = selected_follow.followers.all()
    current_user_following = Follow.objects.get(user = current_user)
    if current_user in follower_profiles:
        selected_follow.followers.delete(current_user)
        current_user_following.following.delete(selected_user)
        selected_follow.save()
        current_user_following.save()

    else:
        selected_follow.followers.add(current_user)
        current_user_following.following.add(selected_user)
        selected_follow.save()
        current_user_following.save()

    return JsonResponse({"message": "Post successful."}, status=201)


