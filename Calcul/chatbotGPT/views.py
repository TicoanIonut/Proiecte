import openai
from django.shortcuts import render
from django.views import View
from api_secrets import API_KEY

openai.api_key = API_KEY


class ChatbotView(View):
    def get(self, request):
        return render(request, 'chatbot.html')

    def post(self, request):
        user_input = request.POST.get('user_input')
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=1000,
            temperature=1,)
        return render(request, 'chatbot.html', {'response': response['choices'][0]['text']})
