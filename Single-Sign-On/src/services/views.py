from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListCreateAPIView, RetrieveDestroyAPIView,
    CreateAPIView, ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import (IsSSOAdminOrReadOnly,
                               IsOrganizationAdminOrSSOAdmin,
                               IsOrganizationAdmin)
from .models import Service, Connection
from .serializers import (ServiceSerializer, ConnectionSerializer,
                          PublicServiceSerializer)

User = get_user_model()
PUBLIC_KEY = open(settings.JWT_PUBLIC_KEY_PATH).read()


class FetchPublicKeyAPIView(APIView):

    def get(self, request):
        return Response({'key': PUBLIC_KEY})


class ListAllServiceAPIView(ListAPIView):
    serializer_class = PublicServiceSerializer
    permission_classes = (IsAuthenticated, IsOrganizationAdminOrSSOAdmin,)
    queryset = Service.objects.all()


class ListCreateServiceAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsSSOAdminOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Service.for_user(user)

    def get_serializer_class(self):
        ser = {
            'GET': PublicServiceSerializer,
            'POST': ServiceSerializer
        }
        return ser[self.request.method]


class CreateConnectionAPIView(CreateAPIView):
    serializer_class = ConnectionSerializer
    permission_classes = (IsAuthenticated, IsOrganizationAdmin)

    def perform_create(self, serializer):
        service = serializer.validated_data['service']
        user = serializer.validated_data['user']
        if user.organization != self.request.user.organization:
            raise PermissionDenied(f"{user} does not belong to your organization")
        if service.org_subscriptions.filter(org=self.request.user.organization).count() == 0:
            raise PermissionDenied(f"Your organization is not subscribed to {service}")
        serializer.save()


class ConnectionDetailAPIView(RetrieveDestroyAPIView):
    serializer_class = ConnectionSerializer
    permission_classes = (IsAuthenticated, IsOrganizationAdmin)
    queryset = Connection.objects.all()
