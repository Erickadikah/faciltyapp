# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     phone = models.CharField(max_length=15)
#     address = models.CharField(max_length=100)
#     eircode = models.CharField(max_length=10)
#     country = models.CharField(max_length=50)

#     class Meta:
#         verbose_name = 'Custom User'
#         verbose_name_plural = 'Custom Users'

#     def __str__(self):
#         return self.username
    
    # class host_permission(models.Model):
    #     class Meta:
    #         permissions = [
    #             ('can_login_as_host', 'Can log in as host'),
    #             ('cant_login_as_guest', 'Can not log in as guest'),
    #             ('cant_login_as_client', 'Can not log in as client'),
    #             ('cant_login_as_admin', 'Can not log in as admin'),
    #             ('can_create_client', 'Can create client'),
    #         ]
