from django.db import models

"""
    *Foreign Key represents One to Many Relationship
    *A customer can have multiple address. So it's a one-to-many
    relationship thats why we use ForeignKEY.
    *A Promotion can have multiple product and vice-verca. So its a 
    many-to-many relationship
    *on_delete = models.CASCADE-> when we want to delete the addresses associated
    with customer.
    *model.PROTECT--> Say for example we deleted the Collection,
    but we don't want to delete Product.
    
"""

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product= models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name="+")

class Promtion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    product = models.ManyToManyField(Promtion)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICE = [
        (MEMBERSHIP_BRONZE, 'BRONZE'),
        (MEMBERSHIP_SILVER, 'SILVER'),
        (MEMBERSHIP_GOLD, 'GOLD'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birtdate = models.DateField(null=True)
    choices = models.CharField(max_length=15,choices=MEMBERSHIP_CHOICE, default=MEMBERSHIP_BRONZE)

class Adress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
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