import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import User, Manuscript, Email, Conversation

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
    searchTitle = request.POST["inputTitle"]
    searchLocation = request.POST["inputLocation"]
    searchTags1 = request.POST["inputTags"].split(",")
    searchTags2 = request.POST["inputTags"].split(" ")
    searchTags = searchTags1 + searchTags2
    searchKeywords1 = request.POST["inputKeywords"].split(",")
    searchKeywords2 = request.POST["inputKeywords"].split(" ")
    searchKeywords = searchKeywords1 + searchKeywords2
    searchYearFrom = request.POST["inputYearFrom"]
    searchYearTo = request.POST["inputYearTo"]
    if searchYearFrom == "" and searchYearTo == "":
        manuscripts = Manuscript.objects.filter(title__icontains=searchTitle, location__icontains=searchLocation)
    if searchYearFrom == "" and searchYearTo != "":
        manuscripts = Manuscript.objects.filter(title__icontains=searchTitle, location__icontains=searchLocation, yearto__lte=searchYearTo)
    if searchYearTo == "" and searchYearFrom != "":
        manuscripts = Manuscript.objects.filter(title__icontains=searchTitle, location__icontains=searchLocation, yearfrom__gte=searchYearFrom)
    if searchYearTo != "" and searchYearFrom != "":
        manuscripts = Manuscript.objects.filter(title__icontains=searchTitle, location__icontains=searchLocation, yearfrom__gte=searchYearFrom, yearto__lte=searchYearTo)
    return render(request, "wmi/results.html", {
        "results": manuscripts
    })


def manuscript(request, manuscript_id):
    manuscript = Manuscript.objects.get(pk=manuscript_id)
    return render(request, "wmi/singlemanuscript.html", {
        "manuscript": manuscript
    })
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

@csrf_exempt
def createnewmessage(request, manuscript_id):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    recipient = data.get("recipient", "")
    body = data.get("body", "")

    # Check recipient emails
    if recipient == [""]:
        return JsonResponse({
            "error": "recipient required."
        }, status=400)

    if body == [""]:
        return JsonResponse({
            "error": "body of text required."
        }, status=400)
    
    recipient = User.objects.get(id=recipient)
    # Create email
    email = Email(
        sender=request.user,
        recipient=recipient,
        body=body,
    )
    email.save()

    #NOW ADD NEW EMAIL TO THE CONVERSATION
    poster = User.objects.get(id=request.user.id)
    manuscript = Manuscript.objects.get(id=manuscript_id)
    conversation = Conversation.objects.get( participants = request.user and poster, manuscript = manuscript )
    conversation.emails.add(email)


    return JsonResponse({"message": "mail sent successfully."}, status=201)


def conversations(request):
    conversations = Conversation.objects.filter( participants=request.user ) 
    conversations = conversations.order_by("-timestamp").all()
    return JsonResponse([conversation.serialize() for conversation in conversations], safe=False)


def load_conversation_messages(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)
    emails = conversation.emails.all()
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)

def find_conversation(request, manuscript_id, poster_id):
    poster = User.objects.get(id=poster_id)
    manuscript = Manuscript.objects.get(id=manuscript_id)
    try:
        conversation = Conversation.objects.get( participants = request.user and poster, manuscript = manuscript )
    except:
        conversation = Conversation(
            manuscript = manuscript
        )
        conversation.save()
        conversation.participants.add(request.user)
        conversation.participants.add(poster)
    return JsonResponse(conversation.serialize())