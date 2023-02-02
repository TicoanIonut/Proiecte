import openai
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from api_secrets import API_KEY
from .models import ChatbotResponse

openai.api_key = API_KEY

# @login_required


def chatbot_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        response = openai.Completion.create(
            engine="text-davinci-003",prompt=user_input,max_tokens=1000,temperature=1,)
        response_text = response['choices'][0]['text']
        # ChatbotResponse.objects.create(question=user_input, answer=response_text)
        ChatbotResponse.objects.create(user=request.user, question=user_input, answer=response_text)
        context = {'question': user_input, 'answer': response_text}
        return render(request, 'chatbot.html', context)
    return render(request, 'chatbot.html')


def answer_question(request):
    rendering = ChatbotResponse.objects.all()
    context = {'rendering': rendering}
    return render(request, 'answer_question.html', context)
