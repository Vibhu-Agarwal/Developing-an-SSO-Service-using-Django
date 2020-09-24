from django.urls import path
from api_app import views

app_name = 'api_app'

urlpatterns = [
    path('protected-resource/', views.HelloPythonistaAPIView.as_view(), name='fetch-protected-resource'),
]
