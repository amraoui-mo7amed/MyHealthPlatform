from .models.notifications import Notifications
from user_auth.models import UserProfile
def getUserData(request):
    user = request.user
    if user.is_authenticated:
        userProfile = UserProfile.objects.filter(user=user).first()
        role = user.profile.role
        return {
            'user':user,
            'role' : role,
            'user_profile':userProfile,
            'notifications' : Notifications.objects.filter(user=user),
        }
    else:
        return {}