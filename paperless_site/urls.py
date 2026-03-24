from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Import lahat ng function galing sa tracking/views.py
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
    delete_user, 
    edit_user, 
    user_details,
    access_requests,    
    approve_user,
    reject_user,
    bulk_approve_users,
    pending_staff_approvals,
    approve_staff,
    reject_staff,
    my_department_staff,
    inbound_external_documents,
)

# Import lahat ng function galing sa tracking/documentview.py
from tracking import documentview

urlpatterns = [
    # ==========================================
    # AUTHENTICATION & CORE ENTRY
    # ==========================================
    path('', login, name='login'), 
    path('register/', register, name='register'), 
    path('logout/', logout, name='logout'),
    path('adminlogin/', admin_login, name='admin_login'), 
    path('headlogin/', head_login, name='head_login'),

    # ==========================================
    # SYSTEM ADMIN (Django Native & Custom)
    # ==========================================
    path('admin/system/', admin.site.urls), 
    path('admin/', admin_dashboard, name='admin_dashboard'), 

    # ==========================================
    # DASHBOARDS (Role-Based)
    # ==========================================
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard_alt'),
    path('head-dashboard/', head_dashboard, name='head_dashboard'),

    # ==========================================
    # USER MANAGEMENT (Superuser/Admin Only)
    # ==========================================
    path('user-management/', user_management, name='user_management'),
    path('user-details/<int:user_id>/', user_details, name='user_details'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    
    # Registration Approval System (Admin Level)
    path('access-requests/', access_requests, name='access_requests'),
    path('approve-user/<int:profile_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:profile_id>/', reject_user, name='reject_user'),
    path('bulk-approve-users/', bulk_approve_users, name='bulk_approve_users'),

    # ==========================================
    # STAFF APPROVAL SYSTEM (Department Head Level)
    # ==========================================
    path('pending-staff-approvals/', pending_staff_approvals, name='pending_staff_approvals'),
    path('my-department-staff/', my_department_staff, name='my_department_staff'),
    path('approve-staff/<int:user_profile_id>/', approve_staff, name='approve_staff'),
    path('reject-staff/<int:user_profile_id>/', reject_staff, name='reject_staff'),

    # ==========================================
    # INBOUND DOCUMENTS & DECISIONS (For Head)
    # ==========================================
    path('head/inbound-external/', inbound_external_documents, name='inbound_external_documents'),
    path('decisions/', documentview.document_decision_history, name='document_decision_history'),

    # ==========================================
    # DOCUMENT TRACKING & MANAGEMENT
    # ==========================================
    path('upload-document/', documentview.upload_document, name='upload_document'), 
    path('send-document/', documentview.send_document, name='send_document'),
    path('delete-document/<int:doc_id>/', documentview.delete_document, name='delete_document'),
    path('mark-as-read/<int:doc_id>/', documentview.mark_as_read, name='mark_as_read'),
    
    path('documents/all/', documentview.all_documents, name='all_documents'),
    path('my-uploads/', documentview.my_uploads_view, name='my_uploads'),
    path('received/', documentview.received_docs_view, name='received_documents'),
    path('sent-status/', documentview.sent_documents_status, name='sent_status'),
    path('sent-documents/', documentview.view_sent_documents, name='view_sent_documents'),

    # ==========================================
    # API ENDPOINTS (AJAX/Fetch)
    # ==========================================
    # Note: Siguraduhing may trailing slash (/) para iwas 404/301 errors
    path('api/notifications/', documentview.get_notifications_api, name='notifications_api'),
    path('api/notifications/mark-read/<int:ntf_id>/', documentview.mark_as_read_api, name='mark_as_read_api'),
    path('api/documents/approve/<int:doc_id>/', documentview.approve_document_api, name="approve_document_api"),
    path('api/documents/reject/<int:doc_id>/', documentview.reject_document_api, name="reject_document_api"),
    path('api/documents/receive/<int:doc_id>/', documentview.receive_document_api, name="receive_document_api"),

    # ==========================================
    # PASSWORD RESET
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
]

# Static & Media Files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)