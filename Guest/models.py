# models.py
from django.db import models
from django.contrib.auth.models import User

class UploadedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100)
    document_type = models.CharField(max_length=50)
    upload_file = models.FileField(upload_to='uploads/%Y/%m/%d/')  # Specifying the upload directory

    def __str__(self):
        return self.document_name
