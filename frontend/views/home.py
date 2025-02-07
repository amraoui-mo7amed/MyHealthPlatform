from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json 

def home(request):
    context = {}
    return render(request, 'frontend/index.html', context=context)

