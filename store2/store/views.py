from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CustomerSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer,CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from .models import Customer, Product, Collection, OrderItem, Review, Cart, CartItem
from .filter import ProductFilter
from .pagination import PaginationNumber
from . import permission
from . import serializers
from . import models
"""
API View-->
"""

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

# class CollectionDetail(APIView):
#     def get(self, request, pk):
#         collection = get_object_or_404(
#         Collection.objects.annotate(product_count=Count("products")), pk=pk)
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     def put(self, request,pk):
#         collection = get_object_or_404(
#         Collection.objects.annotate(product_count=Count("products")), pk=pk)
#         serializer = CollectionSerializer(collection, request.data)
#         serializer.is_valid()
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#     def delete(self, request,pk):
#         collection = get_object_or_404(
#         Collection.objects.annotate(product_count=Count("products")), pk=pk)
#         if collection.products.count() > 0:
#             return Response(
#                 {"error": "cant delete item because order item exist"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         collection.delete()
#         return Response(
#             {"message": f"item with {pk} deleted"}, status=status.HTTP_204_NO_CONTENT
#         )






# @api_view(["GET", "POST"])
# def product_list(request):
#     if request.method == "GET":
#         queryset = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(
#             queryset, many=True, context={"request": request}
#         )
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def product_id(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#     elif request.method == "DELETE":
#         if product.orderitem_set.count() > 0:
#             return Response(
#                 {"error": "cant delete item because order item exist"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         product.delete()
#         return Response(
#             {"message": f"item with {id} deleted"}, status=status.HTTP_204_NO_CONTENT
#         )





"""
GENERIC View->
"""
# class CollectionList(ListCreateAPIView):
#     def get_queryset(self):
#         return Collection.objects.annotate(product_count=Count("products")).all()
#     def get_serializer_class(self):
#         return CollectionSerializer
#     def get_parser_context(self, http_request):
#         return {"request": self.request}

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(product_count=Count("products"))
#     serializer_class = CollectionSerializer
#     def delete(self, request, pk):
#         collection = get_object_or_404(
#         Collection.objects.annotate(product_count=Count("products")), pk=pk)
#         if collection.products.count() > 0:
#             return Response(
#                 {"error": "cant delete item because order item exist"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         collection.delete()
#         return Response(
#             {"message": f"item with {pk} deleted"}, status=status.HTTP_204_NO_CONTENT
#         )
        


# class ProductList(ListCreateAPIView):
#     def get_queryset(self):
#         return Product.objects.select_related("collection").all()
#     def get_serializer_class(self):
#         return ProductSerializer
#     def get_serializer_context(self):
#         return {"request": self.request}

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     def delete(self, request, pk):
#          product = get_object_or_404(Product, pk=pk)
#          if product.orderitem_set.count()>0:
#              return Response({"message":"can't delete"}, status=status.HTTP_400_BAD_REQUEST)
#          product.delete()
#          return Response(
#             {"message": f"item with {pk} deleted"}, status=status.HTTP_204_NO_CONTENT
#         )

"""
Viewset->
"""
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    # collection_id = self.request.query_params.get("collection_id")
    # if collection_id is not None:
    #     queryset = queryset.filter(collection_id=collection_id)
    # return queryset
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields =["id","unit_price"]
    pagination_class = PaginationNumber
    serializer_class = ProductSerializer
    permission_classes = [permission.IsAdminOrReadOnly]
    def get_serializer_context(self):
        return {"request": self.request}
    def destroy(self, request, *args, **kwargs):
        if  OrderItem.objects.filter(product_id = kwargs["pk"]).count() > 0:
            return  Response(
                {"error": "cant delete item because order item exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Product created successfully!",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count = Count("products")).all()
    serializer_class = CollectionSerializer
    def get_serializer_context(self):
        return {"request": self.request}
    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.annotate(product_count = Count("products")), pk=kwargs["pk"])
        if collection.products.count() > 0:
            return Response(
                {"error": "cant delete item because product exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)
    
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])
    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}

        
class CartViewSet(CreateModelMixin,DestroyModelMixin,RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related("item__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    def get_serializer_class(self):
        if self.request.method=="POST":
            return AddCartItemSerializer
        if self.request.method=="PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {"cart_id" : self.kwargs["cart_pk"]}
    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs["cart_pk"]).select_related("product")
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    @action(detail=True, permission_classes=[permission.ViewCustomerPermission])
    def history(self, request,pk):
        return Response("ok")
    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, valid) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"user_id":self.request.user.id}
    
    def get_serializer_class(self):
        if self.request.method=="POST":
            return serializers.CreateOrderSerializer
        return serializers.OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return models.Order.objects.all()
        (customer_id, created) = Customer.objects.only("id").get_or_create(user_id = user.id)
        return models.Order.objects.filter(customer_id=customer_id)