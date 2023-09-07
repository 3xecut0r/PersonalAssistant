from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

from django.http import HttpResponse


# def fake_login(request):
#     return HttpResponse("Fake login page. No actual login functionality.")


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
    # path(
    #     "tag/<str:tag>", views.NoteSearchView.as_view(), name="search-tags"
    # ),  # этот путь может быть не нужен, так как мы используем POST для поиска
    path("add-tag/", views.TagView.as_view(), name="add-tags"),
]
