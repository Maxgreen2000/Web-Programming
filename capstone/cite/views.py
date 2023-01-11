import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


from .models import User, Article

def index(request):
    return render(request, "cite/index.html")


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
            return render(request, "cite/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cite/login.html")


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
            return render(request, "cite/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cite/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cite/register.html")

def userauthenicated(request):
    currentUser = request.user
    if currentUser.is_authenticated:
        authenticated = {"authenticated":"True"}
        return JsonResponse(authenticated)
    else:
        authenticated = {"authenticated":"False"}
        return JsonResponse(authenticated)

def search(request):
    return render(request, "cite/searchpage.html")

@csrf_exempt
def searchresult(request):
    articles = Article.objects.all()
    articles = articles.order_by("year").all()
    return JsonResponse([article.serialize() for article in articles], safe=False)
    

