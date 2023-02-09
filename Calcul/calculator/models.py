from django.contrib.auth.models import User
from django.db import models


class CalcResponse(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	num1 = models.TextField()
	num2 = models.TextField()
	symbol = models.TextField()
	calc_answer = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.num1, self.num2, self.calc_answer
