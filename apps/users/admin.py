from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        (_("Login details"), {'fields': ('email', 'password',)}),
        (_('User info'), {
         'fields': ('first_name', 'last_name', 'role', 'branch',)}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    list_display = ['email', 'role', 'first_name', 'last_name']
    list_editable = ['role']
    search_fields = ('email', 'first_name', 'last_name',)
    list_filter = ('role', 'branch',)
    ordering = ('id',)


admin.site.register(User, UserAdmin)
