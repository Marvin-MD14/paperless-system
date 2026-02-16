from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Department, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# 1. PARA SA REGULAR STAFF (localhost:8000/)
def login(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None:
            # Check kung HINDI siya superuser
            if not user.is_superuser:
                auth_login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, "Admin accounts must use the Admin Portal.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'login.html')

# 2. PARA SA ADMIN LOGIN (localhost:8000/adminlogin/)
def admin_login(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None:
            # Check kung SUPERUSER siya
            if user.is_superuser:
                auth_login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. Not an administrator.")
        else:
            messages.error(request, "Invalid admin credentials.")
            
    return render(request, 'admin_login.html') # Gawa tayo ng separate na template nito mamaya

# 3. REGULAR STAFF DASHBOARD
def user_dashboard(request):
    return render(request, 'dashboard.html')

# 4. ADMIN DASHBOARD (May registration logic na ito)
def admin_dashboard(request):
    # Security: Double check kung admin ang nakatingin
    if not request.user.is_superuser:
        return redirect('admin_login')

    departments = Department.objects.all()
    profiles = UserProfile.objects.all()
    heads_count = UserProfile.objects.filter(role='HEAD').count()
    governor_count = UserProfile.objects.filter(role='GOVERNOR').count()
    executive_count = UserProfile.objects.filter(role='EXECUTIVE').count()
    staff_count = UserProfile.objects.filter(role='STAFF').count()

    if request.method == "POST":
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        role = request.POST.get('role')
        dept_id = request.POST.get('department')

        try:
            new_user = User.objects.create_user(username=u_name, password=p_word)
            dept_obj = Department.objects.get(id=dept_id) if dept_id else None
            UserProfile.objects.create(user=new_user, department=dept_obj, role=role)
            
            messages.success(request, f"Account created for {u_name}!")
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f"Error: {e}")

    context = {
        'departments': departments,
        'profiles': profiles,
        'heads_count': heads_count,
        'governor_count': governor_count,
        'executive_count': executive_count,
        'staff_count': staff_count,
    }
    return render(request, 'admin_dashboard.html', context)

# 5. REGISTER (Optional page kung gusto mo ng hiwalay sa dashboard)
def register(request):
    depts = Department.objects.all()
    return render(request, 'register.html', {'departments': depts})

# 6. LOGOUT
def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# PARA SA DEPARTMENT HEAD LOGIN (localhost:8000/headlogin/)
def head_login(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None:
            # Kunin ang profile para i-check ang role
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

# DEPARTMENT HEAD DASHBOARD
def head_dashboard(request):
    # Security: Dapat HEAD lang ang nakaka-access
    if not request.user.is_authenticated or request.user.userprofile.role != 'HEAD':
        return redirect('head_login')
        
    user_profile = request.user.userprofile
    # Dito, kukunin lang natin ang staff na kapareho ng department niya
    my_staff = UserProfile.objects.filter(department=user_profile.department).exclude(user=request.user)

    context = {
        'profile': user_profile,
        'my_staff': my_staff,
    }
    return render(request, 'head_dashboard.html', context)