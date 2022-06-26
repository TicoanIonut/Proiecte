from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render
from .forms import NewAccountForm
from .models import Ticket


def index(request):
	tickets = Ticket.objects.order_by('-created_at')[:5]
	return render(request, 'index.html', {'tickets': tickets})


def ticket_by_id(request, ticket_id):
	ticket = Ticket.objects.get(pk=ticket_id)
	return render(request, 'ticket_by_id.html', {'ticket':ticket})


def register_request(request):
	if request.method == "POST":
		form = NewAccountForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			email = form.cleaned_data.get('email')
			user = authenticate(username=username, password=password, email=email)
			login(request, user)
			return render(request, "index.html")
	form = NewAccountForm()
	return render(request, "register_request.html", {"form": form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return render(request, "index.html")
			else:
				messages.success(request, "Incorrect username or password.")
		else:
			messages.success(request, "Incorrect username or password.")
	form = AuthenticationForm()
	return render(request, "login_request.html", {'form': form})


def logout_request(request):
	logout(request)
	return render(request, "index.html")
