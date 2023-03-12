from django.contrib.auth.models import User
from django.db import models


class Conversation(models.Model):
	members = models.ManyToManyField(User, related_name='conversations')
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
		
		
class ConversationMessage(models.Model):
	conversation = models.ForeignKey(Conversation, related_name='mesages', on_delete=models.CASCADE)
	content = models.CharField(max_length=9999)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)
	
	
	