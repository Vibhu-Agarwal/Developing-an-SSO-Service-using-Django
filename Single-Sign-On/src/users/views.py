from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import (RetrieveUpdateDestroyAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView)
from rest_framework.permissions import (IsAuthenticated, SAFE_METHODS)
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Organization
from users.permissions import (IsOwner, IsOrganizationAdminOrSSOAdmin,
                               IsOrganizationAdmin, IsSSOAdminOrReadOnly)
from users.serializers import (CreateUserSerializer, UserSerializer,
                               OrganizationSerializer, PublicOrganizationSerializer,
                               PublicUserSerializer)

User = get_user_model()


class ListCreateOrganizationsAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsSSOAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PublicOrganizationSerializer
        else:
            return OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.all()


class OrganizationUsersAPIView(ListAPIView):

    permission_classes = (IsAuthenticated, IsOrganizationAdmin,)
    serializer_class = PublicUserSerializer

    def get_queryset(self):
        request_user = self.request.user
        return request_user.admin_org.users.exclude(id=request_user.id)


class ListAllUsersAPIView(ListAPIView):
    serializer_class = PublicUserSerializer

    def get_queryset(self):
        request_user = self.request.user
        return User.objects.exclude(id=request_user.id)


class OrganizationProfileGetView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Organization.objects.all()

    def retrieve(self, request, *args, **kwargs):
        organization = self.get_object()
        serializer = PublicOrganizationSerializer(organization)
        if IsOrganizationAdminOrSSOAdmin().has_object_permission(request, self, organization):
            serializer = OrganizationSerializer(organization)
        return Response(serializer.data)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwner,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserSignUpView(APIView):

    def post(self, request, *args, **kwargs):
        serialized = CreateUserSerializer(data=request.data)
        if serialized.is_valid():
            serializer_data = serialized.validated_data
            User.objects.create_user(**serializer_data)
            serializer_data = serialized.data
            serializer_data.pop('password')
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
