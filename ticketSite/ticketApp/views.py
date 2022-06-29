from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import NewAccountForm, CreateTicketForm
from .models import *


def create_ticket(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = CreateTicketForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('index')
		form = CreateTicketForm
		return render(request, 'CreateTicket.html', {'form': form})
	return render(request, 'index.html')


def edit_ticket(request, ticket_id):
	if request.user.is_authenticated:
		ticket = Ticket.objects.get(pk=ticket_id)
		form = CreateTicketForm(request.POST or None, instance=ticket)
		if form.is_valid():
			form.save()
			return redirect('index')
		return render(request, 'EditTicket.html', {'ticket': ticket, 'form': form})
	return render(request, 'index.html')


def delete_ticket(request, ticket_id):
	if request.user.is_authenticated:
		ticket = Ticket.objects.get(pk=ticket_id)
		ticket.delete()
		return redirect('index')
	return render(request, 'index.html')


def index(request):
	tickets = Ticket.objects.order_by('-created_at')
	return render(request, 'index.html', {'tickets': tickets})


def ticket_by_id(request, ticket_id):
	if request.user.is_authenticated:
		ticket = Ticket.objects.get(pk=ticket_id)
		return render(request, 'ticket_by_id.html', {'ticket': ticket})
	return render(request, 'index.html')


def register_request(request):
	if request.method == "POST":
		form = NewAccountForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			email = form.cleaned_data.get('email')
			comp = form.cleaned_data.get('compartment')
			user = form.save()
			user.set_password(user.password)
			user.save()
			user = authenticate(username=username, password=password, email=email, compartment=comp)
			login(request, user)
			return redirect('index')
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
				return redirect('index')
			else:
				messages.success(request, ("There Was An Error Logging In, Try Again..."))
				return redirect('login_request')
	form = AuthenticationForm()
	return render(request, "login_request.html", {'form': form})


def logout_request(request):
	logout(request)
	return redirect('index')
