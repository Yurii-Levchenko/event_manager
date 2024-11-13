from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_display_links = ('id', 'email', 'first_name', 'last_name')
    ordering = ('email',)  # Example: order by email instead of username
    search_fields = ('first_name', 'last_name', 'email')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

