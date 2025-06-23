from django.urls import path
from .views import product_list, product_id, collection_detail, collection_list

urlpatterns = [
    path("product/", product_list),
    path("product/<int:id>", product_id),
    path("collection/", collection_list),
    path("collection/<int:pk>", collection_detail, name="collection-detail"),
]
