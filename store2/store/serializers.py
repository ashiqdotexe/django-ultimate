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

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id"
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description", "date"]
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)