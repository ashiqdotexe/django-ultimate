from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "featured_product"]
class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_on_tax = serializers.SerializerMethodField(
        method_name = "tax_on_price"
    )
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

    #Another way to show this-->(ModelSerializer)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price',"price_on_tax", 'inventory', 'collection']


    def tax_on_price(self, product: Product):
        return product.unit_price * Decimal(1.1)