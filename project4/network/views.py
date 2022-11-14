import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator


from .models import User, Post, Profile, Follow, Like


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


def view_profile(request, username):
    currentUser = request.user
    selectedUser = User.objects.get(username = username)
    UserID = selectedUser.id
    selectedProfile = Profile.objects.get(profile_owner = selectedUser)
    followercount = countfollowers(selectedUser)   
    followingcount = countfollowing(selectedUser)
    if currentUser.is_authenticated:
        if currentUser == selectedUser:
            follow_button = "currentuser"
        elif userAisfollowinguserB(currentUser, selectedUser) == False:
            follow_button = "Follow"
        else:
            follow_button = "Unfollow"

        return render(request, "network/profile.html", {
            "message": username,
            "UserID": UserID,
            "profileData": selectedProfile,
            "follow_unfollow": follow_button,
            "followercount": followercount,
            "followingcount": followingcount
        })
    else:
        return render(request, "network/profile.html", {
            "message": username,
            "UserID": UserID,
            "profileData": selectedProfile,
            "followercount": followercount,
            "followingcount": followingcount
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
    elif page == "following" and id == 0: 
        current_user = request.user
        allFollowing = Follow.objects.filter(user_id = current_user).values_list('following_user_id')
        posts = Post.objects.filter(poster__in=allFollowing)
    else:
        return JsonResponse({"error": "Invalid page."}, status=400)

    # Return emails in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def myFollowing(request):
    return render(request, "network/following.html") 

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


def editpost(request, postid):
    #####ADD EDITPOST FUNCTION HERE

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    body = data.get("body", "")

    posttoedit = Post.objects.get(pk=postid)
    posttoedit.body = body
    posttoedit.save()

    return JsonResponse({"message": "Edit successful."}, status=201)


def countfollowers(user):
    followercount = Follow.objects.filter(following_user_id = user).count()
    return followercount

def countfollowing(user):
    followingcount = Follow.objects.filter(user_id = user).count()
    return followingcount

def postisliked(currentUser, selectedPost):
    if Like.objects.filter(liker = currentUser, liked_Post = selectedPost ).exists():
        return True
    else:
        return False


def determinebutton(request, postid):
    currentUser = request.user
    selectedPost = Post.objects.get(pk = postid)
    if postisliked(currentUser, selectedPost) == False:
        buttontext = {"text":"Like"}
        return JsonResponse(buttontext)
    else:
        buttontext = {"text":"Unlike"}
        return JsonResponse(buttontext)


def likepost(request, postid):
    currentUser = request.user
    selectedPost = Post.objects.get(pk = postid)
    if postisliked(currentUser, selectedPost) == False:
        selectedLike = Like.objects.create(liker = currentUser, liked_Post = selectedPost)
        selectedLike.save()
        ##ADD A LIKE TO THE LIKE COUNTER FOR A CERTAIN POST
        selectedPost.likes = selectedPost.likes + 1
        selectedPost.save()
        return JsonResponse({"message": "Like successful."}, status=201)
    else:
        selectedLike = Like.objects.get(liker = currentUser, liked_Post = selectedPost)
        selectedLike.delete()
        selectedPost.likes = selectedPost.likes - 1                   #HAVE TO REFERESH THE PAGE TO GET HE LIKES TO UPDATE NOT GOOD!!!!!!!!!!!!!!
        selectedPost.save()
        return JsonResponse({"message": "Unlike successful."}, status=201)


