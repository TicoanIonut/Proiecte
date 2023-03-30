from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput, EmailInput


# class SignUpForm(forms.ModelForm):
# 	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
# 	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
# 	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
# 	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
# 	email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
#
# 	class Meta:
# 		model = User
# 		fields = ['username', 'first_name', 'last_name', 'email', 'password']
# 		widgets = {
# 			'username': TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
# 			'first_name': TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}),
# 			'last_name': TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
# 			'email': EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
# 			'password': PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
#
# 		}
#
# 	def clean(self):
# 		field_data = self.cleaned_data
# 		email_value = field_data.get('email')
# 		usename_value = field_data.get('username')
# 		if User.objects.filter(email=email_value).exists():
# 			self._errors['email'] = self.error_class(['Email exixts, ad another email!'])
# 		if User.objects.filter(username=usename_value).exists():
# 			self._errors['username'] = self.error_class(['User exists ad another user!'])
# 		return field_data


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label='',
	                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
	first_name = forms.CharField(label='', max_length=100,
	                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
	last_name = forms.CharField(label='', max_length=100,
	                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password1')
	
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields[
			'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
		
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields[
			'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
		
		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields[
			'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'