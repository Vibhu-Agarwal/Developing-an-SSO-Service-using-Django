import requests
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Organization, email_superuser
from users.serializers import UserSerializer

User = get_user_model()


def make_request_to_callback_url(service, user: User = None):
    admin_SSO = User.objects.get(email=email_superuser)
    token = RefreshToken.for_user(admin_SSO)
    token['aud'] = service.identifier
    if user is None:
        user = admin_SSO
        token['sso_admin'] = True
    headers = {
        'Authorization': f"Bearer {token.access_token}"
    }
    user_data = UserSerializer(user).data
    response = requests.post(service.callback_url, data=user_data, headers=headers)
    if not response.ok:
        raise APIException(f"Call to Service ({service}) Failed!"
                           f"Returned with status code: {response.status_code}")


class Service(models.Model):

    name = models.CharField(max_length=50)
    identifier = models.CharField(max_length=10, unique=True)
    callback_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self._state.adding:
            make_request_to_callback_url(self)
        super(Service, self).save(force_insert=force_insert, force_update=force_update,
                                  using=using, update_fields=update_fields)

    @classmethod
    def for_user(cls, user: User):
        # Returns Queryset of Services the
        # User is connected to
        if not user.is_staff:
            org = user.organization
            if org:
                org_services = cls.objects.filter(org_subscriptions__org=org,
                                                  org_subscriptions__is_active=True)
                user_services = org_services.filter(user_connections__user=user)
            else:
                return cls.objects.none()
        else:
            user_services = cls.objects.all()
        return user_services


class Connection(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='service_connections')
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                related_name='user_connections')

    class Meta:
        unique_together = ['service', 'user']

    def __str__(self):
        return f"{self.user} | {self.service}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self._state.adding:
            make_request_to_callback_url(self.service, self.user)
        super(Connection, self).save(force_insert=force_insert, force_update=force_update,
                                     using=using, update_fields=update_fields)


class Subscription(models.Model):

    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                related_name='org_subscriptions')
    org = models.ForeignKey(Organization, on_delete=models.CASCADE,
                            related_name='service_subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ['service', 'org']

    def __str__(self):
        return f"{self.service} | {self.org}"
