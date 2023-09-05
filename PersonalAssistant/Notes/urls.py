from django.urls import path
from . import views


app_name = "notes"


urlpatterns = [
    path("", views.main, name="main"),
    path(
        "notes/add/", views.NoteView.as_view(), name="add-note"
    ),  # изменил "add-quote" на "add-note" для ясности
    path("notes/edit/<int:pk>", views.NoteUpdateView.as_view(), name="edit"),
    path("notes/remove/<int:pk>", views.NoteRemoveView.as_view(), name="remove"),
    path(
        "notes/search/", views.NoteSearchView.as_view(), name="search-notes"
    ),  # новый путь для поиска
    path(
        "tags/<str:tag>", views.NoteView.as_view(), name="search-tags"
    ),  # этот путь может быть не нужен, так как мы используем POST для поиска
    path("tags/add/", views.TagView.as_view(), name="add-tags"),
]
