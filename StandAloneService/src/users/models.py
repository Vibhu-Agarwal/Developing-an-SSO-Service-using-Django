from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
import uuid

from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model to store local users in the database.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='ID')
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)

    is_staff = models.BooleanField(_('staff'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        user_representation = self.first_name
        if self.last_name:
            user_representation += f" {self.last_name}"
        return user_representation

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.clean()
        except ValidationError as e:
            raise APIException(str(e))
        super(User, self).save()
