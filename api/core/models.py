from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User class created as recommended by Django to reduce
# headaches down the line if a custom implementation is required.


class User(AbstractUser):
    pass


class Client(models.Model):

    company_name = models.CharField(max_length=60)
    membership_expiry = models.DateField()
    description = models.TextField()
    contact_name = models.CharField(max_length=60)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

