from django.shortcuts import render, HttpResponse
import json

import requests
from ipware import get_client_ip


# def start_page(request):
#     context = {}
#     return render(request, 'Contacts/base.html', context)


def start_page(request):
    # weatherbit.io
    api_key = "e0968fa8d191445689837cc732013dd4"
    client_ip, is_routable = get_client_ip(request)
    if client_ip:
        request_url = f'https://geolocation-db.com/jsonp/{client_ip}'
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result = json.loads(result)
        if response:
            latitude = result.get('latitude')
            longitude = result.get('longitude')
            url = f'https://api.weatherbit.io/v2.0/current?lat={latitude}&lon={longitude}&key={api_key}'
            try:
                data = requests.get(url).json()
                city_name = data['data'][0]['city_name']
                country_code = data['data'][0]['country_code']
                wind_spd = data['data'][0]['wind_spd']
                app_temp = data['data'][0]['app_temp']
                aqi = data['data'][0]['aqi']
                temp = data['data'][0]['temp']

                context = {'city': city_name, 'country': country_code, 'wind_spd': wind_spd, 'app_temp': app_temp,
                           'aqi': aqi, 'temp': temp}
            except Exception as e:
                return HttpResponse({'status': str(e)})
            return render(request, 'Contacts/index.html', context)
        else:
            pass
    else:
        pass
    return render(request, 'Contacts/index.html')