from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem, Order
def say_hello(request):
    # query_set = Product.objects.filter(title__istartswith="Coffee") -- starts with coffee
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values("product_id").distinct()).order_by("title")[:5]
    query_set = Order.objects.select_related("customer").prefetch_related("orderitem_set__product").order_by("-placed_at")[:5]
    return render(request, 'hello.html', {'name': 'Mosh', "orders":list(query_set)})
