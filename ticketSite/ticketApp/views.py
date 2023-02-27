from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.db.models import Q


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
		form = CreateTicketFormAdmin(request.POST or None, request.FILES or None, instance=ticket)
		if form.is_valid():
			form.save()
			return redirect('index')
		return render(request, 'EditTicket.html', {'ticket': ticket, 'form': form})
	else:
		if request.user == ticket.assignee or request.user.usercreate.compartment == ticket.compartment:
			form = CreateTicketForm(request.POST or None, request.FILES or None, instance=ticket)
			if form.is_valid():
				form.save()
				return redirect('index')
			return render(request, 'EditTicket.html', {'ticket': ticket, 'form': form})
		return redirect('index')


@login_required
def edit_users(request, user_id):
	users = User.objects.get(pk=user_id)
	form = NewAccountForm(request.POST or None, request.FILES or None, instance=users)
	if request.user.is_superuser:
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			email = form.cleaned_data.get('email')
			comp = form.cleaned_data.get('compartment')
			user = form.save()
			user.set_password(user.password)
			user.save()
			return redirect('super_menue_users')
		return render(request, 'EditUsers.html', {'users': users, 'form': form})
	return render(request, 'EditUsers.html', {'users': users, 'form': form})
	

@login_required
def delete_ticket(request, ticket_id):
	ticket = Ticket.objects.get(pk=ticket_id)
	if request.user.is_superuser:
		ticket.delete()
		return redirect('super_menue_users')
	return render(request, 'index.html')


@login_required
def delete_users(request, user_id):
	users = User.objects.get(pk=user_id)
	if request.user.is_superuser:
		users.delete()
		return redirect('super_menue_users')
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
	users = User.objects.get(pk=user_id)
	if request.user.is_superuser:
		users.is_active = False
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
		users = User.objects.get(pk=user_id)
		users.is_active = True
		users.save()
		return redirect('super_menue_users')


def index(request):
	p = Paginator(Ticket.objects.order_by('-created_at'), 8)
	page = request.GET.get('page')
	tickets = p.get_page(page)
	return render(request, 'index.html', {'tickets': tickets})


def index_updated(request):
	p = Paginator(Ticket.objects.order_by('-updated_at'), 8)
	page = request.GET.get('page')
	tickets = p.get_page(page)
	return render(request, 'index.html', {'tickets': tickets})


def status_updated(request):
	p = Paginator(Ticket.objects.order_by('-status'), 8)
	page = request.GET.get('page')
	tickets = p.get_page(page)
	return render(request, 'index.html', {'tickets': tickets})


def status_compartment(request):
	p = Paginator(Ticket.objects.order_by('-compartment'), 8)
	page = request.GET.get('page')
	tickets = p.get_page(page)
	return render(request, 'index.html', {'tickets': tickets})


def status_created_by(request):
	p = Paginator(Ticket.objects.order_by('-assignee'), 8)
	page = request.GET.get('page')
	tickets = p.get_page(page)
	return render(request, 'index.html', {'tickets': tickets})


def status_summary(request):
	p = Paginator(Ticket.objects.order_by('-title'), 8)
	page = request.GET.get('page')
	tickets = p.get_page(page)
	return render(request, 'index.html', {'tickets': tickets})


@login_required
def searches(request):
	word = Ticket.objects.all()
	res = request.GET.get('search')
	if res:
		word = Ticket.objects.filter(Q(title__icontains=res) | Q(compartment__icontains=res) | Q(status__icontains=res) | Q(assignee__username__icontains=res)).distinct()
	paginator = Paginator(word, 6)
	page = request.GET.get('page')
	try:
		results = paginator.page(page)
	except PageNotAnInteger:
		results = paginator.page(1)
	except EmptyPage:
		results = paginator.page(paginator.num_pages)
	context = {'results': results, 'search_query': res}
	if res:
		context['search_query'] = res
		context['search_url'] = f'?search={res}&'
	return render(request, 'search.html', context)

# def index_search(request):
# 	search = request.GET.get('search')
# 	tickets = Ticket.objects.filter(Q(title__icontains=search) | Q(compartment__icontains=search) |
# 	                                Q(id__icontains=search) | Q(created_at__icontains=search) |
# 	                                Q(updated_at__icontains=search) | Q(status__icontains=search))
# 	return render(request, 'search.html', {'tickets': tickets, 'search': search})


@login_required
def super_menue_tickets(request):
	if request.user.is_superuser:
		p = Paginator(Ticket.objects.order_by('-created_at'), 8)
		page = request.GET.get('page')
		tickets = p.get_page(page)
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
			user.is_active = False
			user.save()
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
				if UserCreate.active:
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
