from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


def home(request):
	return render(request, 'home.html', {})


def result(request):
	no1 = int(request.GET.get('no1'))
	no2 = int(request.GET.get('no2'))
	answer = no1 + no2
	return render(request, 'home.html', {'answer': answer})