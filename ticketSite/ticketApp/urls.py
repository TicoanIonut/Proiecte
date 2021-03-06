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
    path('DeleteTicket<ticket_id>/', views.delete_ticket, name='DeleteTicket'),
]