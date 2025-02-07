from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from functools import wraps

UserModel = get_user_model()

def patient_required(view_func):
    """
    Decorator to ensure user is authenticated, has PATIENT role, and confirmed email.
    Redirects unauthenticated users to login, raises PermissionDenied for others.

    HOW TO USE:
    1. Import this decorator in your views file:
       from patient.decorators import patient_required
    2. Add it above any view function that should only be accessible to patients:
       @patient_required
       def my_view(request):
           # Your view logic here

    BEHAVIOR:
    - For authenticated patients with confirmed email: Allows access to the view
    - For unauthenticated users: Redirects to login page
    - For authenticated non-patients or patients with unconfirmed email: Raises PermissionDenied
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        
        # Check all required conditions:
        # 1. User must be logged in
        # 2. User's email must be confirmed
        # 3. User must have PATIENT role
        if user.is_authenticated and user.profile.email_confirmed and user.profile.role == 'PATIENT':
            return view_func(request, *args, **kwargs)
            
        # Handle unauthorized access:
        # If user isn't logged in, redirect to login page
        if not user.is_authenticated:
            return redirect('user_auth:login')
        # If user is logged in but doesn't meet other conditions, deny access
        raise PermissionDenied("You must be a logged-in patient with confirmed email to access this page.")
    
    return _wrapped_view 