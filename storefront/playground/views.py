from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem, Order, Collection
from store.models import Customer
from django.db.models import Q, F, Count, ExpressionWrapper, DecimalField


def say_hello(request):
    # query_set = Product.objects.filter(unit_price__range=(1,1000))
    query_set = (
        Order.objects.select_related("customer")
        .prefetch_related("orderitem_set")
        .order_by("-placed_at")[:5]
    )

    # Grouping data
    grp_data = Customer.objects.annotate(order_count=Count("order"))
    discounted_price = ExpressionWrapper(
        F("unit_price") * 0.8, output_field=DecimalField(max_digits=6, decimal_places=0)
    )
    query_set2 = Product.objects.annotate(discounted_price=discounted_price)
    ##Creating objects----
    collection = Collection()
    collection.title = "Video Game"
    collection.featured_product = Product(pk=1)
    collection.save()
    return render(
        request,
        "hello.html",
        {
            "name": "Mosh",
            "orders": list(query_set),
            "products": query_set2,
            "grp_data": grp_data,
        },
    )
