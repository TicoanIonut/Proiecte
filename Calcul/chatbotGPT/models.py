from django.contrib.auth.models import User
from django.db import models


class ChatbotResponse(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.TextField()
	answer = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.question, self.answer
