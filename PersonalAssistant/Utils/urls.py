from django.urls import path
from . import views


app_name = 'utils'

urlpatterns = [
    path('upload_files/', views.upload_files, name="upload"),
    path('images/', views.show_user_images, name="show_images"),
    path('documents/', views.show_user_documents, name="show_documents"),
    path('unknown/', views.show_user_unknown, name="show_unknown"),
    path('download/<int:file_id>', views.download_user_file, name="download"),
    path('delete/<int:file_id>', views.remove_user_file, name="delete"),
    path('authorize/', views.dropbox_oauth, name='dropbox_oauth'),
    path('authorized/', views.dropbox_authorized, name='dropbox_authorized'),
    path('weather/', views.weather_forcast, name="get_weather"),
    path('utils_main_page/', views.main_page, name='main_page')
]

