from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from users.models import User, Organization


class CustomUserAdmin(UserAdmin):
    ordering = ('id',)
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'phone_number', 'is_active', 'is_staff', 'organization', 'admin_org')
    list_display_links = ('id', 'first_name', 'last_name', 'email')
    list_filter = ('is_staff',)

    fieldsets = (
        (None, {'fields': ('password', 'email', 'nickname')}),
        ('Personal info', {'fields': ('avatar', 'first_name', 'last_name', 'phone_number')}),
        ('Organization Details', {'fields': ('organization', 'admin_org')}),
        ('User Details', {'fields': ('is_active', 'is_staff', 'groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name',
                       'phone_number', 'password1', 'password2'),
        }),
    )


class OrganizationPanel(admin.ModelAdmin):
    list_display = ('id', 'name', 'joining_date')
    list_display_links = ('id', 'name', 'joining_date')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Organization, OrganizationPanel)
