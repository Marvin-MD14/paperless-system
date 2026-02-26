from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Office, UserProfile, Document
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.http import JsonResponse
import json
from .choices import OFFICE_CHOICES

# --- HELPER FUNCTION: Authenticate by email ---
def authenticate_by_email(email, password):
    """Authenticate user using email instead of username."""
    try:
        user_obj = User.objects.get(email=email)
        user = authenticate(username=user_obj.username, password=password)
        return user
    except User.DoesNotExist:
        return None

# --- LOGIN SECTION ---
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

            # --- REMEMBER ME FUNCTIONALITY ---
            if remember_me:
                request.session.set_expiry(1209600)  
            else:
                request.session.set_expiry(0)        

            return redirect_by_role(user)
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'login.html')


def redirect_by_role(user):
    """
    Helper function para sa redirection logic base sa role.
    Updated: Gumagamit ng get_or_create para maiwasan ang DoesNotExist error.
    """
    # 1. Check kung Superuser (Admin ng Django)
    if user.is_superuser:
        return redirect('admin_dashboard')

    # 2. Siguraduhin na may UserProfile ang user. 
    # Kung wala pa, kusa itong gagawa ng bago na may default role na 'STAFF'.
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'STAFF'} # Default role kung bagong gawa
    )

    # 3. Redirection logic base sa nakuha o ginawang profile
    role = profile.role
    
    if role == 'HEAD':
        return redirect('head_dashboard')
    
    elif role in ['GOVERNOR', 'EXECUTIVE']:
        return redirect('executive_dashboard')
    
    elif role == 'STAFF':
        return redirect('user_dashboard')
    
    # Fallback kung sakaling may ibang role na hindi nahanap
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
            # Gagamit tayo ng get_or_create. 
            # Kung wala pang profile si user, gagawan siya ng default na 'HEAD' role.
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'HEAD'}
            )

            # I-verify kung HEAD nga ang role ng profile
            if profile.role == 'HEAD':
                auth_login(request, user)

                # --- REMEMBER ME LOGIC ---
                if remember_me:
                    request.session.set_expiry(1209600) # 2 weeks
                else:
                    request.session.set_expiry(0) # Browser close logout

                return redirect('head_dashboard')
            else:
                messages.error(request, "Access Denied: Account is not an Office Head.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'head_login.html')


# --- DASHBOARD SECTION (With Cache Protection) ---
@login_required
@never_cache
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')

    # Kinukuha ang listahan para sa table at dropdowns
    offices = Office.objects.all()
    profiles = UserProfile.objects.select_related('user', 'office').all().order_by('-user__date_joined')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name', '')
        role = request.POST.get('role')
        office_id = request.POST.get('office')

        # 1. Validation: Check kung ang email/username ay gamit na
        if User.objects.filter(username=email).exists():
            messages.error(request, f"Error: The email {email} is already registered.")
            return redirect('admin_dashboard')

        try:
            # 2. Name Splitting Logic
            parts = full_name.strip().split()
            first_name = parts[0] if parts else ""
            last_name = ' '.join(parts[1:]) if len(parts) > 1 else ""

            # 3. Create the User Object
            new_user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # 4. Get Office Object safely
            # Ginagamit natin ang office_id mula sa form (karaniwang PK/ID ito)
            office_obj = None
            if office_id:
                try:
                    office_obj = Office.objects.get(id=office_id)
                except Office.DoesNotExist:
                    office_obj = None

            # 5. Safe Profile Creation/Update
            # Gagamit tayo ng update_or_create para iwas "Duplicate Entry" 
            # sakaling may active na signals sa models.py mo.
            UserProfile.objects.update_or_create(
                user=new_user,
                defaults={
                    'office': office_obj,
                    'role': role
                }
            )

            messages.success(request, f"Successfully created {role} account for {full_name}!")
            return redirect('admin_dashboard')

        except Exception as e:
            messages.error(request, f"System Error: {str(e)}")
            return redirect('admin_dashboard')

    # Counting logic for the dashboard statistics
    context = {
        'offices': offices,
        'offices_list': OFFICE_CHOICES, # Kung kailangan mo pa ito para sa template
        'profiles': profiles,
        'governor_count': UserProfile.objects.filter(role='GOVERNOR').count(),
        'heads_count': UserProfile.objects.filter(role='HEAD').count(),
        'executive_count': UserProfile.objects.filter(role='EXECUTIVE').count(),
        'staff_count': UserProfile.objects.filter(role='STAFF').count(),
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
    # Imbes na get_object_or_404, gagamit tayo ng get_or_create
    # para kung wala pang profile ang user, gagawan siya ng system imbes na mag-error.
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'STAFF'} # Default role kung bagong gawa
    )

    if profile.role == 'HEAD':
        return redirect('head_dashboard')
    elif profile.role in ['GOVERNOR', 'EXECUTIVE']:
        return redirect('executive_dashboard')
    elif profile.role != 'STAFF':
        messages.error(request, "Unauthorized access.")
        return redirect('login')

    my_uploads = Document.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')[:5] 
    
    # Siguraduhing hindi mag-error kung walang office
    office_docs_count = 0
    if profile.office:
        office_docs_count = Document.objects.filter(
            routings__to_office=profile.office,
            status='PENDING'
        ).distinct().count()

    context = {
        'profile': profile,
        'my_uploads': my_uploads,
        'office_docs_count': office_docs_count,
        'my_uploads_count': Document.objects.filter(uploaded_by=request.user).count(),
    }
    return render(request, 'employee_dashboard.html', context)
# --- ACCOUNT ACTIONS ---
def register(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('pwd')
        full_name = request.POST.get('full_name')
        office_code = request.POST.get('office')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        try:
            # 1. Create User
            parts = full_name.strip().split()
            first_name = parts[0] if parts else ""
            last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            new_user = User.objects.create_user(
                username=email, email=email, password=password,
                first_name=first_name, last_name=last_name
            )

            # 2. Setup Office
            office_display = dict(OFFICE_CHOICES).get(office_code, office_code)
            office_instance, _ = Office.objects.get_or_create(
                office_code=office_code,
                defaults={'office_name': office_display}
            )

            # 3. Safe Profile Creation (Ito ang fix sa Duplicate Entry)
            # Ginagamit ang update_or_create para kung ginawa na ng Signal ang profile, 
            # ia-update na lang nito ang office at role imbes na gumawa ng bago.
            UserProfile.objects.update_or_create(
                user=new_user,
                defaults={
                    'office': office_instance,
                    'role': 'STAFF'
                }
            )

            messages.success(request, "Account created! Please log in.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Registration failed: {e}")
            return redirect('register')

    return render(request, 'register.html', {'offices': OFFICE_CHOICES})
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
@user_passes_test(lambda u: u.is_superuser)  # Only admins
def user_management(request):
    # Get filter parameters
    role_filter = request.GET.get('role', '')
    search_query = request.GET.get('search', '')
    
    # Get all user profiles
    userprofiles = UserProfile.objects.select_related('user', 'office').all().order_by('-user__date_joined')
    
    # Apply filters
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
    
    # Get counts by role
    governor_count = UserProfile.objects.filter(role='GOVERNOR').count()
    heads_count = UserProfile.objects.filter(role='HEAD').count()
    executive_count = UserProfile.objects.filter(role='EXECUTIVE').count()
    staff_count = UserProfile.objects.filter(role='STAFF').count()
    
    # Pagination
    paginator = Paginator(userprofiles, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all offices for dropdown
    offices = Office.objects.all().order_by('office_name')
    
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
        
        # Validate required fields
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('user_management')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken.')
            return redirect('user_management')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=is_active
            )
            
            # Get office if selected
            office = None
            if office_id:
                office = get_object_or_404(Office, id=office_id)
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                office=office,
                role=role
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
            user = get_object_or_404(User, id=user_id)
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
    
    # Get additional stats
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
        
        # Update profile
        office_id = request.POST.get('office')
        if office_id:
            userprofile.office = get_object_or_404(Office, id=office_id)
        else:
            userprofile.office = None
        
        userprofile.role = request.POST.get('role', userprofile.role)
        userprofile.save()
        
        messages.success(request, f'User {user.username} updated successfully!')
        return redirect('user_management')
    
    # GET request - show edit form
    offices = Office.objects.all()
    context = {
        'profile': userprofile,
        'offices': offices,
    }
    return render(request, 'edit_user.html', context)
