from decimal import Decimal
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_on_tax = serializers.SerializerMethodField(
        method_name = "tax_on_price"
    )
    def tax_on_price(self, product: Product):
        return product.unit_price * Decimal(1.1)