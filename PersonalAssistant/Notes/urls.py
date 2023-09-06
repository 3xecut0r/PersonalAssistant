from django.urls import path
from . import views


app_name = "notes"


urlpatterns = [
    path("", views.main, name="index"),
    path(
        "add/", views.NoteView.as_view(), name="add-note"
    ),  # изменил "add-quote" на "add-note" для ясности
    path("edit/<int:pk>", views.NoteUpdateView.as_view(), name="edit"),
    path("remove/<int:pk>", views.NoteRemoveView.as_view(), name="remove"),
    path(
        "search/", views.NoteSearchView.as_view(), name="search-notes"
    ),  # новый путь для поиска
    path(
        "<str:tag>", views.NoteView.as_view(), name="search-tags"
    ),  # этот путь может быть не нужен, так как мы используем POST для поиска
    path("add/", views.TagView.as_view(), name="add-tags"),
]
