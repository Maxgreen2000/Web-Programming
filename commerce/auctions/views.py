from ast import Index, Return
import re
from turtle import title
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    counter = activeListings.count()
    currentUser = request.user
    allCategories = Category.objects.all()
    if currentUser.is_authenticated:
        watchlist = currentUser.listingWatchlist.all()
        watchlistCounter = watchlist.count()
        return render(request, "auctions/index.html",{
            "listings": activeListings,
            "categories": allCategories,
            "chosenCategory": "Active Listings",
            "counter": counter,
            "user":currentUser,
            "watchlistCounter": watchlistCounter
        })
    else:
        return render(request, "auctions/index.html",{
            "listings": activeListings,
            "categories": allCategories,
            "chosenCategory": "Active Listings",
            "counter": counter,

    })
    


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createListing(request):
    currentUser = request.user
    if request.method == "GET":
        allCategories = Category.objects.all()
        watchlist = currentUser.listingWatchlist.all()
        watchlistCounter = watchlist.count()        
        return render(request, "auctions/createListing.html", {
            "categories": allCategories,
            "watchlistCounter": watchlistCounter
        })
    else:                       
        title = request.POST["title"]      #Getting all the information from the form
        description = request.POST["description"]
        imageUrl = request.POST["imageUrl"]
        startingPrice = request.POST["startingPrice"]
        category = request.POST["category"]

        if (title and description and imageUrl and startingPrice and category) != "":

            categoryData = Category.objects.get(categoryName=category)    ##This retrieves the specific category selected by matches the option selected witht he categoryName using the get function.


            newListing = Listing(                              #Adding the information collected to the database
                owner = currentUser,
                title = title,
                description = description,
                imageUrl = imageUrl,
                startingPrice = startingPrice,
                highestBid = startingPrice,
                highestBidder = currentUser,
                category = categoryData 
            )

            newListing.save()                                #Saving the database entry and then redirect the user back to the index page
            id = newListing.id
            addToWatchlist(request, id)                      #Before being redirected the new listing is added to the current users watchlist.
            return HttpResponseRedirect(reverse(index))

        else:
            allCategories = Category.objects.all()
            return render(request, "auctions/createListing.html", {
            "categories": allCategories,
            "emptyField": True,
            "message": "Make sure all fields are filled in before submitting"      
        })


def selectedCategory(request):
    if request.method == "POST":
        postedCategory = request.POST['category']                 
        if postedCategory == "Active Listings":
                return HttpResponseRedirect(reverse("index"))
        else:            
            allCategories = Category.objects.all()
            currentUser = request.user
            chosenCategory = Category.objects.get(categoryName = postedCategory)
            activeListings = Listing.objects.filter(isActive=True, category=chosenCategory )
            counter = activeListings.count()
            if currentUser.is_authenticated:
                watchlist = currentUser.listingWatchlist.all()
                watchlistCounter = watchlist.count()   
                return render(request, "auctions/index.html",{
                    "listings": activeListings,
                    "categories": allCategories,
                    "chosenCategory": chosenCategory,
                    "counter": counter,
                    "watchlistCounter": watchlistCounter
                })
            else:
                return render(request, "auctions/index.html",{
                    "listings": activeListings,
                    "categories": allCategories,
                    "chosenCategory": chosenCategory,
                    "counter": counter,
                })


def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    currentUser = request.user
    if currentUser.is_authenticated:
        isListingInWatchlist = request.user in listingData.watchlist.all()
        watchlist = currentUser.listingWatchlist.all()
        watchlistCounter = watchlist.count()   
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
            "watchlistCounter": watchlistCounter,
            "currentUser": currentUser,
            "message": "Congratulations, you are the highest bidder",
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "allComments": allComments,
            "isOwner": isOwner,
        })



def removeFromWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    

def addToWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def showWatchlist(request):
    currentUser = request.user
    watchlist = currentUser.listingWatchlist.all()
    watchlistCounter = watchlist.count()
    if request.method == "POST":
        statusBool = request.POST['status']
        if statusBool == "Active":
            allListings = currentUser.listingWatchlist.filter(isActive = True)
        elif statusBool == "Ended":
            allListings = currentUser.listingWatchlist.filter(isActive = False)
        else:
            allListings = currentUser.listingWatchlist.all()
        
        return render(request,  "auctions/watchlist.html",{
             "listings": allListings,
             "watchlistCounter": watchlistCounter,
             "status": statusBool
        })

    else:    
        allListings = currentUser.listingWatchlist.all()
        return render(request,  "auctions/watchlist.html",{
            "listings": allListings,
            "watchlistCounter": watchlistCounter,
            "status": "All"
        })

def addComment(request, id):                                                   #CHANGE SO COMMENTS CANNOT BE EMPTY
    currentUser = request.user
    listingData = Listing.objects.get(pk=id) 
    message = request.POST['newComment']
    if message != "":
        newComment = Comment(
            author = currentUser,
            listing = listingData,
            message = message
        )
        newComment.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    else:
        return HttpResponseRedirect(reverse("listing", args=(id, )))


def addBid(request, id):
    addToWatchlist(request, id)
    currentUser = request.user                                          #WHEN A USER BIDS THE ITEM, WHETHER THEY ARE SUCCESSFUL OR NOT, THEY HAVE BID ON AUTOMATICALLY GETS PUT IN THEIR WATCHLIST
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    if int(newBid) > listingData.highestBid:
        listingData.highestBid = newBid
        listingData.highestBidder = currentUser
        listingData.bidCounter = listingData.bidCounter + 1
        listingData.save()
        return render(request, "auctions/listing.html",{
            "listing": listingData,
            "message": "Congratulations, you are the highest bidder",
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
            "currentUser": currentUser
         })
    elif int(newBid) <= listingData.highestBid and currentUser ==  listingData.highestBidder:
        return render(request, "auctions/listing.html",{
            "listing": listingData,
            "message": "Congratulations, you are the highest bidder",
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
            "currentUser": currentUser
         })
    else:
        return render(request,  "auctions/listing.html",{
            "listing": listingData,
            "message": "Your bid was unsuccessful, please bid higher. Item has been added to your watchlist",
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
            "currentUser": currentUser
         })


def endAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)

    return render(request,  "auctions/listing.html",{
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "You have ended the auction"
     })


def myListings(request):
    currentUser = request.user
    watchlist = currentUser.listingWatchlist.all()
    watchlistCounter = watchlist.count()  
    if request.method == "POST":
        statusBool = request.POST['status']
        if statusBool == "Active":
            allListings = Listing.objects.filter(owner = currentUser, isActive = True)
        elif statusBool == "Ended":
            allListings = Listing.objects.filter(owner = currentUser, isActive = False)
        else:
            allListings = Listing.objects.filter(owner = currentUser)
        return render(request,  "auctions/myListings.html",{
            "listings": allListings,
            "watchlistCounter": watchlistCounter,
            "status": statusBool
    })
    else:  
        allListings = Listing.objects.filter(owner = currentUser)
        return render(request,  "auctions/myListings.html",{
            "listings": allListings,
            "watchlistCounter": watchlistCounter,
            "status": "All"
        })