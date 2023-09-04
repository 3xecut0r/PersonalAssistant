from django.urls import path
from .views import start_page

app_name = 'contacts'

urlpatterns = [
    path('base/', start_page, name="start_page"),
]
