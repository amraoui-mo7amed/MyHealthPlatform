from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def role_or_admin_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            # ... existing code ...
            
            # Check if user is admin
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            # Check if user has the required role
            if hasattr(user, 'profile') and user.profile.role == required_role:
                return view_func(request, *args, **kwargs)
                
            return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator
