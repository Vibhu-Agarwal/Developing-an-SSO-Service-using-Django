from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model
from services.models import Connection

User = get_user_model()


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, user_obj):
        return user_obj == request.user


class IsSSOAdminOrReadOnly(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsOrganizationAdminOrSSOAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            (request.user.is_staff or request.user.admin_org)
        )

    def has_object_permission(self, request, view, obj):
        # obj -> Organization
        return request.user.is_staff or request.user.admin_org == obj


class IsOrganizationAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.admin_org
        )

    def has_object_permission(self, request, view, obj):
        perm = {
            Connection: lambda conn: conn.user.organization == request.user.admin_org,
            User: lambda user: user.organization == request.user.admin_org,
        }
        return perm.get(type(obj), lambda x: False)(obj)
