from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Office, UserProfile, Document
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None:
            auth_login(request, user)
            # Check for Admin (Superuser)
            if user.is_superuser:
                return redirect('admin_dashboard')
            
            # Check Role via UserProfile
            try:
                role = user.userprofile.role
                if role == 'HEAD':
                    return redirect('head_dashboard')
                elif role in ['GOVERNOR', 'EXECUTIVE']:
                    return redirect('executive_dashboard')
                else:
                    return redirect('user_dashboard')
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found. Contact Admin.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'login.html')

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

def user_dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')

    offices = Office.objects.all()
    profiles = UserProfile.objects.select_related('user', 'office').all()

    if request.method == "POST":
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        role = request.POST.get('role')
        office_id = request.POST.get('office') # Changed from department to office

        try:
            new_user = User.objects.create_user(username=u_name, password=p_word)
            office_obj = Office.objects.get(id=office_id) if office_id else None
            UserProfile.objects.create(user=new_user, office=office_obj, role=role)
            
            messages.success(request, f"Successfully created {role} account for {u_name}!")
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f"Error: {e}")

    context = {
        'offices': offices,
        'profiles': profiles,
        'counts': {
            'HEAD': UserProfile.objects.filter(role='HEAD').count(),
            'STAFF': UserProfile.objects.filter(role='STAFF').count(),
            'EXEC': UserProfile.objects.filter(role__in=['GOVERNOR', 'EXECUTIVE']).count(),
        }
    }
    return render(request, 'admin_dashboard.html', context)

def register(request):
    depts = Department.objects.all()
    return render(request, 'register.html', {'departments': depts})

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

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

# 2. HEAD DASHBOARD (Filtering by Office)
@login_required
def head_dashboard(request):
    # Security: Ensure only HEADs can enter
    if request.user.userprofile.role != 'HEAD':
        messages.error(request, "Unauthorized access.")
        return redirect('login')
        
    profile = request.user.userprofile
    # Filter staff belonging only to the Head's Office
    my_staff = UserProfile.objects.filter(office=profile.office).exclude(user=request.user)
    
    # Injected Logic: Get documents currently in this office
    # (Based on the Document Routing table in your ERD)
    office_docs = Document.objects.filter(routings__to_office=profile.office).distinct()

    context = {
        'profile': profile,
        'my_staff': my_staff,
        'office_docs': office_docs,
    }
    return render(request, 'head_dashboard.html', context)