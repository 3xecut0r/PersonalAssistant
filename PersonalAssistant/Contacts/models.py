from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.core.validators import EmailValidator


class Contact(models.Model):
    
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(validators=[EmailValidator(message="Invalid email address")])
    birthday = models.DateField()
    user = ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['name']
