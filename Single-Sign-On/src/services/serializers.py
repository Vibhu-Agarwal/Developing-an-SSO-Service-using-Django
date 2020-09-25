from rest_framework.serializers import ModelSerializer
from .models import Service, Connection


class PublicServiceSerializer(ModelSerializer):

    class Meta:
        model = Service
        fields = ('id', 'name', 'identifier',)


class ServiceSerializer(ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class ConnectionSerializer(ModelSerializer):

    class Meta:
        model = Connection
        fields = '__all__'
