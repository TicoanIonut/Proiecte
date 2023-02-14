from django.urls import path
from . import views

urlpatterns = [
	path('chatbot', views.chatbot_response, name='chatbot'),
	path('delete_resp/<int:chatbotresponse_id>', views.delete_resp, name='delete_resp'),
]
