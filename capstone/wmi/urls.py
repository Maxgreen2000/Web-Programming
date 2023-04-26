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
    path("manuscript/<int:manuscript_id>", views.manuscript, name="manuscript"),
    path("searchresult", views.searchresult, name="searchresult"),
    path("mymanuscripts", views.mymanuscripts, name="mymanuscripts"),
    path("mymanuscriptresults", views.mymanuscriptresults, name="mymanuscriptresults"),
    path("loadaddnew", views.loadaddnew, name="loadaddnew"),
    path("addnewmanuscript", views.addnewmanuscript, name="addnewmanuscript"),
    path("loadmailbox", views.loadmailbox, name="loadmailbox"),
    path("emails/<str:mailbox>", views.mailbox, name="mailbox"),
    path("email/<int:email_id>", views.email, name="email"),
]