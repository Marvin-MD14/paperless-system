from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Office, UserProfile, Document
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .choices import REGISTRATION_TYPES
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
import json
from .choices import OFFICE_CHOICES
from django.db.models import Sum
import os

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
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  

        user = authenticate_by_email(email, password)

        if user is not None:
            auth_login(request, user)

            if remember_me:
                request.session.set_expiry(1209600)  
            else:
                request.session.set_expiry(0)        

            return redirect_by_role(user)
        else:
            messages.error(request, "Invalid email or password. Please try again.")

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

    offices = Office.objects.all()
    
    profiles = UserProfile.objects.filter(
        is_approved=True, 
        user__is_active=True  
    ).select_related('user', 'office').order_by('-user__date_joined')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name', '')
        role = request.POST.get('role')
        office_id = request.POST.get('office')

        if User.objects.filter(username=email).exists():
            messages.error(request, f"Error: The email {email} is already registered.")
            return redirect('admin_dashboard')

        try:
            parts = full_name.strip().split()
            first_name = parts[0] if parts else ""
            last_name = ' '.join(parts[1:]) if len(parts) > 1 else ""

            new_user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=True  
            )

        
            office_obj = None
            if office_id:
                try:
                    office_obj = Office.objects.get(id=office_id)
                except Office.DoesNotExist:
                    office_obj = None

          
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

            messages.success(request, f"Successfully created {role} account for {full_name}!")
            return redirect('admin_dashboard')

        except Exception as e:
            messages.error(request, f"System Error: {str(e)}")
            return redirect('admin_dashboard')

    context = {
        'offices': offices,
        'offices_list': OFFICE_CHOICES,
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
        messages.error(request, "Unauthorized access.")
        return redirect('login')

    profile = request.user.userprofile
    my_staff = UserProfile.objects.filter(
        office=profile.office
    ).exclude(user=request.user)

    office_docs = Document.objects.filter(
        routings__to_office=profile.office
    ).distinct()

    context = {
        'profile': profile,
        'my_staff': my_staff,
        'office_docs': office_docs,
    }

    return render(request, 'head_dashboard.html', context)


@login_required
@never_cache
def user_dashboard(request):
    # Siguraduhing may profile ang user
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'STAFF'} 
    )

    # Role Redirection
    if profile.role == 'HEAD':
        return redirect('head_dashboard')
    elif profile.role in ['GOVERNOR', 'EXECUTIVE']:
        return redirect('executive_dashboard')

    # DATA FETCHING
    all_uploads = Document.objects.filter(uploaded_by=request.user)
    received_all = Document.objects.filter(recipient=request.user)

    # STORAGE CALCULATION (Manual calculation dahil walang file_size field)
    total_bytes = 0
    for doc in all_uploads:
        try:
            if doc.file and os.path.exists(doc.file.path):
                total_bytes += doc.file.size
        except (ValueError, FileNotFoundError):
            continue
            
    total_size_mb = round(total_bytes / (1024 * 1024), 2)

    # --- DYNAMIC STORAGE LOGIC (Unlimited 100MB Blocks) ---
    storage_limit = 100
    # Habang ang total size ay mas malaki sa limit, dagdag lang ng 100MB
    while total_size_mb >= storage_limit:
        storage_limit += 100
    
    # Kalkulahin ang percentage para sa bar (e.g., 50MB / 100MB = 50%)
    storage_percentage = (total_size_mb / storage_limit) * 100

    context = {
        'profile': profile,
        
        # 1. PARA SA METRIC CARDS
        'recent_logs': all_uploads, 
        'processed_count': all_uploads.filter(status='PROCESSED').count(),
        'unread_received_count': received_all.filter(is_read=False).count(),
        'total_size_mb': total_size_mb, 
        'storage_limit': storage_limit,
        'storage_percentage': storage_percentage,
        
        # 2. PARA SA MORRIS CHARTS
        'word_count': all_uploads.filter(category='word').count(),
        'excel_count': all_uploads.filter(category='excel').count(),
        'ppt_count': all_uploads.filter(category='ppt').count(),
        'pdf_count': all_uploads.filter(category='pdf').count(),
        
        # 3. PARA SA UNREAD DOCUMENTS LIST
        'unread_docs': received_all.filter(is_read=False).order_by('-uploaded_at')[:5],
    }

    return render(request, 'employee_dashboard.html', context)

def register(request):

    
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('pwd')
        full_name = request.POST.get('full_name', '')
        office_code = request.POST.get('office')
        role = 'STAFF'  

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        try:
            
            parts = full_name.strip().split()
            first_name = parts[0] if parts else ""
            last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
            
           
            new_user = User.objects.create_user(
                username=email, 
                email=email, 
                password=password,
                first_name=first_name, 
                last_name=last_name,
                is_active=False  
            )

       
            office_display = dict(OFFICE_CHOICES).get(office_code, office_code)
            office_instance, created = Office.objects.get_or_create(
                office_code=office_code,
                defaults={'office_name': office_display}
            )

        
            UserProfile.objects.create(
                user=new_user,
                office=office_instance,
                role=role,
                is_approved=False,
                registration_type='SELF'
            )

            messages.success(request, (
                "Your registration request has been submitted successfully! "
                "An administrator will review and approve your account within 24-48 hours. "
                "You will receive an email notification once your account is activated."
            ))
            
            return redirect('login') 

        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
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
def user_management(request):
    role_filter = request.GET.get('role', '')
    search_query = request.GET.get('search', '')
    
    userprofiles = UserProfile.objects.filter(
        is_approved=True  
    ).select_related('user', 'office').order_by('-user__date_joined')
    

    if role_filter:
        userprofiles = userprofiles.filter(role=role_filter)
    
    if search_query:
        userprofiles = userprofiles.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(office__office_name__icontains=search_query) |
            Q(office__office_code__icontains=search_query)
        )
    
    governor_count = UserProfile.objects.filter(role='GOVERNOR', is_approved=True).count()
    heads_count = UserProfile.objects.filter(role='HEAD', is_approved=True).count()
    executive_count = UserProfile.objects.filter(role='EXECUTIVE', is_approved=True).count()
    staff_count = UserProfile.objects.filter(role='STAFF', is_approved=True).count()
    
    paginator = Paginator(userprofiles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all offices for dropdown
    offices = Office.objects.all().order_by('office_name')
    
    # You can remove this part or fix it by importing REGISTRATION_TYPES
    # If you want to display registration type, import it from choices
    # from .choices import REGISTRATION_TYPES
    
    context = {
        'userprofiles': page_obj,
        'governor_count': governor_count,
        'heads_count': heads_count,
        'executive_count': executive_count,
        'staff_count': staff_count,
        'offices': offices,
        'role_filter': role_filter,
        'search_query': search_query,
    }
    
    return render(request, 'user_management.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_user(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        office_id = request.POST.get('office')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'on'
        
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('user_management')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken.')
            return redirect('user_management')
        
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=is_active
            )
            
            office = None
            if office_id:
                office = get_object_or_404(Office, id=office_id)
            
            UserProfile.objects.create(
                user=user,
                office=office,
                role=role,
                is_approved=True,  
                registration_type='ADMIN', 
                approved_by=request.user,
                approved_at=timezone.now()
            )
            
            messages.success(request, f'User {username} created successfully!')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return redirect('user_management')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user_profile = get_object_or_404(UserProfile, id=user_id)
            user = user_profile.user
            
            if request.user.id == user.id:
                return JsonResponse({'success': False, 'error': 'You cannot delete your own account!'}, status=400)
            
            username = user.username
            user.delete()  
            return JsonResponse({'success': True, 'message': f'User {username} deleted successfully'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_details(request, user_id):
    userprofile = get_object_or_404(UserProfile.objects.select_related('user', 'office'), id=user_id)
    
    documents_created = userprofile.user.uploaded_documents.count() if hasattr(userprofile.user, 'uploaded_documents') else 0
    
    context = {
        'profile': userprofile,
        'documents_count': documents_created,
    }
    
    return render(request, 'user_details_partial.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    userprofile = get_object_or_404(UserProfile.objects.select_related('user'), id=user_id)
    
    if request.method == 'POST':
        # Update user data
        user = userprofile.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.is_active = request.POST.get('is_active') == 'on'
        
        # Update password if provided
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
    
    offices = Office.objects.all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = f'''
        <form method="POST" action="/edit-user/{user_id}/" id="editUserForm">
            <input type="hidden" name="csrfmiddlewaretoken" value="{request.COOKIES.get('csrftoken', '')}">
            <div class="modal-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="username" class="fw-bold">Username <span class="text-danger">*</span></label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fas fa-user"></i></span>
                                </div>
                                <input type="text" class="form-control" id="username" name="username" value="{userprofile.user.username}" required>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="email" class="fw-bold">Email Address</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                                </div>
                                <input type="email" class="form-control" id="email" name="email" value="{userprofile.user.email or ''}">
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="first_name" class="fw-bold">First Name</label>
                            <input type="text" class="form-control" id="first_name" name="first_name" value="{userprofile.user.first_name or ''}">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="last_name" class="fw-bold">Last Name</label>
                            <input type="text" class="form-control" id="last_name" name="last_name" value="{userprofile.user.last_name or ''}">
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="new_password" class="fw-bold">New Password</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fas fa-lock"></i></span>
                                </div>
                                <input type="password" class="form-control" id="new_password" name="new_password" placeholder="Leave blank to keep current">
                                <div class="input-group-append">
                                    <span class="input-group-text" style="cursor: pointer;" id="editToggleIcon">
                                        <i class="fas fa-eye"></i>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="confirm_password" class="fw-bold">Confirm Password</label>
                            <input type="password" class="form-control" id="confirm_password" name="confirm_password" placeholder="Confirm new password">
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="office" class="fw-bold">Office</label>
                            <select class="form-control" id="office" name="office">
                                <option value="">Select Office (Optional)</option>
                                {''.join([f'<option value="{office.id}" {"selected" if userprofile.office and userprofile.office.id == office.id else ""}>{office.office_name} ({office.office_code})</option>' for office in offices])}
                            </select>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="role" class="fw-bold">Role <span class="text-danger">*</span></label>
                            <select class="form-control" id="role" name="role" required>
                                <option value="STAFF" {"selected" if userprofile.role == 'STAFF' else ""}>Staff</option>
                                <option value="HEAD" {"selected" if userprofile.role == 'HEAD' else ""}>Office Head</option>
                                <option value="EXECUTIVE" {"selected" if userprofile.role == 'EXECUTIVE' else ""}>Executive</option>
                                <option value="GOVERNOR" {"selected" if userprofile.role == 'GOVERNOR' else ""}>Governor</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <div class="custom-control custom-switch">
                        <input type="checkbox" class="custom-control-input" id="is_active" name="is_active" {"checked" if userprofile.user.is_active else ""}>
                        <label class="custom-control-label" for="is_active">Active Account</label>
                    </div>
                    <small class="text-muted">If unchecked, user won't be able to log in</small>
                </div>
                
                <div class="alert alert-info mt-3" id="editPasswordStrength" style="display: none;">
                    <strong>Password Strength:</strong> <span id="editStrengthText">Weak</span>
                    <div class="progress mt-2" style="height: 5px;">
                        <div class="progress-bar" id="editStrengthBar" role="progressbar" style="width: 0%;"></div>
                    </div>
                </div>
            </div>
            <div class="modal-footer bg-light">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">
                    <i class="fas fa-times me-2"></i>Cancel
                </button>
                <button type="submit" class="btn btn-primary" id="editSubmitBtn">
                    <i class="fas fa-save me-2"></i>Save Changes
                </button>
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
    ).exclude(
        user__date_joined=timezone.now()
    )[:10]
    
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
            
            # Approve the user
            user.is_active = True
            user.save()
            
            profile.is_approved = True
            profile.approved_at = timezone.now()
            profile.approved_by = request.user
            profile.save()
            
            return JsonResponse({
                'success': True, 
                'message': f'User {user.username} has been approved successfully!'
            })
            
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
            
            profile.user.delete()
            
            return JsonResponse({
                'success': True, 
                'message': f'User {username} has been rejected and removed.'
            })
            
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
            approved_count = 0
            
            for profile in profiles:
                user = profile.user
                user.is_active = True
                user.save()
                
                profile.is_approved = True
                profile.approved_at = timezone.now()
                profile.approved_by = request.user
                profile.save()
                approved_count += 1
            
            return JsonResponse({
                'success': True, 
                'message': f'{approved_count} user(s) have been approved successfully!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)