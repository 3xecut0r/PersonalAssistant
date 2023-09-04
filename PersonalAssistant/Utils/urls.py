from django.urls import path
from . import views


urlpatterns = [
    path('upload_files/', views.upload_files, name="upload_files")
]