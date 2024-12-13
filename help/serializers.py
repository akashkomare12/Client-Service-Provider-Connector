from rest_framework import serializers
from .models import Client, ServiceProvider, ServiceRecords


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'


class ServiceRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRecords
        fields = '__all__'
