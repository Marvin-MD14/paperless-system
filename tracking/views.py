import os
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Q, Sum
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator

from .models import Office, UserProfile, Document
from .choices import OFFICE_CHOICES, REGISTRATION_TYPES


def authenticate_by_email(email, password):
    """Authenticate user using email instead of username."""
    try:
        user_obj = User.objects.get(email=email)
        user = authenticate(username=user_obj.username, password=password)
        return user
    except User.DoesNotExist:
        return None

@never_cache
def login(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == "POST":
        login_input = request.POST.get('username', '').strip() 
        password = request.POST.get('password', '').strip()
        remember_me = request.POST.get('remember_me')
        user = None
        
        if '@' in login_input:
            try:
                user_obj = User.objects.get(email=login_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is None:
            user = authenticate(request, username=login_input, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)

                if remember_me:
                    request.session.set_expiry(1209600) 
                else:
                    request.session.set_expiry(0) 

                messages.success(request, f"Welcome back, {user.first_name if user.first_name else user.username}!")
                return redirect_by_role(user)
            else:
                messages.error(request, "Your account is inactive. Please contact the administrator.")
        else:
            messages.error(request, "Invalid credentials. Please check your email/username and password.")

    return render(request, 'login.html')

def redirect_by_role(user):
   
    if user.is_superuser:
        return redirect('admin_dashboard')


    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'STAFF'} 
    )

    role = profile.role
    
    if role == 'HEAD':
        return redirect('head_dashboard')
    
    elif role in ['GOVERNOR', 'EXECUTIVE']:
        return redirect('executive_dashboard')
    
    elif role == 'STAFF':
        return redirect('user_dashboard')
    
    return redirect('user_dashboard')

@never_cache
def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate_by_email(email, password)

        if user is not None:
            if user.is_superuser:
                auth_login(request, user)

                if remember_me:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)

                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. Not an administrator.")
        else:
            messages.error(request, "Invalid admin credentials.")

    return render(request, 'admin_login.html')


@never_cache
def head_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate_by_email(email, password)

        if user is not None:
      
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'HEAD'}
            )

            if profile.role == 'HEAD':
                auth_login(request, user)

                if remember_me:
                    request.session.set_expiry(1209600) 
                else:
                    request.session.set_expiry(0) 

                return redirect('head_dashboard')
            else:
                messages.error(request, "Access Denied: Account is not an Office Head.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'head_login.html')

@login_required
@never_cache
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')

    profiles = UserProfile.objects.filter(
        is_approved=True, 
        user__is_active=True  
    ).select_related('user', 'office').order_by('-user__date_joined')

    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        role = request.POST.get('role')
        office_id = request.POST.get('office_id') 
        password = request.POST.get('password', 'DefaultPassword123!') 

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Error: The username {username} is already taken.")
            return redirect('admin_dashboard')

        try:
            new_user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=True  
            )

            office_obj = Office.objects.filter(id=office_id).first()

            UserProfile.objects.update_or_create(
                user=new_user,
                defaults={
                    'office': office_obj,
                    'role': role,
                    'is_approved': True,
                    'registration_type': 'ADMIN',
                    'approved_by': request.user,
                    'approved_at': timezone.now()
                }
            )

            messages.success(request, f"Successfully created account for {first_name} {last_name}!")
            return redirect('admin_dashboard')

        except Exception as e:
            messages.error(request, f"System Error: {str(e)}")
            return redirect('admin_dashboard')

    
    from .models import OFFICE_CHOICES 
    offices = Office.objects.all() 

    context = {
        'offices': offices, 
        'profiles': profiles,
        'governor_count': UserProfile.objects.filter(role='GOVERNOR', is_approved=True, user__is_active=True).count(),
        'heads_count': UserProfile.objects.filter(role='HEAD', is_approved=True, user__is_active=True).count(),
        'executive_count': UserProfile.objects.filter(role='EXECUTIVE', is_approved=True, user__is_active=True).count(),
        'staff_count': UserProfile.objects.filter(role='STAFF', is_approved=True, user__is_active=True).count(),
    }

    return render(request, 'admin_dashboard.html', context)
@login_required
@never_cache
def head_dashboard(request):
    if request.user.userprofile.role != 'HEAD':
        messages.error(request, "Unauthorized access. This page is for Department Heads only.")
        return redirect('login')

    # 1. Get Head Profile and Office
    profile = request.user.userprofile
    current_office = profile.office
    office_name = current_office.office_name if current_office else "No Office Assigned"

    # 2. Staff Management
    my_staff = UserProfile.objects.filter(
        office=current_office,
        role='STAFF',
        is_approved=True,
        user__is_active=True
    ).select_related('user').order_by('user__first_name')

    pending_staff_count = UserProfile.objects.filter(
        office=current_office,
        role='STAFF',
        is_approved=False
    ).count()

    # 3. Document Logic (Base sa Routings ng Office)
    # Kinukuha ang lahat ng docs na dumaan sa office na ito
    office_docs = Document.objects.filter(
        routings__to_office=current_office
    ).distinct()

    # 4. Actionable Logic for Head
    # Ang "Pending Review" ay ang mga docs na status ay 'RECEIVED' (naka-confirm na ng staff)
    pending_review = office_docs.filter(status='RECEIVED')

    # 5. Prepare Context for Dashboard
    context = {
        'profile': profile,
        'office_name': office_name, 
        'my_staff': my_staff,
        'office_docs': office_docs,
        
        # Stats for Cards
        'total_staff': my_staff.count(),
        'pending_staff_count': pending_staff_count,
        'unread_received_count': pending_review.count(), # Docs waiting for Head's action
        'total_approved': office_docs.filter(status='APPROVED').count(),
        'returned_rejected': office_docs.filter(Q(status='RETURNED') | Q(status='REJECTED')).count(),
        
        # File Type Distribution (Morris Charts)
        'word_count': office_docs.filter(category__iexact='word').count(),
        'excel_count': office_docs.filter(category__iexact='excel').count(),
        'ppt_count': office_docs.filter(category__iexact='ppt').count(),
        'pdf_count': office_docs.filter(category__iexact='pdf').count(),
        
        # Recent Activities
        'recent_docs': office_docs.order_by('-uploaded_at')[:5],
        'pending_review_list': pending_review.order_by('-uploaded_at')[:5],
    }

    return render(request, 'head_dashboard.html', context)
@login_required
def my_department_staff(request):
    """Pinapakita ang lahat ng active/approved staff ng office na ito"""
    if request.user.userprofile.role != 'HEAD':
        return redirect('login')

    staff_members = UserProfile.objects.filter(
        office=request.user.userprofile.office,
        role='STAFF',
        is_approved=True
    ).select_related('user').order_by('user__first_name')

    return render(request, 'my_department_staff.html', {'staff_members': staff_members})
@login_required
def pending_staff_approvals(request):
    """View para sa Head para makita ang mga staff na nag-register sa office nila"""
    if request.user.userprofile.role != 'HEAD':
        messages.error(request, "Unauthorized access.")
        return redirect('login')

    # Kunin ang mga staff sa kaparehong office na hindi pa approved
    pending_staff = UserProfile.objects.filter(
        office=request.user.userprofile.office,
        role='STAFF',
        is_approved=False
    ).select_related('user').order_by('-user__date_joined')

    return render(request, 'pending_staff.html', {'pending_staff': pending_staff})

@login_required
def approve_staff(request, user_profile_id):
    """Function para i-approve ang staff registration"""
    if request.user.userprofile.role != 'HEAD':
        messages.error(request, "Unauthorized action.")
        return redirect('head_dashboard')

    staff_profile = get_object_or_404(UserProfile, id=user_profile_id, office=request.user.userprofile.office)
    
    staff_profile.is_approved = True
    staff_profile.save()
    
    # I-activate ang login access
    staff_profile.user.is_active = True
    staff_profile.user.save()

    messages.success(request, f"Staff {staff_profile.user.get_full_name()} has been approved.")
    return redirect('pending_staff_approvals')

@login_required
def reject_staff(request, user_profile_id):
    """Function para i-reject at i-delete ang maling registration"""
    if request.user.userprofile.role != 'HEAD':
        messages.error(request, "Unauthorized action.")
        return redirect('head_dashboard')

    staff_profile = get_object_or_404(UserProfile, id=user_profile_id, office=request.user.userprofile.office)
    user = staff_profile.user
    
    # Burahin ang profile at ang user account
    user.delete() 

    messages.warning(request, "Registration has been rejected and the account was deleted.")
    return redirect('pending_staff_approvals')
@login_required
def approve_staff(request, user_profile_id):
    # Siguraduhin na Head ang nag-aaksyon
    if request.user.userprofile.role != 'HEAD':
        messages.error(request, "Unauthorized action.")
        return redirect('head_dashboard')

    # Hanapin ang profile ng staff na i-aapprove sa kaparehong office
    staff_profile = get_object_or_404(
        UserProfile, 
        id=user_profile_id, 
        office=request.user.userprofile.office
    )
    
    staff_profile.is_approved = True
    staff_profile.save()
    
    # Siguraduhin na pwede na siyang mag-login
    staff_profile.user.is_active = True
    staff_profile.user.save()

    messages.success(request, f"User {staff_profile.user.get_full_name()} has been approved successfully.")
    return redirect('pending_staff_approvals') # I-redirect sa listahan ng approvals
@login_required
@never_cache
def user_dashboard(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'STAFF'} 
    )

   
    if profile.role == 'HEAD':
        return redirect('head_dashboard')
    elif profile.role in ['GOVERNOR', 'EXECUTIVE']:
        return redirect('executive_dashboard')
    all_uploads = Document.objects.filter(uploaded_by=request.user)
    received_all = Document.objects.filter(recipient=request.user)
    total_bytes = 0
    for doc in all_uploads:
        try:
            if doc.file and os.path.exists(doc.file.path):
                total_bytes += doc.file.size
        except (ValueError, FileNotFoundError):
            continue
            
    total_size_mb = round(total_bytes / (1024 * 1024), 2)
    storage_limit = 100
    while total_size_mb >= storage_limit:
        storage_limit += 100
    
    storage_percentage = (total_size_mb / storage_limit) * 100

  
    context = {
        'profile': profile,
        'total_uploads': all_uploads.count(),
        'processed_count': all_uploads.filter(status__iexact='APPROVED').count(),
        'returned_count': all_uploads.filter(status__iexact='REJECTED').count(),
        'unread_received_count': received_all.filter(is_read=False).count(),
        'total_size_mb': total_size_mb, 
        'storage_limit': storage_limit,
        'storage_percentage': storage_percentage,
        'word_count': all_uploads.filter(category__iexact='word').count(),
        'excel_count': all_uploads.filter(category__iexact='excel').count(),
        'ppt_count': all_uploads.filter(category__iexact='ppt').count(),
        'pdf_count': all_uploads.filter(category__iexact='pdf').count(),
        'unread_docs': received_all.filter(is_read=False).order_by('-uploaded_at')[:5],
    }

    return render(request, 'employee_dashboard.html', context)
def register(request):
   
    if request.user.is_authenticated:
        return redirect('dashboard') 

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('username', '').strip()
        password = request.POST.get('pwd')
        confirm_password = request.POST.get('cpwd')
        office_code = request.POST.get('office') 

        if not all([full_name, email, password, office_code]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered. Please use another or login.")
            return redirect('register')

        try:
            with transaction.atomic():
                name_parts = full_name.split(' ', 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ""

           
                office_name_display = dict(OFFICE_CHOICES).get(office_code, office_code)
                office, created = Office.objects.get_or_create(
                    office_code=office_code,
                    defaults={'office_name': office_name_display}
                )

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=False  
                )
                
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'office': office,
                        'role': 'STAFF',
                        'registration_type': 'SELF',
                        'is_approved': False
                    }
                )

            messages.success(request, "Registration successful! Please wait for administrative approval.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('register')
            

    context = {
        'offices': OFFICE_CHOICES
    }
    return render(request, 'register.html', context)
def logout(request):
    auth_logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass  

    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
@user_passes_test(lambda u: u.is_superuser)
@never_cache
def user_management(request):
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')

    profiles = UserProfile.objects.all().select_related('user', 'office').order_by('-user__date_joined')

    if search_query:
        profiles = profiles.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(office__office_name__icontains=search_query)
        )

    if role_filter:
        profiles = profiles.filter(role=role_filter)

    if request.method == "POST":
        try:
            with transaction.atomic():
                username = request.POST.get('username')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                password = request.POST.get('password')
                role = request.POST.get('role')
                office_code = request.POST.get('office_id')

             
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    is_active=True
                )

           
                office = None
                if office_code:
                    office_name_display = dict(OFFICE_CHOICES).get(office_code, office_code)
                    
                    office, created = Office.objects.get_or_create(
                        office_code=office_code,
                        defaults={'office_name': office_name_display}
                    )

                UserProfile.objects.create(
                    user=user,
                    office=office,
                    role=role,
                    is_approved=True,
                    registration_type='ADMIN'
                )

                messages.success(request, f"Account for {username} created successfully!")
                return redirect('user_management')
                
        except Exception as e:
            messages.error(request, f"Registration Failed: {str(e)}")

    context = {
        'profiles': profiles,
        'offices': OFFICE_CHOICES, 
        'search_query': search_query,
        'role_filter': role_filter,
    }
    return render(request, 'user_management.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if user_to_delete.is_superuser:
        messages.error(request, "Cannot delete a superuser.")
    else:
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"User {username} has been deleted.")
    return redirect('user_management')
@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_details(request, user_id):
    userprofile = get_object_or_404(UserProfile.objects.select_related('user', 'office'), id=user_id)
    
    documents_created = 0
    if hasattr(userprofile.user, 'uploaded_documents'):
        documents_created = userprofile.user.uploaded_documents.count()
    
    context = {
        'profile': userprofile,
        'documents_count': documents_created,
    }
    return render(request, 'user_details_partial.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    userprofile = get_object_or_404(UserProfile.objects.select_related('user'), id=user_id)
    user = userprofile.user
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                user.username = request.POST.get('username', user.username)
                user.email = request.POST.get('email', user.email)
                user.first_name = request.POST.get('first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.is_active = request.POST.get('is_active') == 'on'
                
                new_password = request.POST.get('new_password')
                if new_password:
                    user.set_password(new_password)
                
                user.save()
                
             
                office_id = request.POST.get('office')
                if office_id:
                    userprofile.office = get_object_or_404(Office, id=office_id)
                else:
                    userprofile.office = None
                
                userprofile.role = request.POST.get('role', userprofile.role)
                userprofile.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True, 
                        'message': f'User {user.username} updated successfully!'
                    })
                
                messages.success(request, f'User {user.username} updated successfully!')
                return redirect('user_management')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)}, status=400)
            messages.error(request, f"Error updating user: {str(e)}")
    
  
    offices = Office.objects.all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        office_options = "".join([
            f'<option value="{o.id}" {"selected" if userprofile.office and userprofile.office.id == o.id else ""}>{o.office_name} ({o.office_code})</option>' 
            for o in offices
        ])
        
        html = f'''
        <form method="POST" action="/edit-user/{user_id}/" id="editUserForm">
            <input type="hidden" name="csrfmiddlewaretoken" value="{request.COOKIES.get('csrftoken', '')}">
            <div class="modal-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="fw-bold">Username <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" name="username" value="{user.username}" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="fw-bold">Email</label>
                            <input type="email" class="form-control" name="email" value="{user.email or ''}">
                        </div>
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="fw-bold">First Name</label>
                            <input type="text" class="form-control" name="first_name" value="{user.first_name or ''}">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="fw-bold">Last Name</label>
                            <input type="text" class="form-control" name="last_name" value="{user.last_name or ''}">
                        </div>
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="fw-bold">New Password</label>
                            <input type="password" class="form-control" name="new_password" placeholder="Leave blank to keep">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="fw-bold">Office</label>
                            <select class="form-control" name="office">
                                <option value="">Select Office</option>
                                {office_options}
                            </select>
                        </div>
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="fw-bold">Role</label>
                            <select class="form-control" name="role" required>
                                <option value="STAFF" {"selected" if userprofile.role == 'STAFF' else ""}>Staff</option>
                                <option value="HEAD" {"selected" if userprofile.role == 'HEAD' else ""}>Office Head</option>
                                <option value="EXECUTIVE" {"selected" if userprofile.role == 'EXECUTIVE' else ""}>Executive</option>
                                <option value="GOVERNOR" {"selected" if userprofile.role == 'GOVERNOR' else ""}>Governor</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-6 d-flex align-items-center mt-4">
                        <div class="custom-control custom-switch">
                            <input type="checkbox" class="custom-control-input" id="is_active" name="is_active" {"checked" if user.is_active else ""}>
                            <label class="custom-control-label" for="is_active">Active Account</label>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
        </form>
        '''
        return HttpResponse(html)
    
    return redirect('user_management')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def access_requests(request):
    pending_requests = UserProfile.objects.filter(
        registration_type='SELF',  
        is_approved=False,
        user__is_active=False
    ).select_related('user', 'office').order_by('-user__date_joined')
    
    approved_users = UserProfile.objects.filter(
        registration_type='SELF',  
        is_approved=True
    ).select_related('user', 'office').order_by('-approved_at')[:20]
    
    rejected_users = UserProfile.objects.filter(
        registration_type='SELF',  
        is_approved=False,
        user__is_active=False
    ).exclude(user__date_joined=timezone.now())[:10]
    
    context = {
        'pending_requests': pending_requests,
        'approved_users': approved_users,
        'rejected_users': rejected_users,
        'pending_count': pending_requests.count(),
    }
    return render(request, 'access_requests.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_user(request, profile_id):
    if request.method == 'POST':
        try:
            profile = get_object_or_404(UserProfile, id=profile_id)
            user = profile.user
            
            user.is_active = True
            user.save()
            
            profile.is_approved = True
            profile.approved_at = timezone.now()
            profile.approved_by = request.user
            profile.save()
            
            return JsonResponse({'success': True, 'message': f'User {user.username} approved!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_user(request, profile_id):
    if request.method == 'POST':
        try:
            profile = get_object_or_404(UserProfile, id=profile_id)
            username = profile.user.username
            profile.user.delete() # Burahin ang user object (cascade delete sa profile)
            return JsonResponse({'success': True, 'message': f'User {username} rejected.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def bulk_approve_users(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_ids = data.get('profile_ids', [])
            
            if not profile_ids:
                return JsonResponse({'success': False, 'error': 'No users selected'}, status=400)
            
            profiles = UserProfile.objects.filter(id__in=profile_ids, is_approved=False)
            count = 0
            for profile in profiles:
                user = profile.user
                user.is_active = True
                user.save()
                profile.is_approved = True
                profile.approved_at = timezone.now()
                profile.approved_by = request.user
                profile.save()
                count += 1
            
            return JsonResponse({'success': True, 'message': f'{count} users approved!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)