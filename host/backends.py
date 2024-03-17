from django.contrib.auth.backends import BaseBackend
from .models import Client

class ClientAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Try to find the client by username/email
            client = Client.objects.get(email=username)
            # Check if the password is correct
            if client.check_password(password):
                return client
        except Client.DoesNotExist:
            # Client not found or password incorrect
            return None
    