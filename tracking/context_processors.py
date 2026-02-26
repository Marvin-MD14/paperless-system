from .models import UserProfile

def pending_requests_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        count = UserProfile.objects.filter(is_approved=False, user__is_active=False).count()
        return {'pending_requests_count': count}
    return {'pending_requests_count': 0}