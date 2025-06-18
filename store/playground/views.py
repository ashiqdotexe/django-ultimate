from django.shortcuts import render
from django.db.models import F,ExpressionWrapper, DecimalField
from django.db import transaction
from store.models import Product, OrderItem, Order, Collection
def say_hello(request):
    # query_set = Product.objects.filter(title__istartswith="Coffee") -- starts with coffee
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values("product_id").distinct()).order_by("title")[:5]
    # query_set = Order.objects.select_related("customer").prefetch_related("orderitem_set__product").order_by("-placed_at")[:5]
    # query_set = Product.objects.annotate(new_id = F("id")+1)
    # discount = ExpressionWrapper(F("unit_price")*0.8, output_field=DecimalField(decimal_places=0))
    # query_set = Product.objects.annotate(discounted_price = discount)

    #Creating Updating and Deleting->
    with transaction.atomic():
        collection = Collection()
        collection.title = "Video Games"
        collection.save()
    
    return render(request, 'hello.html', {'name': 'Mosh', "orders":list(query_set)})
