from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def reset_notifications_count(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.notifications_count = 0
        profile.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)
