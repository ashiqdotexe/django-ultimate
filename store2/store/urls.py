from django.urls import path
from .views import product_list,product_id
urlpatterns=[
    path("product/", product_list),
    path("product/<int:id>", product_id),
]