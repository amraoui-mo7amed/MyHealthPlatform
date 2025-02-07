from django.contrib import messages
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

from django.contrib.auth import get_user_model
from user_auth.models import OTP

userModel = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dash:home')
    if request.method == 'POST':
        try: 
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(password)
            # Example validation checks (replace with actual logic)
            errors = []
            if not username:
                errors.append(_("Username is required."))
            if not password:
                errors.append(_("Password is required."))

            if errors:
                # If errors, return them as a JSON response
                return JsonResponse({'errors': errors})
            
            # Authentication and login logic (you can replace with actual user login)
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if not user.profile.email_confirmed:
                    return JsonResponse({'errors': [_('Please confirm your email address before logging in.')]})
                if not user.profile.is_approved:
                    return JsonResponse({'errors': [_('Your account is pending approval. Please wait for admin approval.')]})
                login(request,user)
                return JsonResponse({'success':True,'redirect_url' : reverse('patient:request_a_diet')})
            else:
                return JsonResponse({'errors': [_('Invalid credentials.')],'success':False})
        except Exception as e:
            print(e)

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('user_auth:login')  # Redirects to the homepage (or any page you choose)

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            return JsonResponse({'success': True,'message':email})
    return render(request, 'auth/password_reset.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birthdate = request.POST.get('birthdate')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Add new fields from the template
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        wilaya = request.POST.get('wilaya')
        certificate_serial = request.POST.get('certificate_serial')
        speciality = request.POST.get('speciality')

        # Move User model definition to the top of the function
        User = get_user_model()
        admin = User.objects.filter(is_superuser=True).first()
        errors = []

        # Field validation
        required_fields = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'birthdate': birthdate,
            'email': email,
            'role': role,
            'password1': password1,
            'password2': password2
        }
        
        for field, value in required_fields.items():
            if not value:
                errors.append(_(f"{field.replace('_', ' ').title()} is required."))

        # Add validation for new fields
        if not gender:
            errors.append(_("Gender is required."))
        if not phone_number:
            errors.append(_("Phone number is required."))
        if not wilaya:
            errors.append(_("Wilaya is required."))
        if role == 'DOCTOR':
            if not certificate_serial:
                errors.append(_("Certificate serial is required for doctors."))
            if not speciality:
                errors.append(_("Speciality is required for doctors."))

        # Password validation
        if password1 != password2:
            errors.append(_("Passwords do not match."))
        elif len(password1) < 4:
            errors.append(_("Password must be at least 4 characters."))

        # Unique validation
        if User.objects.filter(email=email).exists():
            errors.append(_("Email already exists."))
        if User.objects.filter(username=username).exists():
            errors.append(_("Username already exists."))

        # Role validation
        if role not in ['PATIENT', 'DOCTOR']:
            errors.append(_("Invalid role."))

        if len(errors) > 0:
            return JsonResponse({'errors': errors, 'success': False})
        else:
            try:
                # Only create user if no errors exist
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1,
                )
                
                profile = UserProfile.objects.create(
                    user=user,
                    birthdate=birthdate,
                    image='images/user-teal.png',
                    notifications_count=0,
                    role=role,
                    gender=gender,
                    phone_number=phone_number,
                    is_approved = False if role == 'DOCTOR' else True,
                    wilaya=wilaya,
                    certificate_serial=certificate_serial if role == 'DOCTOR' else None,
                    speciality=speciality if role == 'DOCTOR' else None
                )
                
                user.save()
                profile.save()
                if role == 'DOCTOR':
                    # Send notification to admin
                    notification = Notifications.objects.create(
                        user=admin,
                        title=_("New Doctor registered"),
                        text=_("A new Doctor registered. Please approve. <a href='{}' class='text-primary'>View Profile</a>").format(reverse('dash:user-details', args=[user.pk])),
                    )
                    admin.profile.notifications_count += 1
                    admin.profile.save()                                           
                    notification.save()
                # Return success response without logging in
                if role == 'PATIENT':
                    return JsonResponse({
                        'success': True,
                        'message': _('Registration successful! Please confirm your e-mail.'),
                        'redirect_url': reverse('user_auth:login')
                    })
                else:
                    return JsonResponse({
                        'success': True,
                        'message': _('Registration successful! Please confirm your e-mail & wait for admin approval.'),
                        'redirect_url': reverse('user_auth:login')
                    })
            except Exception as e:
                errors.append(str(e))
                return JsonResponse({'errors': errors, 'success': False})

    return render(request, 'auth/register.html')


def activate_email(request):
    """
    Handle email activation using the token sent to the user
    """
    token = request.GET.get('token')
    
    if not token:
        messages.error(request, _('Activation token is missing.'))
        return render(request, 'emails/activation_status.html')

    try:
        # Get the OTP instance for this token
        otp = OTP.objects.get(code=token)
        if not otp.is_valid():
            messages.error(request, _('Activation link has expired. Please request a new one.'))
            return render(request, 'emails/activation_status.html')
        
        # Activate the user
        user = otp.user
        user.profile.email_confirmed = True
        user.profile.save()
        user.save()
        
        # Delete the used OTP
        otp.delete()
        
        messages.success(request, _('Your account has been successfully activated! You can now login.'))
        return render(request, 'emails/activation_status.html')
    
    except OTP.DoesNotExist:
        messages.error(request, _('Invalid activation link.'))
        return render(request, 'emails/activation_status.html')
    
    except Exception as e:
        messages.error(request, _('An error occurred during activation. Please try again.'))
        return render(request, 'emails/activation_status.html')

