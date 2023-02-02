from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('chatbot', views.chatbot_response, name='chatbot'),
	path('answer_question', views.answer_question, name='answer_question'),

]
# urlpatterns = [    path('chatbot', ChatbotView.as_view(), name='chatbot'),]