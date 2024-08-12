from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry_page, name="wiki"),
    path("new_entry/", views.new_entry, name="new_entry"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    path("random", views.random_page, name="random_page")
]
