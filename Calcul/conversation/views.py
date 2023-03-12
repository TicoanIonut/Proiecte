from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm


def view_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, members=request.user)
    messages = conversation.mesages.order_by('created_at')
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()
            return redirect('view_conversation', conversation_id=conversation.id)
    else:
        form = ConversationMessageForm()
    context = {
        'conversation': conversation,
        'messages': messages,
        'form': form,
    }
    return render(request, 'start_conversation.html', context)


def start_conversation(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        recipient = User.objects.get(id=user_id)
        conversation = Conversation.objects.create()
        conversation.members.add(request.user)
        conversation.members.add(recipient)
        content = request.POST.get('message')
        message = ConversationMessage.objects.create(conversation=conversation, content=content, created_by=request.user)
        return redirect('view_conversation', conversation_id=conversation.id)
    else:
        users = User.objects.exclude(id=request.user.id)
        context = {
            'users': users,
        }
        return render(request, 'start_conversation.html', context)