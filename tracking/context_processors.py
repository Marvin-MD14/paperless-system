from .models import UserProfile, Document

def global_counts(request):
    counts = {
        'pending_requests_count': 0,
        'unread_received_count': 0
    }
    
    if request.user.is_authenticated:
        # 1. Registration Requests (Admin only)
        if request.user.is_superuser:
            counts['pending_requests_count'] = UserProfile.objects.filter(
                is_approved=False, 
                user__is_active=False
            ).count()
        
        # 2. Received Documents (All users)
        # Gagamit ng is_read=False para sa real-time notification badge
        counts['unread_received_count'] = Document.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        
    return counts