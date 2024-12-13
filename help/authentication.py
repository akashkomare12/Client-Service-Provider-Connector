from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Client,ServiceProvider

class ClientBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            client = Client.objects.get(username=username)
        except Client.DoesNotExist:
            return None

        if check_password(password, client.password):
            return client
        return None

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None
        
class ServiceProverBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            service_provider = ServiceProvider.objects.get(username=username)
        except ServiceProvider.DoesNotExist:
            return None

        if check_password(password, service_provider.password):
            return service_provider
        return None

    def get_user(self, user_id):
        try:
            return ServiceProvider.objects.get(pk=user_id)
        except ServiceProvider.DoesNotExist:
            return None
