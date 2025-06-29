from django.urls import path
from .views import ProductList, ProductDetail, CollectionList, CollectionDetail

urlpatterns = [
    path("product/", ProductList.as_view()),
    path("product/<int:pk>", ProductDetail.as_view()),
    path("collection/", CollectionList.as_view()),
    path("collection/<int:pk>", CollectionDetail.as_view(), name="collection-detail"),
]
