from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem, Order
from store.models import Customer
from django.db.models import Q, F, Count


def say_hello(request):
    # query_set = Product.objects.filter(unit_price__range=(1,1000))
    query_set = (
        Order.objects.select_related("customer")
        .prefetch_related("orderitem_set")
        .order_by("-placed_at")[:5]
    )
    query_set2 = Customer.objects.filter(
        Q(membership__icontains="B") & Q(first_name__startswith="F")
    )
    # Grouping data
    grp_data = Customer.objects.annotate(order_count=Count("order"))
    return render(
        request,
        "hello.html",
        {
            "name": "Mosh",
            "orders": list(query_set),
            "customers": query_set2,
            "grp_data": grp_data,
        },
    )
