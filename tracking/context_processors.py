from .models import UserProfile, Document

def global_counts(request):
    counts = {
        'pending_requests_count': 0,
        'unread_received_count': 0,
        'unread_notifications': [] # Idagdag ito
    }
    
    if request.user.is_authenticated:
        # 1. Registration Requests (Admin only)
        if request.user.is_superuser:
            counts['pending_requests_count'] = UserProfile.objects.filter(
                is_approved=False, 
                user__is_active=False
            ).count()
        
        # 2. Received Documents (All users)
        unread_docs = Document.objects.filter(
            recipient=request.user,
            is_read=False
        ).order_by('-uploaded_at') # Pinakabago ang nasa taas
        
        counts['unread_received_count'] = unread_docs.count()
        counts['unread_notifications'] = unread_docs[:5] # Kunin lang ang top 5 para sa dropdown
        
    return counts