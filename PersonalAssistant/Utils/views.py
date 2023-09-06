from django.shortcuts import render, HttpResponse
import json
from datetime import datetime

import requests
from ipware import get_client_ip


def get_day_of_week(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    return date_obj.strftime('%A')


def weather_forcast(request):
    api_key = "e0968fa8d191445689837cc732013dd4"
    client_ip, is_routable = get_client_ip(request)
    if client_ip:
        request_url = f'https://geolocation-db.com/jsonp/{client_ip}'
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result = json.loads(result)
        if response:
            city = result.get('city')
            url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={city}&key={api_key}'
            try:
                data = requests.get(url).json()
                weather_data = data['data']


                for entry in weather_data:
                    entry['day_of_week'] = get_day_of_week(entry['valid_date'])

                context = {'city': city, 'weather_data': weather_data}
            except Exception as e:
                return HttpResponse({'status': str(e)})
            return render(request, 'Utils/weather.html', context=context)
        else:
            pass
    else:
        pass
    return render(request, 'Utils/weather.html')


