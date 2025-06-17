from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem
def say_hello(request):
    # query_set = Product.objects.filter(title__istartswith="Coffee") -- starts with coffee
    query_set = Product.objects.filter(OrderItem.objects.values("product_id").distinct()).order_by("title")
    return render(request, 'hello.html', {'name': 'Mosh', "products":list(query_set)})
