from django.urls import path
from .views import start_page
from . import views
from .views import add_contact
from .views import contact_search
from .views import edit_contact
from .views import delete_contact


urlpatterns = [
    path('base/', start_page, name="start_page"), 
    path('card_subtitle/', views.card_subtitle_view, name='card_subtitle'), 
    path('add_contact/', add_contact, name='add_contact'),
    path('contact_search/', contact_search, name='contact_search'),
    path('edit_contact/<int:contact_id>/', edit_contact, name='edit_contact'),
    path('delete_contact/<int:contact_id>/', delete_contact, name='delete_contact'),
]

