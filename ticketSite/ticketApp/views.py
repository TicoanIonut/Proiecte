from django.shortcuts import render
from .models import Ticket
from django.http import HttpResponse


def index(request):
	tickets = Ticket.objects.order_by('-created_at')[:5]
	return render(request, 'index.html', {'tickets': tickets})


def ticket_by_id(request, ticket_id):
	ticket = Ticket.objects.get(pk=ticket_id)
	return render(request, 'ticket_by_id.html', {'ticket':ticket})
