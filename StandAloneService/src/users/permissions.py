from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.models import TokenUser
from django.contrib.auth import get_user_model

User = get_user_model()

SSO_ADMIN_EMAIL = 'superuser@vigastudios.com'


class IsSSOAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        try:
            assert request.user and request.user.is_authenticated
            if request.auth.payload.get('sso_admin'):
                return True
            user = request.user
            if isinstance(request.user, TokenUser):
                user_set = User.objects.filter(id=user.id)
                if user_set.exists():
                    user = user_set.first()
                else:
                    return False
            return user.email == SSO_ADMIN_EMAIL
        except AssertionError:
            return False


class IsUserOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, user_obj):
        return user_obj == request.user
