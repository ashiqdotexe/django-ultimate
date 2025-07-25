from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem, Customer,Order,OrderItem
from .signals import order_created

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "product_count"]

    product_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_on_tax = serializers.SerializerMethodField(method_name="tax_on_price")
    # #Calling relationalField 3 ways->
    # #1.
    # collection = serializers.StringRelatedField()
    # #2.
    # collection = CollectionSerializer()

    # #3.
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Product.objects.all(),
    #     view_name = "collection-detail"
    # )

    # Another way to show this-->(ModelSerializer)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "unit_price",
            "price_on_tax",
            "inventory",
            "collection",
        ]

    def tax_on_price(self, product: Product):
        return product.unit_price * Decimal(1.1)
    

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()
    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "total_price"
        ]

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    item = CartItemSerializer(many = True, read_only= True)
    total_price = serializers.SerializerMethodField(read_only= True)

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.item.all()])
    class Meta:
        model = Cart
        fields = [
            "id","item","total_price"
        ]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            return serializers.ValidationError("No such product")
        return value
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance=cart_item
            #Updating
        except:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            #creating newobjects
    class Meta:
        model = CartItem
        fields = ["id", "product_id","quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description", "date"]
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)
    
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]



class CustomOrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["id","product"]

class OrderSerializer(serializers.ModelSerializer):
    item = CustomOrderItemSerializer(many = True, read_only=True)
    class Meta:
        model = Order
        fields = ["id","customer","payment_status","placed_at", "item"]

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status"]

class CreateOrderSerializer(serializers.Serializer):
    with transaction.atomic():
    
        cart_id = serializers.UUIDField()

        def validate_cart_id(self, cart_id):
            if not Cart.objects.filter(pk=cart_id).exists():
                raise serializers.ValidationError("No such cart")
            if CartItem.objects.filter(cart_id=cart_id).count()==0:
                raise serializers.ValidationError("No item in the cart")
            return cart_id
        
        def save(self, **kwargs):
            print(self.context["user_id"])
            customer= Customer.objects.get(user_id=self.context["user_id"])
            order= Order.objects.create(customer=customer)
            cart_items = CartItem.objects.select_related("product").filter(cart_id = self.validated_data["cart_id"])
            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=self.validated_data["cart_id"]).delete()
            order_created.send_robust(self.__class__, order = order)
            return order