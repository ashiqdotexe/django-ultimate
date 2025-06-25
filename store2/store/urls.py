from django.urls import path
from .views import product_list, product_id, CollectionList, CollectionDetail

urlpatterns = [
    path("product/", product_list),
    path("product/<int:id>", product_id),
    path("collection/", CollectionList.as_view()),
    path("collection/<int:pk>", CollectionDetail.as_view(), name="collection-detail"),
]
