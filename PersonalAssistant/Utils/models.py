from django.db import models
from django.db.models import ForeignKey
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class UserFiles(models.Model):
    Image = ArrayField(models.CharField(max_length=1000), blank=True, null=True, default=list)
    Documents = ArrayField(models.CharField(max_length=1000), blank=True, null=True, default=list)
    Unknown = ArrayField(models.CharField(max_length=1000), blank=True, null=True, default=list)
    user = ForeignKey(User, on_delete=models.CASCADE)
