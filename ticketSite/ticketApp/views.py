from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.core.paginator import Paginator


@login_required
def create_ticket(request):
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


@login_required
def edit_ticket(request, ticket_id):
	ticket = Ticket.objects.get(pk=ticket_id)
	if request.user.is_superuser:
		form = CreateTicketFormAdmin(request.POST)
		if form.is_valid():
			form.save()
			return redirect('index')
		return render(request, 'EditTicket.html', {'ticket': ticket, 'form': form})
	else:
		if request.user == ticket.assignee or request.user.usercreate.compartment == ticket.compartment:
			form = CreateTicketForm(request.POST or None, instance=ticket)
			if form.is_valid():
				form.save()
				return redirect('index')
			return render(request, 'EditTicket.html', {'ticket': ticket, 'form': form})
		return redirect('index')


@login_required
def delete_ticket(request, ticket_id):
	ticket = Ticket.objects.get(pk=ticket_id)
	if request.user.is_superuser:
		ticket.delete()
	return render(request, 'index.html')


@login_required
def delete_users(request, user_id):
	users = User.objects.get(pk=user_id)
	if request.user.is_superuser:
		users.delete()
	return render(request, 'super_menue_users.html')


"""inactive_ticket is just for normal users"""


@login_required
def inactive_ticket(request, ticket_id):
	ticket = Ticket.objects.get(pk=ticket_id)
	if request.user == ticket.assignee or request.user.is_superuser or\
			request.user.usercreate.compartment == ticket.compartment:
		ticket.active = 0
		ticket.save()
		return redirect('index')
	

@login_required
def deactivate_ticket(request, ticket_id):
	ticket = Ticket.objects.get(pk=ticket_id)
	if request.user.is_superuser:
		ticket.active = 0
		ticket.save()
		return redirect('super_menue_tickets')
	
	
@login_required
def deactivate_users(request, user_id):
	users = UserCreate.objects.get(pk=user_id)
	if request.user.is_superuser:
		users.active = 0
		users.save()
		return redirect('super_menue_users')


@login_required
def active_ticket(request, ticket_id):
	if request.user.is_superuser:
		ticket = Ticket.objects.get(pk=ticket_id)
		ticket.active = 1
		ticket.save()
		return redirect('super_menue_tickets')
	

@login_required
def active_users(request, user_id):
	if request.user.is_superuser:
		users = UserCreate.objects.get(pk=user_id)
		users.active = 1
		users.save()
		return redirect('super_menue_users')


def index(request):
	tickets = Ticket.objects.order_by('-created_at')
	return render(request, 'index.html', {'tickets': tickets})


@login_required
def index_search(request):
	if request.method == "POST":
		searched = request.POST['searched']
		tickets = Ticket.objects.filter(title__icontains=searched) or \
		          Ticket.objects.filter(compartment__icontains=searched) or \
		          Ticket.objects.filter(id__icontains=searched) or \
		          Ticket.objects.filter(created_at__icontains=searched) or \
		          Ticket.objects.filter(updated_at__icontains=searched) or \
		          Ticket.objects.filter(status__icontains=searched)
		return render(request, 'index_search.html', {'tickets': tickets, 'searched': searched})
	else:
		return render(request, 'index_search.html', {})


@login_required
def super_menue_tickets(request):
	if request.user.is_superuser:
		tickets = Ticket.objects.order_by('-created_at')
		return render(request, 'super_menue_tickets.html', {'tickets': tickets})


@login_required
def super_menue_users(request):
	if request.user.is_superuser:
		users = User.objects.order_by('-date_joined')
		return render(request, 'super_menue_users.html', {'users': users})


@login_required
def ticket_by_id(request, ticket_id):
	ticket = Ticket.objects.get(pk=ticket_id)
	if request.user == ticket.assignee or request.user.is_superuser or\
			request.user.usercreate.compartment == ticket.compartment:
		return render(request, 'ticket_by_id.html', {'ticket': ticket})
	else:
		return redirect('index')


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


@login_required
def logout_request(request):
	logout(request)
	return redirect('index')
