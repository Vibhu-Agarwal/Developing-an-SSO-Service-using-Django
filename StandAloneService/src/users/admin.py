from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from users.models import User


class CustomUserAdmin(UserAdmin):
    ordering = ('id',)
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'is_staff')
    list_display_links = ('id', 'first_name', 'last_name', 'email')
    list_filter = ('is_staff',)

    fieldsets = (
        (None, {'fields': ('password', 'email')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('User Details', {'fields': ('is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name',
                       'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
