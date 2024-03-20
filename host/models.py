from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import make_password
import random
import string

CustomUser = get_user_model()

class Client(models.Model):
    raw_password = models.CharField(max_length=128, blank=True, null=True)
    creator_id = models.IntegerField()
    username = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=120)
    rentPayDate = models.DateField()
    rentEndDate = models.DateField()
    password = models.CharField(max_length=128, blank=True)  # Make sure the field allows blank values
    
    def save(self, *args, **kwargs):
        if not self.password:  # Check if a password is provided
            self.password = self.generate_random_password()  # Generate a random password if not provided
        else:
            self.password = make_password(self.password)  # Hash the provided password
        super().save(*args, **kwargs)
    
    def generate_random_password(self):
        # Generate a random password of length 8
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    def __str__(self):
        return self.username
    
class GuestPermission(models.Model):
    class Meta:
        permissions = [
            ('can_login_as_guest', 'Can log in as guest'),
            ('cant_login_as_host', 'Can not log in as host')
        ]

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    file = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"