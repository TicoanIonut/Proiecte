from django.urls import path
from .views import *

app_name = 'ecomm'
urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('product/<slug:slug>/', ProductDetailView.as_view(), name='productdetail'),
	path('addtocart<int:pro_id>/', AddToCartView.as_view(), name='addtocart'),
	path('mycart/', MyCartView.as_view(), name='mycart'),
	path('managecart/<int:cp_id>/', ManageCartView.as_view(), name='managecart'),
	path('emptycart/', EmptyCartView.as_view(), name='emptycart'),
	path('checkout/', CheckoutView.as_view(), name='checkout'),
	path('register/', CustomerRegistrationView.as_view(), name='customerregistration'),
	path('logout/', CustomerLogoutView.as_view(), name='customerlogout'),
	path('login/', CustomerLoginView.as_view(), name='customerlogin'),
	path('profile/', CustomerProfileView.as_view(), name='customerprofile'),
	path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),
	
]