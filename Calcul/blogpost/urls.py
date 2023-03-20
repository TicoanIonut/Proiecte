from django.urls import path
from .views import *

urlpatterns = [
    path('conversation/', view_conversation, name='view_conversation'),
]
