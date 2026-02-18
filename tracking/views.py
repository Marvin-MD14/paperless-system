from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Office, UserProfile, Document
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

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
        remember_me = request.POST.get('remember_me')  # <-- Get remember me checkbox

        user = authenticate_by_email(email, password)

        if user is not None:
            auth_login(request, user)

            # --- REMEMBER ME FUNCTIONALITY ---
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)        # expires on browser close

            return redirect_by_role(user)
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'login.html')


def redirect_by_role(user):
    """Helper function para sa redirection logic base sa role"""
    if user.is_superuser:
        return redirect('admin_dashboard')

    try:
        role = user.userprofile.role
        if role == 'HEAD':
            return redirect('head_dashboard')
        elif role in ['GOVERNOR', 'EXECUTIVE']:
            return redirect('executive_dashboard')
        else:
            return redirect('user_dashboard')
    except UserProfile.DoesNotExist:
        return redirect('login')


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
            try:
                profile = user.userprofile
                if profile.role == 'HEAD':
                    auth_login(request, user)

                    if remember_me:
                        request.session.set_expiry(1209600)
                    else:
                        request.session.set_expiry(0)

                    return redirect('head_dashboard')
                else:
                    messages.error(request, "Access Denied: Account is not a Department Head.")
            except UserProfile.DoesNotExist:
                messages.error(request, "Profile not found.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'head_login.html')


# --- DASHBOARD SECTION (With Cache Protection) ---

@login_required
@never_cache
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')

    offices = Office.objects.all()
    profiles = UserProfile.objects.select_related('user', 'office').all()

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')  # <-- Get Full Name from modal
        role = request.POST.get('role')
        office_id = request.POST.get('office')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('admin_dashboard')

        try:
            # Split full_name into first_name and last_name
            first_name = full_name
            last_name = ''
            if ' ' in full_name:
                parts = full_name.strip().split()
                first_name = parts[0]
                last_name = ' '.join(parts[1:])

            # Create new User
            new_user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            office_obj = Office.objects.get(id=office_id) if office_id else None
            UserProfile.objects.create(
                user=new_user,
                office=office_obj,
                role=role
            )

            messages.success(request, f"Successfully created {role} account for {full_name} ({email})!")
            return redirect('admin_dashboard')

        except Exception as e:
            messages.error(request, f"Error: {e}")

    governor_count = UserProfile.objects.filter(role='GOVERNOR').count()
    heads_count = UserProfile.objects.filter(role='HEAD').count()
    executive_count = UserProfile.objects.filter(role='EXECUTIVE').count()
    staff_count = UserProfile.objects.filter(role='STAFF').count()

    context = {
        'offices': offices,
        'profiles': profiles,
        'governor_count': governor_count,
        'heads_count': heads_count,
        'executive_count': executive_count,
        'staff_count': staff_count,
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
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role == 'HEAD':
        return redirect('head_dashboard')
    elif profile.role in ['GOVERNOR', 'EXECUTIVE']:
        return redirect('executive_dashboard')
    elif profile.role != 'STAFF':
        messages.error(request, "Unauthorized access to Employee Dashboard.")
        return redirect('login')

    my_uploads = Document.objects.filter(
        creator=request.user
    ).order_by('-created_at')[:5]

    my_uploads_count = Document.objects.filter(
        creator=request.user
    ).count()

    office_docs_count = Document.objects.filter(
        routings__to_office=profile.office,
        status='PENDING'
    ).distinct().count()

    context = {
        'profile': profile,
        'my_uploads': my_uploads,
        'office_docs_count': office_docs_count,
        'my_uploads_count': my_uploads_count,
    }

    return render(request, 'employee_dashboard.html', context)


# --- ACCOUNT ACTIONS ---

def register(request):
    offices = Office.objects.all().order_by('office_name')

    if request.method == "POST":
        email = request.POST.get('username')  # <-- matches HTML field name
        password = request.POST.get('pwd')
        full_name = request.POST.get('full_name')
        office_id = request.POST.get('office')
        role = 'STAFF'

        if User.objects.filter(username=email).exists():
            messages.error(request, f"The email '{email}' is already registered.")
            return render(request, 'register.html', {'offices': offices})

        try:
            # Split full_name into first_name and last_name
            first_name = full_name
            last_name = ''
            if ' ' in full_name:
                parts = full_name.strip().split()
                first_name = parts[0]
                last_name = ' '.join(parts[1:])

            # Create new User
            new_user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            office_obj = get_object_or_404(Office, id=office_id)

            UserProfile.objects.create(
                user=new_user,
                office=office_obj,
                role=role
            )

            messages.success(request, "Your account has been created successfully. Please log in.")
            return render(request, 'register.html', {'offices': offices})

        except Exception as e:
            if 'new_user' in locals():
                new_user.delete()
            messages.error(request, f"Registration failed: {e}")

    return render(request, 'register.html', {'offices': offices})



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
