from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Office, UserProfile, Document
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# --- LOGIN SECTION ---

@never_cache
def login(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None:
            auth_login(request, user)
            return redirect_by_role(user)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            
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
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None:
            if user.is_superuser:
                auth_login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. Not an administrator.")
        else:
            messages.error(request, "Invalid admin credentials.")
            
    return render(request, 'admin_login.html') 

@never_cache
def head_login(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None:
            try:
                profile = user.userprofile
                if profile.role == 'HEAD':
                    auth_login(request, user)
                    return redirect('head_dashboard')
                else:
                    messages.error(request, "Access Denied: Account is not a Department Head.")
            except:
                messages.error(request, "Profile not found.")
        else:
            messages.error(request, "Invalid username or password.")
            
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
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        role = request.POST.get('role')
        office_id = request.POST.get('office')

        try:
            new_user = User.objects.create_user(username=u_name, password=p_word)
            office_obj = Office.objects.get(id=office_id) if office_id else None
            UserProfile.objects.create(user=new_user, office=office_obj, role=role)
            
            messages.success(request, f"Successfully created {role} account for {u_name}!")
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f"Error: {e}")

    # Calculate individual counts
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
    my_staff = UserProfile.objects.filter(office=profile.office).exclude(user=request.user)
    office_docs = Document.objects.filter(routings__to_office=profile.office).distinct()

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

    my_uploads = Document.objects.filter(creator=request.user).order_by('-created_at')[:5]
    my_uploads_count = Document.objects.filter(creator=request.user).count()
    
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
        u_name = request.POST.get('username')
        p_word = request.POST.get('pwd') 
        office_id = request.POST.get('office')
        role = 'STAFF'

        if User.objects.filter(username=u_name).exists():
            messages.error(request, f"The username '{u_name}' is already taken.")
            return render(request, 'register.html', {'offices': offices})

        try:
            new_user = User.objects.create_user(username=u_name, password=p_word)
            office_obj = get_object_or_404(Office, id=office_id)
            UserProfile.objects.create(user=new_user, office=office_obj, role=role)
            
            messages.success(request, "Your account has been created successfully. Please log in.")
            return render(request, 'register.html', {'offices': offices})
            
        except Exception as e:
            if 'new_user' in locals():
                new_user.delete()
            messages.error(request, f"Registration failed: {e}")

    return render(request, 'register.html', {'offices': offices})

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response