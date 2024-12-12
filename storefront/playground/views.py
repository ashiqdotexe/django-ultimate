from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product




def say_hello(request):
    query_set = Product.objects.filter(unit_price__range=(1,1000))
    return render(request, 'hello.html', {'name': 'Mosh', 'products': list(query_set)})
