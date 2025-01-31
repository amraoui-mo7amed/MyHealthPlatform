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

from django.urls import reverse
from dashboard.models import Notifications

from user_auth.models import UserProfile
from dashboard.forms.user import PatientDataForm
from dashboard.models.user import PatientData



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
def patient_data_view(request):
    if request.user.profile.role != 'PATIENT':
        return redirect('dash:home')
    
    try:
        patient_data = request.user.patient_data
    except PatientData.DoesNotExist:
        patient_data = None

    # Initialize form for both GET and POST
    form = PatientDataForm(instance=patient_data)

    if request.method == 'POST':
        try:
            form = PatientDataForm(request.POST, instance=patient_data)
            if form.is_valid():
                patient_data = form.save(commit=False)
                patient_data.user = request.user
                patient_data.save()
                return JsonResponse({'success': True, 'redirect_url': reverse('dash:home')})
            else:
                # Return form errors if validation fails
                errors = {field: error_list for field, error_list in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'errors': {'__all__': [str(e)]}}, status=500)

    # Handle GET request - render the form
    return render(request, 'user/patient_data.html', {'form': form})

@require_POST
def patient_data(request):
    form = PatientDataForm(request.POST)
    
    try:
        if form.is_valid():
            # Process the form data
            instance = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Patient data saved successfully!',
                'data': {
                    'id': instance.id,
                    # Add any other relevant data you want to return
                }
            })
        else:
            # Format errors for AJAX response
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list
            
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
            
    except ValidationError as e:
        # Handle specific validation errors
        return JsonResponse({
            'success': False,
            'errors': {'__all__': [str(e)]}
        }, status=400)
        
    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({
            'success': False,
            'errors': {'__all__': ['An unexpected error occurred. Please try again.']}
        }, status=500)
    

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