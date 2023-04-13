from django.urls import path
from . import views


urlpatterns = [
	path('weather_index', views.weather_index, name='weather_index'),

]
