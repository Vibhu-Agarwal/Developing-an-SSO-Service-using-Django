from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from users.serializers import UserSerializer
from users.permissions import (IsUserOwner, IsSSOAdmin)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

User = get_user_model()


class UserProfileView(RetrieveUpdateAPIView):

    permission_classes = (IsUserOwner,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):

    permission_classes = (IsAuthenticated, IsSSOAdmin,)
    authentication_classes = (JWTTokenUserAuthentication,)
    serializer_class = UserSerializer
