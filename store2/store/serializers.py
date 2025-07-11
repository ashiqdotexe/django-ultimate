from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem


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