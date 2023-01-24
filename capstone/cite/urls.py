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
    path("myprojects", views.myprojects, name="myprojects"),
    path("loadprojects", views.loadprojects, name="loadprojects"),
    path("project/<int:project_id>", views.project, name="project"),
    path("add_citation/<int:article_id>/<int:project_id>", views.add_citation, name="add_citation"),
    path("create_project", views.create_project, name="create_project"),
    path("citations/<int:project_id>", views.load_citations, name="load_citations"),
    path("delete_project/<int:project_id>", views.delete_project, name="delete_project"),
]
