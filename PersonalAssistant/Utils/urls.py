from django.urls import path
from . import views

app_name = 'utils'

urlpatterns = [
    path('upload_files/', views.upload_files, name="upload_files"),
    path('images/', views.show_user_images, name="show_images"),
    path('documents/', views.show_user_documents, name="show_documents"),
    path('unknown/', views.show_user_unknown, name="show_unknown")
]

