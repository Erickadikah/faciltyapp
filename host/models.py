from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    userName = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=120, unique=True, default='')  # Default value is an empty string
    rentPayDate = models.DateField()
    rentEndDate = models.DateField()
    
    password = models.CharField(max_length=128)

    # Specify unique related_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',  # Specify a unique related_name
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',  # Specify a unique related_name
        related_query_name='user'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'userName'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.userName

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming a one-to-many relationship with User
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any additional fields as needed, such as attachments, sender, etc.

    def __str__(self):
        return f'Message from {self.user.userName} at {self.created_at}'
