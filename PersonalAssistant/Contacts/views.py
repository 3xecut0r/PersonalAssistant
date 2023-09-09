from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.shortcuts import render, HttpResponse
from datetime import date, timedelta
from .models import Contact
from .forms import ContactDeleteForm

import json
import requests
from ipware import get_client_ip


def start_page(request):
    context = {}
    return render(request, 'Contacts/index.html', context)


# def start_page(request):
#     # weatherbit.io
#     api_key = "e0968fa8d191445689837cc732013dd4"
#     client_ip, is_routable = get_client_ip(request)
#     if client_ip:
#         request_url = f'https://geolocation-db.com/jsonp/{client_ip}'
#         response = requests.get(request_url)
#         result = response.content.decode()
#         result = result.split("(")[1].strip(")")
#         result = json.loads(result)
#         if response:
#             latitude = result.get('latitude')
#             longitude = result.get('longitude')
#             url = f'https://api.weatherbit.io/v2.0/current?lat={latitude}&lon={longitude}&key={api_key}'
#             try:
#                 data = requests.get(url).json()
#                 city_name = data['data'][0]['city_name']
#                 country_code = data['data'][0]['country_code']
#                 wind_spd = data['data'][0]['wind_spd']
#                 app_temp = data['data'][0]['app_temp']
#                 aqi = data['data'][0]['aqi']
#                 temp = data['data'][0]['temp']
#
#                 context = {'city': city_name, 'country': country_code, 'wind_spd': wind_spd, 'app_temp': app_temp,
#                            'aqi': aqi, 'temp': temp}
#             except Exception as e:
#                 return HttpResponse({'status': str(e)})
#             return render(request, 'Contacts/index.html', context)
#         else:
#             pass
#     else:
#         pass
#     return render(request, 'Contacts/index.html')

  
def card_subtitle_view(request):
    return render(request, 'Contacts/card_subtitle.html')



@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            res = Contact.objects.get(email=email)
            res.user_id = request.user.id
            res.save()
            return redirect('contacts:contact_list')  # Перенаправление на страницу со списком контактов
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})


#поиск контактов среди контактов книги
@login_required
def contact_search(request):
    query = request.GET.get('q')  # Получение поискового запроса из URL

    if query:
        # Если есть поисковый запрос, выполните поиск в модели Contact
        results = Contact.objects.filter(name__icontains=query, user_id=request.user.id)
    else:
        results = []

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'contacts/contact_search.html', context)


# редактирование контактов

@login_required
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contacts:contact_list')  # Перенаправление на страницу со списком контактов
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/edit_contact.html', {'form': form})

@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        form = ContactDeleteForm(request.POST)
        if form.is_valid():
            contact.delete()
            return redirect('contacts:contact_list')  # Перенаправление на страницу со списком контактов
    else:
        form = ContactDeleteForm()

    return render(request, 'contacts/delete_contact.html', {'contact': contact, 'form': form})


# список всех контактов из базы данных
# def contact_list(request):
    
#     contacts = Contact.objects.all()

#     context = {
#         'contacts': contacts,
#     }

#     return render(request, 'contacts/contact_list.html', context)


@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user_id=request.user.id)
    for contact in contacts:
        contact.days_until_birthday = days_until_birthday(contact.birthday)

    context = {
        'contacts': contacts,
    }

    return render(request, 'contacts/contact_list.html', context)





def days_until_birthday(birthday):
    today = date.today()
    next_birthday = birthday.replace(year=today.year)
    if today > next_birthday:
        next_birthday = next_birthday.replace(year=today.year + 1)
    days_left = (next_birthday - today).days
    return days_left

