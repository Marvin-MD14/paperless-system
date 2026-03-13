import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.timesince import timesince 
from django.views.decorators.http import require_POST
from .models import Document, Notification
from .models import Document, UserProfile, Routing 
from .choices import OFFICE_CHOICES

# ==========================================
# 1. NOTIFICATION SYSTEM (BELL ICON)
# ==========================================

@login_required
def get_notifications_api(request):
    """
    API for Notification Bell: Shows Received Docs AND Status Updates (Approved/Rejected)
    """
    # 1. Docs na pinadala sa kanya (Inbox)
    inbox = Document.objects.filter(recipient=request.user)
    # 2. Sarili niyang uploads na may update na (Approved/Rejected)
    status_updates = Document.objects.filter(uploaded_by=request.user).filter(Q(status='APPROVED') | Q(status='REJECTED'))
    
    # Combine and Sort
    all_notifs = (inbox | status_updates).distinct().order_by('-uploaded_at')
    unread_count = all_notifs.filter(is_read=False).count()
    
    notifications_data = []
    for ntf in all_notifs[:5]:
        # Determine Label/Icon base sa kung siya ang uploader o recipient
        if ntf.uploaded_by == request.user:
            icon = "✅" if ntf.status == "APPROVED" else "❌"
            msg = f"{icon} Your doc '{ntf.title}' was {ntf.status.lower()}"
            sender = "System Update"
        else:
            msg = f"📩 New doc: {ntf.title}"
            sender = ntf.uploaded_by.username

        notifications_data.append({
            'id': ntf.id,
            'title': msg,
            'sender': sender,
            'file_url': ntf.file.url,
            'is_read': ntf.is_read,
            'time_ago': timesince(ntf.uploaded_at) + " ago"
        })
        
    return JsonResponse({'unread_count': unread_count, 'notifications': notifications_data})

@login_required
@require_POST
def mark_as_read_api(request, ntf_id):
    document = get_object_or_404(Document, Q(id=ntf_id) & (Q(recipient=request.user) | Q(uploaded_by=request.user)))
    
    # ALISIN O I-COMMENT ITO:
    # if document.recipient == request.user and document.status in ['PENDING', 'FOR_REVIEW']:
    #     document.status = 'RECEIVED'
        
    if not document.is_read:
        document.is_read = True
        document.save() # Siguraduhing naka-save
        
    return JsonResponse({'status': 'success', 'new_status': document.status})

# ==========================================
# 2. DASHBOARD LOGIC
# ==========================================

@login_required
def employee_dashboard(request):
    """
    Dashboard View: Naglalaman ng counters para sa Approved at Returned.
    """
    my_uploads = Document.objects.filter(uploaded_by=request.user)
    received_all = Document.objects.filter(recipient=request.user)
    
    # Counters base sa status ng sariling uploads
    approved_count = my_uploads.filter(status='APPROVED').count()
    returned_count = my_uploads.filter(status='REJECTED').count()
    
    context = {
        'recent_logs': my_uploads.order_by('-uploaded_at'),
        'total_uploads': my_uploads.count(),
        'processed_count': approved_count,  # Mapping para sa Green Card
        'returned_count': returned_count,    # Mapping para sa Red Card
        'unread_received_count': received_all.filter(is_read=False).count(),
        
        # Data para sa Morris Charts
        'word_count': my_uploads.filter(category='word').count(),
        'excel_count': my_uploads.filter(category='excel').count(),
        'ppt_count': my_uploads.filter(category='ppt').count(),
        'pdf_count': my_uploads.filter(category='pdf').count(),
        
        'unread_docs': received_all.filter(is_read=False).order_by('-uploaded_at')[:5],
    }
    return render(request, 'employee_dashboard.html', context)

# ==========================================
# 3. APPROVE & REJECT (WITH GMAIL NOTIF)
# ==========================================
@login_required
@require_POST
def approve_document_api(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, recipient=request.user)
    
    # Kunin ang remarks mula sa POST (galing sa SweetAlert modal)
    remarks = request.POST.get('remarks', 'Document approved and is now on process.')

    # 1. Update Document
    document.status = 'APPROVED'
    document.remarks = remarks  # Dito na ise-save ang message
    document.save()

    # 2. In-App Notification
    Notification.objects.create(
        user=document.uploaded_by,
        sender=request.user,
        document=document,
        message=f"APPROVED: '{document.title}'. Note: {remarks}",
        notification_type='APPROVE'
    )

    # 3. Gmail Notification para sa Approval
    uploader = document.uploaded_by
    if uploader.email:
        try:
            subject = f"✅ Document Approved: {document.title}"
            body = (
                f"Hi {uploader.get_full_name() or uploader.username},\n\n"
                f"Your document '{document.title}' has been APPROVED by {request.user.username}.\n\n"
                f"FEEDBACK/REMARKS: {remarks}\n\n"
                f"You can view this in your dashboard: {request.build_absolute_uri('/')}\n\n"
                f"Regards,\nERDMS System"
            )
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [uploader.email], fail_silently=True)
        except Exception as e:
            print(f"Gmail Error: {e}")

    return JsonResponse({"status": "success"})


@login_required
@require_POST
def reject_document_api(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, recipient=request.user)
    
    # Kunin ang reason (reason ang key name sa JS mo kadalasan sa rejection)
    rejection_reason = request.POST.get('reason', 'No reason provided.')

    # 1. Update Document
    document.status = 'REJECTED'
    document.remarks = rejection_reason # I-save ang reason sa remarks field
    document.is_read = False 
    document.save()

    # 2. In-App Notification
    Notification.objects.create(
        user=document.uploaded_by,
        sender=request.user,
        document=document,
        message=f"REJECTED: '{document.title}'. Reason: {rejection_reason}",
        notification_type='REJECT'
    )

    # 3. Gmail Notification para sa Rejection
    uploader = document.uploaded_by
    if uploader.email:
        try:
            subject = f"❌ Document Rejected: {document.title}"
            body = (
                f"Hi {uploader.get_full_name() or uploader.username},\n\n"
                f"Your document '{document.title}' was REJECTED by {request.user.username}.\n\n"
                f"REASON: {rejection_reason}\n\n"
                f"Please check the document and re-upload if necessary.\n\n"
                f"Regards,\nERDMS System"
            )
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [uploader.email], fail_silently=True)
        except Exception as e:
            print(f"Gmail Error: {e}")

    return JsonResponse({"status": "success"})
# ==========================================
# 4. DOCUMENT OPERATIONS (UPLOAD, SEND, DELETE)
# ==========================================

@login_required
def upload_document(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        file = request.FILES.get('file')
        recipient_id = request.POST.get('recipient_id')

        if file:
            try:
                new_doc = Document.objects.create(
                    title=title if title else file.name,
                    category=category,
                    description=description,
                    file=file,
                    uploaded_by=request.user,
                    status='PENDING'
                )

                if recipient_id:
                    recipient_user = get_object_or_404(User, id=recipient_id)
                    sender_profile = getattr(request.user, 'userprofile', None)
                    recipient_profile = getattr(recipient_user, 'userprofile', None)

                    new_doc.recipient = recipient_user
                    new_doc.is_read = False
                    new_doc.status = 'FOR_REVIEW'
                    new_doc.save()

                    Routing.objects.create(
                        document=new_doc,
                        from_office=sender_profile.office if sender_profile else None,
                        to_office=recipient_profile.office if recipient_profile else None,
                        notes="Initial upload and share.",
                        status='FOR_REVIEW'
                    )

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'doc_id': new_doc.id})

                messages.success(request, "Document uploaded successfully!")
                return redirect('upload_document')
            except Exception as e:
                messages.error(request, f"Upload error: {str(e)}")
        else:
            messages.error(request, "Please select a file.")

    # Data para sa GET request
    my_uploads = Document.objects.filter(uploaded_by=request.user)
    received_all = Document.objects.filter(recipient=request.user)
    staff_users = UserProfile.objects.filter(role='STAFF').select_related('user', 'office').exclude(user=request.user)
    
    context = {
        'word_count': my_uploads.filter(category='word').count(),
        'excel_count': my_uploads.filter(category='excel').count(),
        'ppt_count': my_uploads.filter(category='ppt').count(),
        'pdf_count': my_uploads.filter(category='pdf').count(),
        'recent_logs': my_uploads.order_by('-uploaded_at'), 
        'unread_docs': received_all.filter(is_read=False).order_by('-uploaded_at')[:8], 
        'staff_users': staff_users,
        'unread_received_count': received_all.filter(is_read=False).count(),
        'received_count': received_all.count(),
        'office_choices': OFFICE_CHOICES,
    }
    return render(request, 'upload_document.html', context)

@login_required
def send_document(request):
    if request.method == "POST":
        doc_id = request.POST.get('document_id')
        recipient_id = request.POST.get('recipient_id')

        try:
            document = get_object_or_404(Document, id=doc_id)
            recipient_user = get_object_or_404(User, id=recipient_id)
            sender_profile = getattr(request.user, 'userprofile', None)
            recipient_profile = getattr(recipient_user, 'userprofile', None)

            document.recipient = recipient_user
            document.is_read = False  
            document.status = 'FOR_REVIEW'
            document.save()

            Routing.objects.create(
                document=document,
                from_office=sender_profile.office if sender_profile else None,
                to_office=recipient_profile.office if recipient_profile else None,
                notes=f"Document forwarded by {request.user.username}",
                status='FOR_REVIEW'
            )

            # Gmail Notification for Forwarding
            if recipient_user.email:
                send_mail(
                    f"🔔 Document Forwarded: {document.title}",
                    f"Hi {recipient_user.username}, a document has been forwarded to you by {request.user.username}.",
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_user.email],
                    fail_silently=True
                )

            messages.success(request, f"Document sent to {recipient_user.username}!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    return redirect('upload_document')

@login_required
def delete_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, uploaded_by=request.user)
    if document.file and os.path.isfile(document.file.path):
        os.remove(document.file.path)
    document.delete()
    messages.success(request, "Document deleted.")
    return redirect('upload_document')

# ==========================================
# 5. LIST VIEWS
# ==========================================

@login_required
def my_uploads_view(request):
    my_documents = Document.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    query = request.GET.get('q', '')
    if query:
        my_documents = my_documents.filter(Q(title__icontains=query))
    return render(request, 'my_uploads.html', {'my_documents': my_documents, 'title': 'My Uploads'})

@login_required
def received_docs_view(request):
    received_docs = Document.objects.filter(recipient=request.user).order_by('-uploaded_at')
    return render(request, 'all_documents.html', {'received_documents': received_docs, 'title': 'Received'})

@login_required
def all_documents(request):
    my_uploads = Document.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    received_docs = Document.objects.filter(recipient=request.user).order_by('-uploaded_at')
    return render(request, 'all_documents.html', {'my_uploads': my_uploads, 'received_docs': received_docs})

@login_required
def sent_documents_status(request):
    sent_docs = Document.objects.filter(uploaded_by=request.user).exclude(recipient__isnull=True).order_by('-uploaded_at')
    return render(request, 'sent_status.html', {'sent_docs': sent_docs})

@login_required
def mark_as_read(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, recipient=request.user)
    if not document.is_read:
        document.is_read = True
        document.save()
    return redirect(document.file.url)
@login_required
def view_sent_documents(request):
    sent_docs = Document.objects.filter(
        uploaded_by=request.user
    ).exclude(recipient__isnull=True).order_by('-uploaded_at')

    context = {
        'sent_docs': sent_docs,
    }
    # ALISIN ANG "documents/" DITO:
    return render(request, 'sent_documents.html', context)

@login_required
@require_POST
def receive_document_api(request, doc_id):
    """
    API endpoint para i-mark ang document as RECEIVED.
    Ito ay indicator na nakita na ng recipient ang file pero hindi pa Final Decision.
    """
    document = get_object_or_404(Document, id=doc_id, recipient=request.user)
    
    # 1. Update Status to RECEIVED
    # Siguraduhin na 'RECEIVED' ay valid choice sa models.py mo
    document.status = 'RECEIVED'
    document.is_read = True # Matic na read na rin ito
    document.save()

    # 2. In-App Notification para sa uploader
    Notification.objects.create(
        user=document.uploaded_by,
        sender=request.user,
        document=document,
        message=f"RECEIVED: '{document.title}' is now being reviewed by {request.user.username}.",
        notification_type='INFO' # Or any type you use for status updates
    )

    # 3. (Optional) Gmail Notification
    uploader = document.uploaded_by
    if uploader.email:
        try:
            subject = f"📥 Document Received: {document.title}"
            body = (
                f"Hi {uploader.username},\n\n"
                f"Your document '{document.title}' has been RECEIVED by {request.user.username}.\n"
                f"Status: Under Review.\n\n"
                f"ERDMS System"
            )
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [uploader.email], fail_silently=True)
        except Exception as e:
            print(f"Gmail Error: {e}")

    return JsonResponse({"status": "success", "message": "Document marked as received."})