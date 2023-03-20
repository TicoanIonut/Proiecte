from django.core.checks import messages
from django.shortcuts import render, redirect
from .models import *
from .forms import ConversationMessageForm


def view_conversation(request):
	if request.user.is_authenticated:
		form = ConversationMessageForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid():
				message = form.save(commit=False)
				message.members = request.user
				message.save()
				return redirect('view_conversation')
		
		message = BlogPost.objects.all().order_by("-created_at")
		return render(request, 'conversation.html', {"message": message, 'form': form})
	
	else:
		message = BlogPost.objects.all().order_by("-created_at")
		return render(request, 'conversation.html', {"message": message})
	