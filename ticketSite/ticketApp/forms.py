from django import forms
from django.forms import TextInput, PasswordInput, EmailInput
from ticketApp.models import *


class NewAccountForm(forms.ModelForm):
	class Meta:
		model = UserCreate
		fields = ['username', 'first_name', 'last_name', 'email', 'password', 'compartment']
		widgets = {
			'username': TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}),
			'first_name': TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}),
			'last_name': TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
			'email': EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
			'password': PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
			'compartment': forms.Select(attrs={'class': 'form-control'}),
		}
	
	def clean(self):
		field_data = self.cleaned_data
		email_value = field_data.get('email')
		usename_value = field_data.get('username')
		if User.objects.filter(email=email_value).exists():
			self._errors['email'] = self.error_class(['Email exixts, ad another email!'])
		if User.objects.filter(username=usename_value).exists():
			self._errors['username'] = self.error_class(['User exists ad another user!'])
		return field_data


class CreateTicketFormAdmin(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ('title', 'status', 'assignee', 'compartment', 'description')
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
			'status': forms.Select(attrs={'class': 'form-control'}),
			'assignee': forms.Select(attrs={'class': 'form-control'}),
			'compartment': forms.Select(attrs={'class': 'form-control'}),
			'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
		}


class CreateTicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ('title', 'status', 'compartment', 'description')
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
			'status': forms.Select(attrs={'class': 'form-control'}),
			'compartment': forms.Select(attrs={'class': 'form-control'}),
			'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
		}
