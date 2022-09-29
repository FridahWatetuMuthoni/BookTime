from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from . import models

"""_summary_
This is enough for all the basic systems to work. Django admin,
however, will not work, because the standard configuration requires the
presence of the username field. To fix this, we need to define a Django
admin handler for our custom User. Add this to your main/admin.py file:
"""
# Register your models here.


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Persmissions', {'fields': ('is_active', 'is_staff',
                                     'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            "classes": ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
