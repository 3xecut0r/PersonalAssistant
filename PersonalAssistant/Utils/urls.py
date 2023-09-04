from django.urls import path
from . import views


urlpatterns = [
    path('weather/', views.weather_forcast, name="get_weather")
]