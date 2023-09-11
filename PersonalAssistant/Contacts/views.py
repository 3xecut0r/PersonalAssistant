from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import ContactForm
from datetime import date, timedelta
from .models import Contact
from .forms import ContactDeleteForm
from django.core.cache import cache


import os
import json
import requests
from ipware import get_client_ip
from dotenv import load_dotenv

load_dotenv()

# @login_required
# def start_page(request):
#     context = {}
#     return render(request, 'Contacts/index.html', context)


def set_userdata(request, data):
    key = f"user{request.user.id}_data"
    cache.set(key, data)


def get_userdata(request):
    key = f"user{request.user.id}_data"
    return cache.get(key)


@login_required
def start_page(request):
    cache_key = f"user_weather_data:{request.user.id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        data = json.loads(cached_data)
        city_name = data['data'][0]['city_name']
        country_code = data['data'][0]['country_code']
        wind_spd = data['data'][0]['wind_spd']
        app_temp = data['data'][0]['app_temp']
        aqi = data['data'][0]['aqi']
        temp = data['data'][0]['temp']
        context = {'city': city_name, 'country': country_code, 'wind_spd': wind_spd, 'app_temp': app_temp,
                   'aqi': aqi, 'temp': temp}
        return render(request, 'Contacts/index.html', context)
    else:
        try:
            # weatherbit.io
            api_key = os.environ.get('API_WEATHER')
            client_ip, is_routable = get_client_ip(request)
            api = os.environ.get('API_IPSTACK')
            if client_ip:
                request_url = f'http://api.ipstack.com/{client_ip}?access_key={api}'
                response = requests.get(request_url)
                result = response.content.decode()
                result = json.loads(result)
                if response:
                    latitude = result.get('latitude')
                    longitude = result.get('longitude')
                    url = f'https://api.weatherbit.io/v2.0/current?lat={latitude}&lon={longitude}&key={api_key}'
                    try:
                        data = requests.get(url).json()
                        city_name = result.get('city')
                        country_code = data['data'][0]['country_code']
                        wind_spd = data['data'][0]['wind_spd']
                        app_temp = data['data'][0]['app_temp']
                        aqi = data['data'][0]['aqi']
                        temp = data['data'][0]['temp']
                        cache.set(cache_key, json.dumps(data), timeout=3600)
                        context = {'city': city_name, 'country': country_code, 'wind_spd': wind_spd, 'app_temp': app_temp,
                                   'aqi': aqi, 'temp': temp}
                    except Exception as e:
                        return HttpResponse({'status': str(e)})
                    return render(request, 'Contacts/index.html', context)
        except Exception as e:
            return HttpResponse({'status': str(e)})
    return render(request, 'Contacts/index.html')


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contacts:contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})


@login_required
def contact_search(request):
    query = request.GET.get('q')

    if query:
        results = Contact.objects.filter(name__icontains=query, user_id=request.user.id)
    else:
        results = []

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'contacts/contact_search.html', context)


@login_required
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contacts:contact_list')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/edit_contact.html', {'form': form})


@login_required
def delete_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    contact.delete()
    return redirect('contacts:contact_list')


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



