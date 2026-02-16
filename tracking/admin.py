from django.contrib import admin
from .models import Office, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'office')
    list_filter = ('role', 'office')

admin.site.register(Office)
admin.site.register(UserProfile, UserProfileAdmin)