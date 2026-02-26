import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Document, UserProfile, Routing 
from .choices import OFFICE_CHOICES

@login_required
def received_docs_view(request):
    """
    View para sa full list ng lahat ng natanggap na dokumento.
    Ito ang target ng 'View All' link sa dashboard.
    """
    received_docs = Document.objects.filter(recipient=request.user).order_by('-uploaded_at')
    return render(request, 'all_documents.html', {
        'received_docs': received_docs,
        'title': 'Received Documents'
    })

@login_required
def send_document(request):
    """
    Logic para sa pagpapadala ng existing document sa ibang staff.
    """
    if request.method == "POST":
        doc_id = request.POST.get('document_id')
        recipient_id = request.POST.get('recipient_id')

        if not doc_id or not recipient_id:
            messages.error(request, "Missing document or recipient information.")
            return redirect('upload_document')

        try:
            document = get_object_or_404(Document, id=doc_id)
            recipient_user = get_object_or_404(User, id=recipient_id)
            
            sender_profile = getattr(request.user, 'userprofile', None)
            recipient_profile = getattr(recipient_user, 'userprofile', None)

            if not sender_profile or not recipient_profile:
                messages.error(request, "Cannot send: Either sender or recipient is missing a User Profile.")
                return redirect('upload_document')

            # Update Document status
            document.recipient = recipient_user
            document.is_read = False  
            document.status = 'FOR_REVIEW'
            document.save()

            # Create Routing record
            Routing.objects.create(
                document=document,
                from_office=sender_profile.office,
                to_office=recipient_profile.office,
                notes=f"Document forwarded by {request.user.get_full_name() or request.user.username}",
                status='FOR_REVIEW'
            )

            # Gmail Notification
            if recipient_user.email:
                try:
                    subject = f"🔔 Document Forwarded: {document.title}"
                    body = (
                        f"Hello {recipient_user.get_full_name() or recipient_user.username},\n\n"
                        f"A document has been forwarded to you.\n"
                        f"- Title: {document.title}\n"
                        f"- From: {request.user.username}\n\n"
                        f"Please check your dashboard."
                    )
                    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient_user.email], fail_silently=True)
                except Exception as email_err:
                    print(f"Email failed: {email_err}")

            messages.success(request, f"Document successfully sent to {recipient_user.username}!")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return redirect('upload_document')

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
                # Pag-save ng bagong dokumento
                new_doc = Document.objects.create(
                    title=title if title else file.name,
                    category=category,
                    description=description,
                    file=file,
                    uploaded_by=request.user,
                    status='PENDING'
                )

                # Kung may piniling recipient habang nag-uupload
                if recipient_id:
                    recipient_user = get_object_or_404(User, id=recipient_id)
                    recipient_profile = getattr(recipient_user, 'userprofile', None)
                    sender_profile = getattr(request.user, 'userprofile', None)

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

                # AJAX Response para sa smooth UI update
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'doc_id': new_doc.id,
                        'title': new_doc.title,
                        'category': new_doc.category,
                        'file_url': new_doc.file.url,
                        'file_size': f"{(new_doc.file.size / 1024):.1f} KB",
                        'date': new_doc.uploaded_at.strftime('%b %d, %Y'),
                        # Isama ang updated counts para sa AJAX update sa cards
                        'word_count': Document.objects.filter(uploaded_by=request.user, category='word').count(),
                        'excel_count': Document.objects.filter(uploaded_by=request.user, category='excel').count(),
                        'ppt_count': Document.objects.filter(uploaded_by=request.user, category='ppt').count(),
                        'pdf_count': Document.objects.filter(uploaded_by=request.user, category='pdf').count(),
                    })

                messages.success(request, "Document uploaded successfully!")
                return redirect('upload_document')
            except Exception as e:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
                messages.error(request, f"Upload error: {str(e)}")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'No file selected'}, status=400)
            messages.error(request, "Please select a file.")

    # Data para sa Dashboard/Upload Page
    my_uploads = Document.objects.filter(uploaded_by=request.user)
    received_all = Document.objects.filter(recipient=request.user)
    
    # Search functionality
    query = request.GET.get('q', '')
    documents_list = my_uploads.order_by('-uploaded_at')
    if query:
        documents_list = documents_list.filter(Q(title__icontains=query))

    # Listahan ng unread docs (max 8 para sa sidebar/list)
    unread_docs_list = received_all.filter(is_read=False).order_by('-uploaded_at')[:8]
    
    # Staff users para sa forwarding dropdown (exclude self)
    staff_users = UserProfile.objects.filter(role='STAFF').select_related('user', 'office').exclude(user=request.user)
    
    context = {
        # Dynamic Counters para sa Flex Cards
        'word_count': my_uploads.filter(category='word').count(),
        'excel_count': my_uploads.filter(category='excel').count(),
        'ppt_count': my_uploads.filter(category='ppt').count(),
        'pdf_count': my_uploads.filter(category='pdf').count(),
        
        'recent_logs': documents_list, 
        'unread_docs': unread_docs_list, 
        'staff_users': staff_users,
        'unread_received_count': received_all.filter(is_read=False).count(),
        'received_count': received_all.count(),
        'office_choices': OFFICE_CHOICES,
    }
    return render(request, 'upload_document.html', context)


@login_required
def delete_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, uploaded_by=request.user)
    try:
        # Siguraduhing mabubura pati ang physical file sa storage
        if document.file and os.path.isfile(document.file.path):
            os.remove(document.file.path)
        document.delete()
        messages.success(request, "Document deleted.")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('upload_document')

@login_required
def all_documents(request):
    """
    View para sa pag-display ng lahat ng uploads at natanggap na docs sa iisang page.
    """
    my_uploads = Document.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    received_docs = Document.objects.filter(recipient=request.user).order_by('-uploaded_at')
    return render(request, 'all_documents.html', {
        'my_uploads': my_uploads, 
        'received_docs': received_docs
    })

@login_required
def sent_documents_status(request):
    
    sent_docs = Document.objects.filter(
        uploaded_by=request.user
    ).exclude(recipient__isnull=True).order_by('-uploaded_at')
    return render(request, 'sent_status.html', {'sent_docs': sent_docs})

@login_required
def mark_as_read(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, recipient=request.user)
    if not document.is_read:
        document.is_read = True
        document.save()
    return redirect(document.file.url)