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
                login(request,user)
                if user.profile.is_approved:
                    return JsonResponse({'redirect_url': reverse('dash:home')})  # Redirect to dashboard or another page
                else:
                    return JsonResponse({'success':True,'redirect_url' : reverse('dash:pending')})
            else:
                return JsonResponse({'errors': [_('Invalid credentials.')]})
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
                    role=role
                )
                print(role)
                notification = Notifications.objects.create(
                    user=admin,
                    title=_("New Doctor registered"),
                    text=_("A new Doctor registered. Please approve. <a href='{}' class='text-primary'>View Profile</a>").format(reverse('dash:user-details', args=[user.pk])),
                )
                admin.profile.notifications_count += 1
                admin.profile.save()                                           
                user.save()
                profile.save()
                notification.save()
                if role == 'PATIENT':
                    login(request, user)
                    return JsonResponse({'success': True, 'redirect_url': reverse('dash:patient_data')})
                else:
                    return JsonResponse({'success': True, 'redirect_url': reverse('dash:home')})
            except Exception as e:
                errors.append(str(e))
                return JsonResponse({'errors': errors, 'success': False})

    return render(request, 'auth/register.html')

