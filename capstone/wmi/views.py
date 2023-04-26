import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import User, Manuscript, Email

def index(request):
    return render(request, "wmi/index.html")


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
            return render(request, "wmi/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "wmi/login.html")


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
            return render(request, "wmi/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "wmi/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "wmi/register.html")

def userauthenicated(request):
    currentUser = request.user
    if currentUser.is_authenticated:
        authenticated = {"authenticated":"True"}
        return JsonResponse(authenticated)
    else:
        authenticated = {"authenticated":"False"}
        return JsonResponse(authenticated)

def search(request):
    return render(request, "wmi/searchpage.html")

@csrf_exempt
def searchresult(request):
    data = json.loads(request.body) 
    searchTitle = data.get("title")
    searchLocation = data.get("location")
    searchTags1 = data.get("tags").split(",")
    searchTags2 = data.get("tags").split(" ")
    searchTags = searchTags1 + searchTags2
    searchKeywords1 = data.get("keywords").split(",")
    searchKeywords2 = data.get("keywords").split(" ")
    searchKeywords = searchKeywords1 + searchKeywords2
    searchYearFrom = data.get("yearfrom")
    searchYearTo = data.get("yearto")
    if searchYearFrom == "" and searchYearTo == "":
        manuscripts = Manuscript.objects.filter(title__icontains=searchTitle, location__icontains=searchLocation)
    if searchYearFrom == "" and searchYearTo != "":
        manuscripts = Manuscript.objects.filter(title__icontains=searchTitle, location__icontains=searchLocation, yearto__lte=searchYearTo)
    if searchYearTo == "" and searchYearFrom != "":
        manuscripts = Manuscript.objects.filter(title__icontains=searchTitle, location__icontains=searchLocation, yearfrom__gte=searchYearFrom)
    if searchYearTo != "" and searchYearFrom != "":
        manuscripts = Manuscript.objects.filter(title__icontains=searchTitle, location__icontains=searchLocation, yearfrom__gte=searchYearFrom, yearto__lte=searchYearTo)
    return JsonResponse([manuscript.serialize() for manuscript in manuscripts], safe=False)

def manuscript(request, manuscript_id):
    # Query for requested email
    try:
        manuscript = Manuscript.objects.get(pk=manuscript_id)
    except Manuscript.DoesNotExist:
        return JsonResponse({"error": "Manuscript not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(manuscript.serialize())

    # Manuscript must be done via GET 
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

def mymanuscripts(request):
    currentUser = request.user
    if currentUser.is_authenticated:
        return render(request, "wmi/mymanuscripts.html")
    else:
        return render(request, "wmi/login.html")

def mymanuscriptresults(request):
    manuscripts = Manuscript.objects.filter(poster=request.user)
    return JsonResponse([manuscript.serialize() for manuscript in manuscripts], safe=False)

def loadaddnew(request):
    currentUser = request.user
    if currentUser.is_authenticated:
        return render(request, "wmi/addnewpage.html")
    else:
        return render(request, "wmi/login.html")
    
def addnewmanuscript(request):
    currentUser = request.user
    if request.method == "POST":                     
        title = request.POST["title"]      #Getting all the information from the form
        location = request.POST["location"]
        yearfrom = request.POST["YearFrom"]
        yearto = request.POST["YearTo"]
        tags = request.POST["tags"]
        transcript = request.POST["Transcript"]


        if title != "":

            newManuscript = Manuscript(                              #Adding the information collected to the database
                poster = currentUser,
                title = title,
                location = location,
                yearfrom = yearfrom,
                yearto = yearto,
                tags = tags,
                transcript = transcript,
            )

            newManuscript.save()                                #Saving the database entry and then redirect the user back to the my manuscripts page
            return HttpResponseRedirect(reverse(mymanuscripts))

        else:
            return render(request, "wmi/addnewpage.html")
        
def loadmailbox(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "wmi/inbox.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse(login_view))


def mailbox(request, mailbox):

    # Filter emails returned based on mailbox
    if mailbox == "inbox":
        emails = Email.objects.filter(
            recipient=request.user, archived=False
        )
    elif mailbox == "sent":
        emails = Email.objects.filter(
            sender=request.user
        )
    elif mailbox == "archive":
        emails = Email.objects.filter(
            recipient=request.user, archived=True
        )
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)


def email(request, email_id):
    email = Email.objects.get(id=email_id)
    return JsonResponse(email.serialize())
