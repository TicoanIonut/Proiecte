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
	path('register', CustomerRegistrationView.as_view(), name='customerregistration'),
	path('logout/', CustomerLogoutView.as_view(), name='customerlogout'),
	path('login/', CustomerLoginView.as_view(), name='customerlogin'),
	path('profile/', CustomerProfileView.as_view(), name='customerprofile'),
	path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),
	path("search/", SearchView.as_view(), name="searches"),
	# path("search/", views.searches, name="searches"),

	path("forgot-password/", PasswordForgotView.as_view(), name="passwordforgot"),
	path("password-reset/<email>/<token>/", PasswordResetView.as_view(), name="passwordreset"),
	path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
	
	path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
	path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
	path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(), name="adminorderdetail"),
	path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),
	path("admin-order-<int:pk>-change/", AdminOrderStatusChangeView.as_view(), name="adminorderstatuschange"),
	path("admin-product/list/", AdminProductListView.as_view(), name="adminproductlist"),
	path("admin-product/add/", AdminProductCreateView.as_view(), name="adminproductcreate"),
	path("admin-product/edit/<int:prod_id>/", views.edit_product, name="adminproductedit"),
	path("admin-product/delete/<int:prod_id>/", views.delete_product, name="adminproductdelete"),
	path("adminsearch/", AdminSearchView.as_view(), name="adminsearches"),
	path("admin-customer/list/", AdminCustomerListView.as_view(), name="admincustomerlist"),
	path("admin-customer-search/", AdminCustomerSearchView.as_view(), name="admincustomersearch"),
	path("admin-delete-customers/<int:customer_id>/", views.delete_users, name="admindeletecustomers"),
	path("admin-toggle-customers/<int:customer_id>/", views.toggle_user_active, name="admintogglecustomers"),
	path("admin-edit-customers/<int:customer_id>/", views.admin_edit_customers, name="admineditcustomers"),
	path("edit-customers/<int:customer_id>/", views.edit_customers, name="editcustomers"),
]
