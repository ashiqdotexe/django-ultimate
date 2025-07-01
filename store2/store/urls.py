from django.urls import path,include
from .views import ProductViewSet,CollectionViewSet, ReviewViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("product", viewset=ProductViewSet)
router.register("collection", viewset=CollectionViewSet)
nested_router = routers.NestedSimpleRouter(router, "product", lookup="product")
nested_router.register("review", ReviewViewSet, basename="product_reviews")
urlpatterns = [
    path("", include(router.urls)),
    path("", include(nested_router.urls))
]



# urlpatterns = [
#     path("product/", ProductList.as_view()),
#     path("product/<int:pk>", ProductDetail.as_view()),
#     path("collection/", CollectionList.as_view()),
#     path("collection/<int:pk>", CollectionDetail.as_view(), name="collection-detail"),
# ]
