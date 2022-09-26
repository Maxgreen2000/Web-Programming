from django.urls import path

from . import views

urlpatterns = [
    path("rand/", views.rand, name="rand"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("edit/", views.edit, name="edit"),
    path("new/", views.new_page, name="new_page"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("", views.index, name="index")
]
