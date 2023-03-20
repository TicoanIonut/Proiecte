from django.contrib.auth.models import User
from django.db import models


class BlogPost(models.Model):
	members = models.ForeignKey(User, related_name='blogpost', on_delete=models.DO_NOTHING)
	created_at = models.DateTimeField(auto_now_add=True)
	content = models.CharField(max_length=500)
	
	def __str__(self):
		return (f"{self.members} "f"({self.created_at:%Y-%m-%d %H:%M}): "f"{self.content}")
