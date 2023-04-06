from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from user_manage.forms import *


def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			return redirect('login_user')
	else:
		return render(request, 'login.html', {})


# def register_user(request):
# 	form = SignUpForm(request.POST)
# 	if request.method == 'POST':
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			email = form.cleaned_data.get('email')
# 			user = User.objects.create_user(username=username, password=password, email=email)
# 			user.first_name = form.cleaned_data.get('first_name')
# 			user.last_name = form.cleaned_data.get('last_name')
# 			user.save()
# 			login(request, user)
# 			return redirect('home')
# 	return render(request, 'register.html', {'form': form})

def register_user(request):
	form = SignUpForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			user = authenticate(username=username, password=password, email=email)
			login(request, user)
			return redirect('home')
	# else:
	
	return render(request, 'register.html', {'form': form})

class CustomerRegistrationView(CreateView):
	template_name = "register.html"
	form_class = SignUpForm
	success_url = reverse_lazy("index")
	
	def form_valid(self, form):
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		email = form.cleaned_data.get("email")
		user = User.objects.create_user(username, email, password)
		form.instance.user = user
		return super().form_valid(form)


def logout_user(request):
	logout(request)
	return redirect('home')
