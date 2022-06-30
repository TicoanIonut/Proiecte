from django.contrib import admin
from .models import *


class TicketAdmin(admin.ModelAdmin):
	date_hierarchy = 'created_at'
	list_filter = ('status', 'assignee')
	list_display = ('id', 'title', 'status', 'assignee', 'description', 'updated_at')
	search_fields = ['title', 'status']
	

class UserAdmin(admin.ModelAdmin):
	date_hierarchy = 'created_at'
	list_filter = ('status', 'assignee')
	list_display = ('id', 'title', 'status', 'assignee', 'description', 'updated_at')
	search_fields = ['title', 'status']

	
admin.site.register(Ticket, TicketAdmin)
admin.site.register(UserCreate)
