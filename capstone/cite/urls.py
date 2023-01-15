from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("userauthenicated", views.userauthenicated, name="userauthenicated"),
    path("searchresult", views.searchresult, name="searchresult"),
    path("article/<int:article_id>", views.article, name="article"),
]
