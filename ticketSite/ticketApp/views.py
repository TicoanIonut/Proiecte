from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import *
from .models import *


def create_ticket(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			if request.user.is_superuser:
				form = CreateTicketFormAdmin(request.POST)
				if form.is_valid():
					form.save()
					return redirect('index')
			else:
				form = CreateTicketForm(request.POST)
				if form.is_valid():
					ticket = form.save(commit=False)
					ticket.assignee = request.user
					ticket.save()
					return redirect('index')
		else:
			if request.user.is_superuser:
				form = CreateTicketFormAdmin(request.POST)
			else:
				form = CreateTicketForm
		return render(request, 'CreateTicket.html', {'form': form})
	return render(request, 'index.html')


def edit_ticket(request, ticket_id):
	if request.user.is_authenticated:
		ticket = Ticket.objects.get(pk=ticket_id)
		if request.user.is_superuser:
			form = CreateTicketFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return redirect('index')
		else:
			if request.user == ticket.assignee or request.user.usercreate.compartment == ticket.compartment:
				form = CreateTicketForm(request.POST or None, instance=ticket)
				if form.is_valid():
					form.save()
					return redirect('index')
				return render(request, 'EditTicket.html', {'ticket': ticket, 'form': form})
			return redirect('index')
	return render(request, 'index.html')


def delete_ticket(request, ticket_id):
	if request.user.is_authenticated:
		ticket = Ticket.objects.get(pk=ticket_id)
		if request.user == ticket.assignee or request.user.is_superuser:
			ticket.delete()
			return redirect('index')
		else:
			return redirect('index')
	return render(request, 'index.html')


def index(request):
	tickets = Ticket.objects.order_by('-created_at')
	return render(request, 'index.html', {'tickets': tickets})


def ticket_by_id(request, ticket_id):
	if request.user.is_authenticated:
		ticket = Ticket.objects.get(pk=ticket_id)
		if request.user == ticket.assignee or request.user.is_superuser:
			return render(request, 'ticket_by_id.html', {'ticket': ticket})
		else:
			return redirect('index')
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
				return redirect('login_request')
	form = AuthenticationForm()
	return render(request, "login_request.html", {'form': form})


def logout_request(request):
	logout(request)
	return redirect('index')
