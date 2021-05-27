from django.db import models
from datetime import datetime
# Create your models here.

class UploadStudent(models.Model):
    file = models.FileField(upload_to='student/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)


