from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket/<int:ticket_id>', views.ticket_by_id, name='ticket_by_id'),
    
    path('login_request/', views.login_request, name='login_request'),
    path('register_request/', views.register_request, name='register_request'),
    path('logout_request/', views.logout_request, name='logout_request'),
    path('CreateTicket/', views.create_ticket, name='CreateTicket'),
    path('EditTicket<ticket_id>/', views.edit_ticket, name='EditTicket'),
    path('index_search/', views.searches, name='searches'),
    path('index_updated/', views.index_updated, name='index_updated'),
    path('status_updated/', views.status_updated, name='status_updated'),
    path('status_created_by/', views.status_created_by, name='status_created_by'),
    path('status_compartment/', views.status_compartment, name='status_compartment'),
    path('status_summary/', views.status_summary, name='status_summary'),
    
    
    path('DeleteTicket<ticket_id>/', views.delete_ticket, name='DeleteTicket'),
    path('InactiveTicket<ticket_id>/', views.inactive_ticket, name='InactiveTicket'),
    path('DeactivateTicket<ticket_id>/', views.deactivate_ticket, name='DeactivateTicket'),
    path('ActiveTicket<ticket_id>/', views.active_ticket, name='ActiveTicket'),
    path('SuperMenueTickets/', views.super_menue_tickets, name='super_menue_tickets'),
    
    path('SuperMenueUsers/', views.super_menue_users, name='super_menue_users'),
    path('DeleteUser<user_id>/', views.delete_users, name='DeleteUsers'),
    path('DeactivateUser<user_id>/', views.deactivate_users, name='DeactivateUsers'),
    path('ActiveUser<user_id>/', views.active_users, name='ActiveUsers'),
    path('EditUsers<user_id>', views.edit_users, name='EditUsers')
    
    
]