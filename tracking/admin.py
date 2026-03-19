from django.contrib import admin
from .models import Office, UserProfile, Document, Routing, Notification
from .choices import OFFICE_DICT, ROLE_DICT, STATUS_DICT

# --- OFFICE ADMIN ---
@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    # Tinanggal ang 'created_at' dahil wala ito sa iyong models.py (maliban kung idadagdag mo)
    list_display = ('office_code', 'office_name')
    search_fields = ('office_code', 'office_name')
    ordering = ('office_name',)

# --- USER PROFILE ADMIN ---
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # list_display: Ang mga column na makikita mo sa main table
    list_display = ('get_username', 'get_full_name', 'get_role_display_name', 'get_office_display_name', 'is_approved', 'registration_type')
    
    # list_filter: Ang sidebar filter para madaling mag-sort
    list_filter = ('role', 'office', 'is_approved', 'registration_type')
    
    # search_fields: Para makapag-search ng tao gamit ang pangalan o username
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    
    # raw_id_fields: Para sa mabilis na pag-search ng user profile
    raw_id_fields = ('user',)

    # --- CUSTOM DISPLAY METHODS ---

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'

    def get_office_display_name(self, obj):
        # Dahil ForeignKey ang office, kukunin natin ang office_code nito
        if obj.office:
            # Hinahanap ang label sa OFFICE_DICT gamit ang office_code
            return OFFICE_DICT.get(obj.office.office_code, obj.office.office_name)
        return "No Office Assigned"
    # FIXED: Inayos ang pangalan dito para tumugma sa function name sa itaas
    get_office_display_name.short_description = 'Office/Department'

    def get_role_display_name(self, obj):
        return ROLE_DICT.get(obj.role, obj.role)
    get_role_display_name.short_description = 'Designated Role'

# --- OTHER MODELS ---
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'category', 'status', 'uploaded_at')
    list_filter = ('category', 'status')
    search_fields = ('title', 'uploaded_by__username')

@admin.register(Routing)
class RoutingAdmin(admin.ModelAdmin):
    list_display = ('document', 'from_office', 'to_office', 'status', 'routed_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_read', 'created_at')