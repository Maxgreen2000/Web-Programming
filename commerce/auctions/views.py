from ast import Index, Return
import re
from turtle import title
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings": activeListings,
        "categories": allCategories
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
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/createListing.html", {
            "categories": allCategories
        })
    else:
        currentUser = request.user                            #Getting all the information from the form
        title = request.POST["title"] 
        description = request.POST["description"]
        imageUrl = request.POST["imageUrl"]
        price = request.POST["price"]
        category = request.POST["category"]

        categoryData = Category.objects.get(categoryName=category)    ##This retrieves the specific category selected by matches the option selected witht he categoryName using the get function.

        bid = Bid(bid=float(price), user=currentUser)   #CREATE AND SAVE THE BID 
        bid.save()

        newListing = Listing(                              #Adding the information collected to the database
            owner = currentUser,
            title = title,
            description = description,
            imageUrl = imageUrl,
            price = bid,
            category = categoryData 
        )

        newListing.save()                                #Saving the database entry and then redirect the user back to the index page
        id = newListing.id
        addToWatchlist(request, id)
        return HttpResponseRedirect(reverse(index))


def selectedCategory(request):
    if request.method == "POST":
        postedCategory = request.POST['category']
        chosenCategory = Category.objects.get(categoryName = postedCategory)
        activeListings = Listing.objects.filter(isActive=True, category=chosenCategory )
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings": activeListings,
            "categories": allCategories
        })

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner
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
    allListings = currentUser.listingWatchlist.all()
    return render(request,  "auctions/watchlist.html",{
        "listings": allListings
    })

def addComment(request, id):                                                   #CHANGE SO COMMENTS CANNOT BE EMPTY
    currentUser = request.user
    listingData = Listing.objects.get(pk=id) 
    message = request.POST['newComment']

    newComment = Comment(
        author = currentUser,
        listing = listingData,
        message = message
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addBid(request, id):
    addToWatchlist(request, id)                                             #WHEN A USER BIDS THE ITEM, WHETHER THEY ARE SUCCESSFUL OR NOT, THEY HAVE BID ON AUTOMATICALLY GETS PUT IN THEIR WATCHLIST
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html",{
            "listing": listingData,
            "message": "Congratulations, your bid was successful. Item has been added to your watchlist",
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
            "update": True
         })
    else:
        return render(request,  "auctions/listing.html",{
            "listing": listingData,
            "message": "Your bid was unsuccessful, please bid higher. Item has been added to your watchlist",
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
            "update": False
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