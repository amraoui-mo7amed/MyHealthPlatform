from django.http import JsonResponse
from decouple import config

def get_chat_token(request):
    return JsonResponse({
            'token': config('OPENROUTER_API_KEY')
    })