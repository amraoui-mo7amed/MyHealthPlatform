from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

UserModel = get_user_model()

@login_required
def home(request):
    if request.user.profile.is_approved == False:
        return redirect('dash:pending')
    
    context = {
        'doctors':UserModel.objects.filter(profile__role='DOCTOR'),
        'patients':UserModel.objects.filter(profile__role='PATIENT'),
        'users' : UserModel.objects.all().exclude(is_superuser=True)
    }
    return render(request,template_name='dashboard/home.html',context=context)