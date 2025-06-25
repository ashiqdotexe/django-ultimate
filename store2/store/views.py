from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection
from rest_framework.response import Response
from rest_framework import status


# class CollectionList(APIView):
#     def get(self, request):
#         query_set = Collection.objects.annotate(product_count=Count("products")).all()
#         serializer = CollectionSerializer(
#             query_set, many=True, context={"request": request}
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self, request):
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
"""
GENERIC View->
"""
class CollectionList(ListCreateAPIView):
    def get_queryset(self):
        return Collection.objects.annotate(product_count=Count("products")).all()
    def get_serializer_class(self):
        return CollectionSerializer
    def get_parser_context(self, http_request):
        return {"request": self.request}

class CollectionDetail(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(
        Collection.objects.annotate(product_count=Count("products")), pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    def put(self, request,pk):
        collection = get_object_or_404(
        Collection.objects.annotate(product_count=Count("products")), pk=pk)
        serializer = CollectionSerializer(collection, request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    def delete(self, request,pk):
        collection = get_object_or_404(
        Collection.objects.annotate(product_count=Count("products")), pk=pk)
        if collection.products.count() > 0:
            return Response(
                {"error": "cant delete item because order item exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        collection.delete()
        return Response(
            {"message": f"item with {pk} deleted"}, status=status.HTTP_204_NO_CONTENT
        )
        


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def product_id(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == "DELETE":
        if product.orderitem_set.count() > 0:
            return Response(
                {"error": "cant delete item because order item exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product.delete()
        return Response(
            {"message": f"item with {id} deleted"}, status=status.HTTP_204_NO_CONTENT
        )
