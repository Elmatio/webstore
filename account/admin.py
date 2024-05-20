from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('last_name', 'first_name', 'middle_name', 'passport', 'email', 'born_date', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'last_name', 'first_name', 'middle_name', 'passport', 'email', 'born_date', 'phone', 'address', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
