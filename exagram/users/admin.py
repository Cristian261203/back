from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar',)}),  
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')  

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
