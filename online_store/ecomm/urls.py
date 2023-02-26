from django.urls import path

from . import views
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
	# path("search/", SearchView.as_view(), name="searches"),
	path("search/", views.searches, name="searches"),
	path("forgot-password/", PasswordForgotView.as_view(), name="passwordforgot"),
	path("password-reset/<email>/<token>/", PasswordResetView.as_view(), name="passwordreset"),
	
	path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
	path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
	path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(), name="adminorderdetail"),
	path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),
	path("admin-order-<int:pk>-change/", AdminOrderStatusChangeView.as_view(), name="adminorderstatuschange"),
	path("admin-product/list/", AdminProductListView.as_view(), name="adminproductlist"),
	path("admin-product/add/", AdminProductCreateView.as_view(), name="adminproductcreate"),
	
	
]