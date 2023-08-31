from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_contact, name='add_contact'),
    # Другие URL-маршруты, например, для списка контактов
]