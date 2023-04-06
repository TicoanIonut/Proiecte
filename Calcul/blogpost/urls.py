from django.urls import path
from . import views


urlpatterns = [
    path('conversation/', views.view_conversation, name='view_conversation'),
    path('delete_msg/<int:blog_id>', views.delete_msg, name='delete_msg'),
]
