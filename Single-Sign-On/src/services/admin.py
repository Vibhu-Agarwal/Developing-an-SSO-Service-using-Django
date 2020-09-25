from django.contrib import admin
from .models import Service, Connection, Subscription


class ServiceAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'identifier')
    list_display_links = ('id', 'name', 'identifier')


class ConnectionAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'service')
    list_display_links = ('id', 'user', 'service')


class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ('id', 'org', 'service', 'end_date', 'is_active')
    list_display_links = ('id', 'org', 'service', 'end_date', 'is_active')


admin.site.register(Service, ServiceAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
