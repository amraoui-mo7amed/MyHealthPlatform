from .generic import *
from django.utils.translation import gettext_lazy as _
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login,logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings

from django.urls import reverse
from dashboard.models import Notifications

from user_auth.models import UserProfile



@login_required
def UserProfile(request):
    return render(request,'user/profile.html')


@login_required
def EditUserProfile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        thumbnail = request.FILES.get('thumbnail')

        errors = {}
        
        if not first_name:
            errors['first_name'] = _('First name is required.')
        if not last_name:
            errors['last_name'] = _('Last name is required.')
        if not email:
            errors['email'] = _('Email is required.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Update user profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if thumbnail:
            user.profile.image = thumbnail  # Adjust this line as per your user model
        user.save()

        return JsonResponse({'success': True, 'message': 'Profile updated successfully!'})


    return render(request, 'user/edit.html')



def delete_user(request, pk):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    try:
        user = get_user_model().objects.get(pk=pk)
        user.delete()
        return JsonResponse({'success': True, 'message': 'User has been deleted'})
    except get_user_model().DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'}, status=404)

def approve_user(request, pk):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    try:
        profile = UserProfile.objects.get(pk=pk)
        if profile.is_approved:
            return JsonResponse({'success': False, 'message': 'User is already approved'})
        
        profile.is_approved = True
        profile.save()
        
        # Create notification for the approved user
        Notifications.objects.create(
            user=profile.user,
            title=_("Account Approved"),
            text=_("Your account has been approved by the admin. You can now access all features."),
        )
        
        # Send email notification
        subject = _("Account Approved")
        message = _(f"Hello {profile.user.get_full_name()} Your account has been approved by the admin. You can now access all features.")
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [profile.user.email]
        
        send_mail(subject, message, from_email, recipient_list)
        
        return JsonResponse({'success': True, 'message': 'User has been approved'})
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'}, status=404)

def pending_view(request):
    """
    View to show pending approval page
    """
    if request.user.is_authenticated and not request.user.profile.is_approved:
        return render(request, 'user/pending.html')
    return redirect('dash:home')


@login_required
def list_users(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    context = {}
    # Get all users except admins
    users = get_user_model().objects.all().exclude(is_superuser=True)
    context['users'] = users    

    return render(request, 'user/user_list.html', context=context)
    
@login_required
def userDetails(request, pk):
    if request.user.is_superuser:
        try:
            user = get_user_model().objects.get(pk=pk)
            context = {
                'user': user
            }
            return render(request, 'user/user_details.html', context=context)
        except get_user_model().DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
    return redirect('dash:home')