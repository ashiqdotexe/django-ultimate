from django.urls import path
from .views import ProductList, product_id, CollectionList, CollectionDetail

urlpatterns = [
    path("product/", ProductList.as_view()),
    path("product/<int:id>", product_id),
    path("collection/", CollectionList.as_view()),
    path("collection/<int:pk>", CollectionDetail.as_view(), name="collection-detail"),
]
