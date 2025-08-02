from django.contrib import admin

# Register your models here.


from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'password','created_at', 'updated_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'phone',]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'created_at','is_verified']
    search_fields = ['user', 'otp_code']
    # readonly_fields = ['expires_at']
    # ordering = ['email']