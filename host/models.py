from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Client(models.Model):
    username = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=120)
    rentPayDate = models.DateField()
    rentEndDate = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
