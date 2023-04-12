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


def register_user(request):
	form = SignUpForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			user = authenticate(username=username, password=password, email=email)
			login(request, user)
			return redirect('home')
	return render(request, 'register.html', {'form': form})


def logout_user(request):
	logout(request)
	return redirect('home')
