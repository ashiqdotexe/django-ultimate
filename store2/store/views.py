from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from .models import Product
from rest_framework.response import Response


@api_view()
def product_list(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many = True)
    return Response(serializer.data)
