from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class GroupAdmin(admin.ModelAdmin):
    show_reverse_many_to_many = ('user',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','email', 'name', 'surname', 'is_active', 'is_staff')
    list_display_links = ('id', 'email', 'name', 'surname')
    ordering = ('email',)  # order by email instead of username
    search_fields = ('name', 'surname', 'email')

    # Defined fieldsets for editing an existing user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )

    # Defined add_fieldsets for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    # Specify email as the unique identifier
    add_form_template = 'admin/auth/user/add_form.html'
    readonly_fields = ('created_at',)
