from django.db import models

class Collection(models.Model):
    title = models.CharField(max_length=255)

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

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

class Adress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    
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
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

"""
    Foreign Key represents One to Many Relationship
    A customer can have multiple address. So it's a one-to-many
    relationship thats why we use ForeignKEY.
    on_delete = models.CASCADE-> when we want to delete the addresses associated
    with customer... model.PROTECT--> Say for example we deleted the Collection,
    but we don't want to delete Product.

"""