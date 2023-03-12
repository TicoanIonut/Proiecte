from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('calc', views.calc, name='calc'),
	path('delete_res/<int:calcresponse_id>', views.delete_res, name='delete_res'),
]
