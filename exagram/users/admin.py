from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar',)}),  # 将 avatar 字段添加到用户管理界面
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')  # 在管理界面中显示用户和个人简介

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
