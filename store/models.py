from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    last_update = models.DateTimeField(auto_now=True)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICE = [
        (MEMBERSHIP_BRONZE, 'BRONZE'),
        (MEMBERSHIP_SILVER, 'SILVER'),
        (MEMBERSHIP_GOLD, 'GOLD'),
    ]
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=8)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(max_length=11)
    birtdate = models.DateField(null=True)
    choices = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICE, default=MEMBERSHIP_BRONZE)

class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'P'
    PAYMENT_STATUS = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'FAILED'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    choices = models.CharField(max_length=255, choices=PAYMENT_STATUS, default=PAYMENT_PENDING)
