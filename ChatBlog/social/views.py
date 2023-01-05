from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


def result(request):
	no1 = int(request.GET.get('no1'))
	no2 = int(request.GET.get('no2'))
	answer = no1 + no2
	return render(request, 'home.html', {'answer': answer})


def home(request):
	return render(request, 'home.html', {})


def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles": profiles})
	else:
		messages.success(request, ('You must be logged in in order to view Profiles'))
		return redirect('home')


