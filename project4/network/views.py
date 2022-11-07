import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse


from .models import User, Post, Profile, Follow


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


def view_profile(request, username):

    currentUser = request.user
    selectedUser = User.objects.get(username = username)
    UserID = selectedUser.id
    selectedProfile = Profile.objects.get(profile_owner = selectedUser)
    if userAisfollowinguserB(currentUser, selectedUser) == False:
        follow_button = "Follow"
    elif currentUser == selectedUser:
        follow_button = "currentuser"
    else:
        follow_button = "Unfollow"
    


    return render(request, "network/profile.html", {
        "message": username,
        "UserID": UserID,
        "profileData": selectedProfile,
        "follow_unfollow": follow_button
    })


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

def loadposts(request, id, page):

    # Filter emails returned based on page
    if page == "allposts" and id == 0:
        posts = Post.objects.all()
    elif page == "profile" and id == 0:
        posts = Post.objects.filter(poster = request.user)
    elif page == "profile":
        user = User.objects.get(id=id)
        posts = Post.objects.filter(poster = user)  
    #elif page == "archive":
        #emails = Email.objects.filter(
            #user=request.user, recipients=request.user, archived=True
        #)
    else:
        return JsonResponse({"error": "Invalid page."}, status=400)

    # Return emails in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def userAisfollowinguserB(userA, userB):
    if Follow.objects.filter(user_id = userA, following_user_id = userB ).exists():
        return True
    else:
        return False

def addFollow(request, userid):
    currentUser = request.user
    selectedUser = User.objects.get(pk = userid)
    if currentUser != selectedUser:
        if userAisfollowinguserB(currentUser, selectedUser) == False:
            selectedfollow = Follow.objects.create(user_id = currentUser, following_user_id = selectedUser)
            selectedfollow.save()
        else:
            selectedfollow = Follow.objects.get(user_id = currentUser, following_user_id = selectedUser)
            selectedfollow.delete()

    return JsonResponse({"message": "follow successful."}, status=201)



