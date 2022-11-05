
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API ROUTES
    path("new_posts", views.new_post, name="new_post"),
    path("loadposts/<int:id>/<str:page>", views.loadposts, name="loadposts"),
    path("loadprofile/<int:id>", views.loadprofiles, name="loadprofiles"),

]
