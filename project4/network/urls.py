
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("view_profile/<str:profile_owner>", views.view_profile, name="view_profile"),
    path("following", views.showfollowing, name="following"),

    #API PATHS
    path("new_posts", views.new_post, name="new_post"),
    path("createFollows", views.createFollow, name="createFollow"),
]
