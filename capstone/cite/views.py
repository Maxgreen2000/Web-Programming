import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


from .models import User, Article, Project, Citation

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
    data = json.loads(request.body) 
    searchTitle = data.get("title")
    searchAuthor = data.get("author")
    searchPublisher = data.get("publisher")
    searchYearFrom = data.get("yearfrom")
    if searchYearFrom == "":
        searchYearFrom = -100000000000
    searchYearTo = data.get("yearto")
    if searchYearTo == "":
        searchYearTo = 1000000000000000000
    articles = Article.objects.filter(title__icontains=searchTitle, author__icontains=searchAuthor, publisher__icontains=searchPublisher, year__gte=searchYearFrom, year__lte=searchYearTo )
    articles = articles.order_by("year").all()
    return JsonResponse([article.serialize() for article in articles], safe=False)
    

def article(request, article_id):

    # Query for requested email
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(article.serialize())

    # Article must be done via GET 
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

def myprojects(request):
    return render(request, "cite/myprojects.html")


def loadprojects(request):
    currentUser = request.user
    try:
        projects = Project.objects.filter(user=currentUser)
        projects = projects.order_by("-timestamp").all()
        return JsonResponse([project.serialize() for project in projects], safe=False)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found."}, status=404)

def project(request, project_id):
    # Query for requested email
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(project.serialize())

    # Project must be done via GET 
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

def add_citation(request, article_id, project_id):
    currentUser = request.user
    selectedArticle = Article.objects.get(pk=article_id)
    pagefrom = 1
    pageto = 2
    new_cite = Citation(user=currentUser, article=selectedArticle, pagefrom=pagefrom, pageto=pageto)
    new_cite.save()
    selectedProject = Project.objects.get(pk=project_id) 
    selectedProject.citations.add(new_cite)
    return JsonResponse({"success": "Citation added."}, status=200)

@csrf_exempt
def create_project(request):
    data = json.loads(request.body) 
    title = data.get("title")
    new_project = Project(title=title, user=request.user)
    new_project.save()
    return JsonResponse({"success": "Project added."}, status=200)