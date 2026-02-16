from django.contrib import admin
from .models import Department, UserProfile

# Para mas magandang tingnan ang listahan ng users
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department')
    list_filter = ('role', 'department')

admin.site.register(Department)
admin.site.register(UserProfile, UserProfileAdmin)