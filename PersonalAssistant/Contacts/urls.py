from django.urls import path

from .views import start_page
from . import views
from .views import add_contact
from .views import contact_search
from .views import edit_contact
from .views import delete_contact
from .views import contact_list


app_name = 'contacts'

urlpatterns = [
    path('base/', start_page, name="start_page"),
    path('add_contact/', add_contact, name='add_contact'),
    path('contact_search/', contact_search, name='contact_search'),
    path('edit_contact/<int:contact_id>/', edit_contact, name='edit_contact'),
    path('delete_contact/<int:contact_id>/', delete_contact, name='delete_contact'),
    path('contacts/', contact_list, name='contact_list'),
    path('contact_search/', views.contact_search, name='contact_search'),
    path('feedback/', views.send_feedback, name='send_feedback'),
    path('feedback/success/', views.feedback_success, name='feedback_success'),
]
