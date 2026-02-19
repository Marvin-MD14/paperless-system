from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from tracking.views import (
    login,           # dating login_view
    admin_login,     # dating admin_login_view
    register,        # dating register_view
    admin_dashboard, 
    logout,          # dating logout_view
    user_dashboard,
    head_login, 
    head_dashboard,
    user_management,
    register_user,
    delete_user,
    edit_user,
    user_details,
)

urlpatterns = [
    path('admin/', admin.site.urls), 
    
    path('', login, name='login'), 
    
    path('adminlogin/', admin_login, name='admin_login'), 
    
    # 3. Dashboards 
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('headlogin/', head_login, name='head_login'),
    path('headdashboard/', head_dashboard, name='head_dashboard'),

    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),

  # PASSWORD RESET SECTION 
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html',          # Tinanggal ang registration/
             email_template_name='password_reset_email.html',    # Tinanggal ang registration/
             subject_template_name='password_reset_subject.txt', # Tinanggal ang registration/
             success_url='/password-reset/done/'
         ), 
         name='password_reset'),
         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'           # Tinanggal ang registration/
         ), 
         name='password_reset_done'),
         
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',       # Tinanggal ang registration/
             success_url='/password-reset-complete/'
         ), 
         name='password_reset_confirm'),
         
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'      # Tinanggal ang registration/
         ), 
         name='password_reset_complete'),

    # User Management
    path('user-management/', user_management, name='user_management'),
    path('register-user/', register_user, name='register_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('user-details/<int:user_id>/', user_details, name='user_details'),
]