from django.urls import path

from . import views

urlpatterns = [
    path("myListings", views.myListings, name="myListings"),
    path("endAuction/<int:id>", views.endAuction, name="endAuction"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("showWatchlist", views.showWatchlist, name="showWatchlist"),
    path("addToWatchlist/<int:id>", views.addToWatchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<int:id>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("selectedCategory", views.selectedCategory, name="selectedCategory"),
    path("createListing", views.createListing, name="createListing"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
