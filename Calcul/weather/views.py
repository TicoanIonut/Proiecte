import datetime

import requests
from django.shortcuts import render

from api_secrets import WEATHER_API


def weather_index(request):
	API_KEY = WEATHER_API
	current_weather_url = "api.openweathermap.org/data/2.5/weather?q={}&appid={}"
	forecast_url = "api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
	if request.method == 'POST':
		city1 = request.POST['city1']
		city2 = request.POST.get('city2', None)
		weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)
		if city2:
			weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url,
			                                                             forecast_url)
		else:
			weather_data2, daily_forecasts2 = None, None
		context = {
			"weather_data1": weather_data1,
			"daily_forecasts1": daily_forecasts1,
			"weather_data2": weather_data2,
			"daily_forecasts2": daily_forecasts2
		}
		return render(request, "index.html", context)
	else:
		return render(request, "index.html")


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
	response = requests.get(current_weather_url.format(city, api_key)).json()
	lat, long = response['coord']['lat'], response['coord']['long']
	forecast_response = requests.get(forecast_url.format(lat, long, api_key)).json()
	weather_data = {
		"city": city,
		"temperature": round(response['main']['temp'] - 273.15, 2),
		"description": response['weather'][0]['description'],
		"icon": response['weather'][0]['icon']
	}
	daily_forecasts = []
	for daily_data in forecast_response['daily'][:5]:
		daily_forecasts.append({
			"day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
			"min_temp": round(response['main']['min'] - 273.15, 2),
			"max_temp": round(response['main']['max'] - 273.15, 2),
			"description": daily_data['weather'][0]['description'],
			"icon": daily_data['weather'][0]['description']
		})
	return weather_data, daily_forecasts