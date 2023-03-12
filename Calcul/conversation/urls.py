from django.urls import path
from .views import view_conversation, start_conversation

urlpatterns = [
    path('conversation/<int:conversation_id>/', view_conversation, name='view_conversation'),
    path('conversation/', start_conversation, name='start_conversation'),
]