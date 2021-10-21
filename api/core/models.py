from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User class created as recommended by Django to reduce
# headaches down the line if a custom implementation is required.
class User(AbstractUser):
    pass

