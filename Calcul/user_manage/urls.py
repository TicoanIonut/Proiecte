from django.urls import path
from . import views
from .views import CustomerRegistrationView

urlpatterns = [
	path('login_user', views.login_user, name='login_user'),
	path('register_user', views.register_user, name='register_user'),
	# path('register_user', CustomerRegistrationView.as_view(), name='register_user'),
	path('logout_user', views.logout_user, name='logout_user'),
]
