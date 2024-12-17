from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from store.models import Customer
from django.db.models import Q, F


def say_hello(request):
    # query_set = Product.objects.filter(unit_price__range=(1,1000))
    query_set = Product.objects.earliest('unit_price')
    query_set2 = Customer.objects.filter(Q(membership__icontains = 'B') & Q(first_name__startswith="F"))
    return render(request, 'hello.html', {'name': 'Mosh', 'products': query_set, 'customers' : query_set2})
