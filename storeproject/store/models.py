from django.db import models
class Collection(models.Model):
    title = models.CharField(max_length=255)

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digit=6, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
class Customer(models.Model):
    BRONZE = "B"
    SILVER = "S"
    GOLD ="G"

    MEMBERSHIP_CHOICES = [
        (BRONZE , "B"),
        (SILVER , "S"),
        (GOLD , "G"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phone = models.IntegerField(max_length=15)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=255, choices=MEMBERSHIP_CHOICES)
class Order(models.Model):
    PENDING = "P"
    COMPLETE = "C"
    FAILED ="F"

    ORDER_CHOICES = [
        (PENDING, "Pending"),
        (COMPLETE, "Complete"),
        (FAILED, "Faled"),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=255, choices=ORDER_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField()

class Cart(models.Model):
    created_at= models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

class Adresses(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    
