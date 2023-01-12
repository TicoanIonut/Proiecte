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


def calc(request):
	if request.method == 'POST':
		num1 = request.POST['num1']
		num2 = request.POST['num2']
		if 'add' in request.POST:
			res = int(num1) + int(num2)
			return render(request, 'index.html', {'res': res})
		if 'sub' in request.POST:
			res = int(num1) - int(num2)
			return render(request, 'index.html', {'res': res})
		if 'div' in request.POST:
			res = int(num1) / int(num2)
			return render(request, 'index.html', {'res': res})
		if 'mul' in request.POST:
			res = int(num1) * int(num2)
			return render(request, 'index.html', {'res': res})
	return render(request, 'index.html')