from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.viewentry, name="viewentry"),
    path("search/", views.search, name="search"),
    path("createpage/", views.createpage, name="createpage"),
    path("editpage/", views.editpage, name="editpage"),
    path("saveedit/", views.saveedit, name="saveedit"),
]