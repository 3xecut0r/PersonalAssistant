from django.db import models
from django.db.models import ForeignKey
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class UploadedUserFiles(models.Model):
    href = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=1000, blank=True, null=True)
    category = models.CharField(max_length=1000, blank=True, null=True)
    user = ForeignKey(User, on_delete=models.CASCADE)
