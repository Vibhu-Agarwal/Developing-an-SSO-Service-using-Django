import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import APIException

from .managers import CustomUserManager

email_superuser = 'superuser@vigastudios.com'


class Organization(models.Model):

    name = models.CharField(max_length=50)
    joining_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model to store all kinds of users in the database.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          serialize=False, verbose_name='ID')
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='static', null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    nickname = models.CharField(_('nickname'), max_length=30, blank=True, null=True)
    phone_number = PhoneNumberField()
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL,
                                     related_name='users', null=True, blank=True)
    admin_org = models.OneToOneField(Organization, on_delete=models.SET_NULL,
                                     related_name='admin', null=True, blank=True)

    is_active = models.BooleanField(_('is active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number']

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
        if self.admin_org:
            if self.organization:
                if self.organization != self.admin_org:
                    raise APIException(str(f'User is a part of {self.organization}'))
            else:
                self.organization = self.admin_org
        super(User, self).save()


class OrganizationJoinRequest(models.Model):

    org = models.ForeignKey(Organization, on_delete=models.CASCADE,
                            related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='org_requests')

    class Meta:
        unique_together = ['org', 'user']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.user.organization == self.org:
            raise APIException(f'User is already a member of {self.org}')
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)

    def accept(self):
        self.user.organization = self.org
        self.user.save()
        self.delete()
