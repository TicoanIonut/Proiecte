from django.urls import path
from . import views
from .views import *

# urlpatterns = [
# 	path('chatbot', views.chatbot_response, name='chatbot'),
#
# ]
urlpatterns = [    path('chatbot', ChatbotView.as_view(), name='chatbot'),]