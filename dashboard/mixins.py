from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import AccessMixin

class RoleOrAdminMixin(AccessMixin):
    """Mixin that verifies the user has the required role or is an admin"""
    required_role = None  # Must be set by the view
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        
        # Check if user is admin
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
            
        # Check if user has the required role
        if hasattr(user, 'profile') and user.profile.role == self.required_role:
            return super().dispatch(request, *args, **kwargs)
            
        return self.handle_no_permission()
        
    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to access this page.")
