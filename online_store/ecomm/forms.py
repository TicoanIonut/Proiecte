from django import forms
from .models import Order, Customer


class CheckoutForm(forms.ModelForm):

	class Meta:
		model = Order
		fields = ['ordered_by', 'shipping_adress', 'mobile', 'email']
		widgets = {
			'ordered_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
			'shipping_adress': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
			'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
		}
		
		
class CustomerRegistrationForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
	
	class Meta:
		model = Customer
		fields = ['full_name', 'adress', 'username', 'password', 'email']
		widgets = {
			'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
			'adress': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
			'username': forms.TextInput(),
			'password': forms.PasswordInput(),
			'email': forms.EmailInput(),
		}