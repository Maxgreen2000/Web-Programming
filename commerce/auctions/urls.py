from django.urls import path

from . import views

urlpatterns = [
    path("listing/<int:id>", views.listing, name="listing"),
    path("selectedCategory", views.selectedCategory, name="selectedCategory"),
    path("createListing", views.createListing, name="createListing"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
