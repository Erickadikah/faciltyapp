# models.py

from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phoneNumber, rentPayDate, rentEndDate, **extra_fields):
        """
        Create and return a regular user with an email, username, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phoneNumber=phoneNumber,
            rentPayDate=rentPayDate,
            rentEndDate=rentEndDate,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phoneNumber, rentPayDate, rentEndDate, **extra_fields):
        """
        Create and return a superuser with an email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, phoneNumber, rentPayDate, rentEndDate, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=120, unique=True)
    rentPayDate = models.DateField()
    rentEndDate = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phoneNumber', 'rentPayDate', 'rentEndDate']

    def __str__(self):
        return self.username


class User(models.Model):
    userName = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=120, unique=True)
    rentPayDate = models.DateField()
    rentEndDate = models.DateField()

    def __str__(self):
        return self.userName

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming a one-to-many relationship with User
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any additional fields as needed, such as attachments, sender, etc.

    def __str__(self):
        return f'Message from {self.user.username} at {self.created_at}'