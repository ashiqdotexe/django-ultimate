from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from store.models import Customer



def say_hello(request):
    query_set = Product.objects.filter(unit_price__range=(1,1000))
    query_set2 = Customer.objects.filter(membership__icontains = 'B')
    return render(request, 'hello.html', {'name': 'Mosh', 'products': list(query_set), 'customers' : query_set2})
