import os
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Import lahat ng kailangan mula sa tracking app views
from tracking.views import (
    login, 
    admin_login, 
    register, 
    admin_dashboard, 
    logout, 
    user_dashboard, 
    head_login, 
    head_dashboard,
    user_management, 
    register_user, 
    delete_user, 
    edit_user, 
    user_details,
    access_requests,
    approve_user,
    reject_user,
    bulk_approve_users,
)

# Dito nanggagaling ang lahat ng logic para sa documents
from tracking import documentview

urlpatterns = [
    # ==========================================
    # 1. ADMIN PANEL
    # ==========================================
    path('admin/', admin.site.urls), 
    
    # ==========================================
    # 2. AUTHENTICATION & ACCOUNTS
    # ==========================================
    path('', login, name='login'), 
    path('adminlogin/', admin_login, name='admin_login'), 
    path('headlogin/', head_login, name='head_login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    
    # ==========================================
    # 3. DASHBOARDS
    # ==========================================
    # Siguraduhin na ang 'user_dashboard' view ay nagpapasa ng context 
    # (word_count, recent_logs, etc.) para gumana ang charts.
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('headdashboard/', head_dashboard, name='head_dashboard'),

    # ==========================================
    # 4. PASSWORD RESET SECTION
    # ==========================================
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html',          
             email_template_name='password_reset_email.html',    
             subject_template_name='password_reset_subject.txt', 
             success_url='/password-reset/done/'
         ), name='password_reset'),
         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'          
         ), name='password_reset_done'),
         
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',       
             success_url='/password-reset-complete/'
         ), name='password_reset_confirm'),
         
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'     
         ), name='password_reset_complete'),

    # ==========================================
    # 5. USER MANAGEMENT (Admin Only)
    # ==========================================
    path('user-management/', user_management, name='user_management'),
    path('register-user/', register_user, name='register_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('user-details/<int:user_id>/', user_details, name='user_details'),

    # ==========================================
    # 6. DOCUMENT MANAGEMENT LOGIC
    # ==========================================
    # Main upload page at listahan ng uploads
    path('upload-document/', documentview.upload_document, name='upload_document'), 
    
    # Forwarding logic
    path('send-document/', documentview.send_document, name='send_document'),
    
    # Delete logic
    path('delete-document/<int:doc_id>/', documentview.delete_document, name='delete_document'),
    
    # All records (Uploads and Received)
    path('documents/all/', documentview.all_documents, name='all_documents'),
    
    # Tracking status ng pinadalang docs
    path('sent-status/', documentview.sent_documents_status, name='sent_status'),
    
    # Received Documents List (View All link from Dashboard)
    path('received/', documentview.received_docs_view, name='received_documents'),
    path('mark-as-read/<int:doc_id>/', documentview.mark_as_read, name='mark_as_read'),

    path('access-requests/', access_requests, name='access_requests'),
    path('approve-user/<int:profile_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:profile_id>/', reject_user, name='reject_user'),
    path('bulk-approve-users/', bulk_approve_users, name='bulk_approve_users'),

    # path('upload-document/', user_dashboard, name='upload_document'), 
    # path('document-list/', user_dashboard, name='document_list'),

   # Notification API
    path('api/notifications/', documentview.get_notifications_api, name='notifications_api'),
    path('api/notifications/mark-read/<int:ntf_id>/', documentview.mark_as_read_api, name='mark_as_read_api'),

    # Approved / Reject
   path("api/documents/approve/<int:doc_id>/", documentview.approve_document_api, name="approve_document_api"),
   path("api/documents/reject/<int:doc_id>/", documentview.reject_document_api, name="reject_document_api"),

   path('my-uploads/', documentview.my_uploads_view, name='my_uploads'),


]

# Media files serving (Importante para ma-view/download ang uploaded files)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Access Requests
    
