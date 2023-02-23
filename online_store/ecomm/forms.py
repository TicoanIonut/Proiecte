from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput, EmailInput, TextInput

from .models import Order, Customer


class CheckoutForm(forms.ModelForm):

	class Meta:
		model = Order
		fields = ['ordered_by', 'shipping_address', 'mobile', 'email']
		widgets = {
			'ordered_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
			'shipping_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
			'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
		}
		
		
class CustomerRegistrationForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))

	class Meta:
		model = Customer
		fields = ["username", "password", "email", "full_name", "address"]
		widgets = {
			'username': TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
			'password': PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
			'email': EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
			'full_name': TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'}),
			'address': TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
		}
	
	def clean_username(self):
		uname = self.cleaned_data.get("username")
		if User.objects.filter(username=uname).exists():
			raise forms.ValidationError("Customer with this username already exists.")
	
		return uname


class CustomerLoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))
	
	
class PasswordForgotForm(forms.Form):
	email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email fot the account', 'class': 'form-control'}))
	
	def clean_email(self):
		e = self.cleaned_data.get('email')
		if Customer.objects.filter(user__email=e).exists():
			pass
		else:
			raise forms.ValidationError('Customer with this email does not exist')
		return e
			