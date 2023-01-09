from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):

	class Meta:
		model = Order
		fields = ['ordered_by', 'shipping_adress', 'mobile', 'email']
		widgets = {
			'ordered_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
			'shipping_adress': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adress'}),
			'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
		}
		