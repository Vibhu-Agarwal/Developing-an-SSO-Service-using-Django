from users.views import UserProfileView, UserCreateAPIView
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('user/<int:pk>/', UserProfileView.as_view(), name='user-retrieve-update-api'),
    path('user/create/', UserCreateAPIView.as_view(), name='user-create-callback-url'),
]
