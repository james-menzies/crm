from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User class created as recommended by Django to reduce
# headaches down the line if a custom implementation is required.


class User(AbstractUser):
    pass


class Client(models.Model):
    company_name = models.CharField(max_length=60)
    membership_expiry = models.DateField()
    description = models.TextField(null=True)
    contact_name = models.CharField(max_length=60)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)


class Membership(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField()
    price = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    non_member_price = models.IntegerField()
    member_price = models.IntegerField()


class Order(models.Model):
    order_date = models.DateField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_total = models.IntegerField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)


class OrderItem(models.Model):
    TYPE_CHOICES = [
        ('membership', 'Membership'),
        ('product', 'Product'),

    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    price_per_unit = models.IntegerField(blank=True)
    subtotal = models.IntegerField(blank=True)


