from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from dashboard.decorators import role_or_admin_required
from patient.models import DietRequest
from doctor import models as dc_models

UserModel = get_user_model()

@login_required
def home(request):
    """
    Main dashboard view that handles redirection and context setup based on user roles.
    
    Handles three main user types:
    1. Unapproved users - redirected to pending page
    2. Patients - redirected based on diet request status
    3. Staff/Doctors - provided with relevant user/diet request data
    
    Returns:
        HttpResponse: Rendered dashboard template with appropriate context
    """
    context = {}
    
    # Redirect unapproved users to pending page
    if request.user.profile.is_approved == False:
        return redirect('dash:pending')
    
    # Handle patient-specific logic
    if request.user.profile.role == 'PATIENT':
        try:
            # If patient has existing diet request, redirect to pending
            diet_request = DietRequest.objects.filter(patient=request.user).last()
            if diet_request:
                print(diet_request.update_status)
            context['patient_diet_request'] = diet_request
            try :
                diet = dc_models.Diet.objects.filter(diet_request=diet_request).last()
                context['diet'] = diet
                if diet_request.update_status == 'PENDING':
                    return redirect('dash:pening')
            except dc_models.Diet.DoesNotExist:        
                pass
        except DietRequest.DoesNotExist:
            # If no diet request exists, redirect to request creation
            return redirect('patient:request_a_diet')
        
    # Staff users get list of all non-superuser accounts
    if request.user.is_staff:
        # context['doctors'] = UserModel.objects.filter(profile__role='DOCTOR')
        # context['patients'] = UserModel.objects.filter(profile__role='PATIENT')
        context['users'] = UserModel.objects.all().exclude(is_superuser=True)
        
    # Doctors get list of all diet requests
    if request.user.profile.role == 'DOCTOR':
        context['diet_requests'] = DietRequest.objects.all().order_by('-date_created')
        
    return render(request, template_name='dashboard/home.html', context=context)