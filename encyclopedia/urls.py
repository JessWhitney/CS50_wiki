from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="wiki"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("search", views.search, name="search"),
    # TODO: Edit page; random page
]
