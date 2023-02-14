import openai
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from api_secrets import API_KEY
from .models import ChatbotResponse

openai.api_key = API_KEY


def chatbot_response(request):
    p = Paginator(ChatbotResponse.objects.all().order_by('-created_at'), 2)
    page = request.GET.get('page')
    rendering = p.get_page(page)
    nums = "a" * rendering.paginator.num_pages
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        response = openai.Completion.create(
            engine="text-davinci-003", prompt=user_input, max_tokens=1000, temperature=1)
        response_text = response['choices'][0]['text']
        ChatbotResponse.objects.create(user=request.user, question=user_input, answer=response_text)
        return render(request, 'answer_question.html',
                      {'user_input': user_input, 'response_text': response_text, 'rendering': rendering, 'nums': nums})
    return render(request, 'answer_question.html', {'rendering': rendering, 'nums': nums})


def delete_resp(request, chatbotresponse_id):
    calcresponse = ChatbotResponse.objects.get(pk=chatbotresponse_id)
    calcresponse.delete()
    return redirect('chatbot')

