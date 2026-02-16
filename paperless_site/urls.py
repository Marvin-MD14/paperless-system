from django.contrib import admin
from django.urls import path
from tracking.views import (
    login,           # dating login_view
    admin_login,     # dating admin_login_view
    register,        # dating register_view
    admin_dashboard, 
    logout,          # dating logout_view
    user_dashboard,
    head_login, 
    head_dashboard,
)

urlpatterns = [
    path('admin/', admin.site.urls), # Django built-in admin
    
    # 1. Pintuan para sa Regular Staff
    path('', login, name='login'), 
    
    # 2. Pintuan para sa Admin (Safe/Hidden URL)
    path('adminlogin/', admin_login, name='admin_login'), 
    
    
    # 3. Dashboards (Dito ang bagsak pagkatapos ng login)
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('headlogin/', head_login, name='head_login'),
    path('headdashboard/', head_dashboard, name='head_dashboard'),

    # 4. Others
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
]