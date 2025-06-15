from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FarmerProfile, OperatorProfile

# 1. Custom Admin for User model
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'role'),
        }),
    )

    list_display = ('email', 'role', 'is_staff', 'is_active', 'createdAt', 'updatedAt', 'id')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'role')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',) 

    readonly_fields = ('id', 'createdAt', 'updatedAt', 'last_login')
    
# Register User model with custom admin class
admin.site.register(User, CustomUserAdmin)

# Register FarmerProfile
@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'firstName', 'lastName', 'phone', 'createdAt')
    search_fields = ('user__email', 'firstName', 'lastName', 'phone')
    # list_filter = ('type',)

    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = 'user__email'
    user_email.short_description = 'User Email'

# Register OperatorProfile
@admin.register(OperatorProfile)
class OperatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'firstName', 'lastName', 'phone', 'businessName', 'createdAt')
    search_fields = ('user__email', 'firstName', 'lastName', 'phone')
  
    # If we add 'service_type' in the future, add it here: list_filter = ('service_type',)

    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = 'user__email'
    user_email.short_description = 'User Email'