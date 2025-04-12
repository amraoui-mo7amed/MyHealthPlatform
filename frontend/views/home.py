from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json 
from frontend.models.contact import Contact

def home(request):
    context = {}
    return render(request, 'frontend/index.html', context=context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        errors = []

        if not name:
            errors.append('please provide your name')
        if not email:
            errors.append('Please provide your E-mail')
        if not message:
            errors.append('Please provide the message')
        
        if '@' not in email:
            errors.append('Provide a valid e-mail')

        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            })

        try:
            contact = Contact.objects.create(
                name=name,
                email=email,
                message=message
            )
            contact.save()
            # send_mail(
            #     'Contact Form Submission',
            #     f"Name: {name}\nEmail: {email}\nMessage: {message}",
            #     email,
            #     ['myhealthypartner0@gmail.com'],
            #     fail_silently=False,
            # )
            return JsonResponse({
                'success': True,
                'message': 'Your message has been sent successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': ['Failed to send the message. Please try again later.']
            })