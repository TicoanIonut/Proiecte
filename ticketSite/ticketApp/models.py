from django.db import models
from django.contrib.auth.models import User


class TicketStatus(models.TextChoices):
	TO_DO = 'To Do'
	IN_PROGRESS = 'In Progress'
	IN_REVIEW = 'In Review'
	DONE = 'Done'


class Compartiment(models.TextChoices):
	comp1 = 'comp1'
	comp2 = 'comp2'
	comp3 = 'comp3'
	comp4 = 'comp4'


class Ticket(models.Model):
	title = models.CharField(max_length=100)
	assignee = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	status = models.CharField(max_length=25, choices=TicketStatus.choices, default=TicketStatus.TO_DO)
	compartment = models.CharField(max_length=25, choices=Compartiment.choices, default=Compartiment.comp1)
	description = models.TextField()
	created_at = models.DateTimeField('created at', auto_now_add=True)
	updated_at = models.DateTimeField('updated at', auto_now=True)
	active = models.BooleanField(default=True)


class UserCreate(User):
	compartment = models.CharField(max_length=25, choices=Compartiment.choices, default=None)
	active = models.BooleanField(default=True)
