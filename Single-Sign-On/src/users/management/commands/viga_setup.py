import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from users.models import email_superuser

EMAIL_HOST_PASSWORD = os.environ.get('VIGA_HOST_PASSWORD')
if not EMAIL_HOST_PASSWORD:
    raise ImproperlyConfigured("'VIGA_HOST_PASSWORD' environment variable is unset")

User = get_user_model()

superuser_phone_number = "+919999999999"

help_message = f"""
Sets up the DB, creating:
1) superuser with admin rights (Email: {email_superuser})
"""


class Command(BaseCommand):
    """
    viga_setup: Command to set-up database for the application
    """
    help = help_message

    def handle(self, *args, **kwargs):
        if not User.objects.filter(email=email_superuser).exists():
            User.objects.create_superuser(first_name="SSO ADMIN",
                                          email=email_superuser,
                                          password=EMAIL_HOST_PASSWORD,
                                          phone_number=superuser_phone_number)
            print('Super-User Created!')
        print('Viga Set-Up Complete!')
