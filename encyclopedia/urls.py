from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("wiki", views.search, name="search"),
    path("create", views.create, name="create"),
    path("randompage", views.randompage, name="randompage"),
    path("edit", views.edit, name="edit")
]
