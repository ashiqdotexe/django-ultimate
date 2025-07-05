from django.urls import path,include
from .views import ProductViewSet,CollectionViewSet, ReviewViewSet, CartViewSet, CartItemViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("product", viewset=ProductViewSet, basename="product")
router.register("collection", viewset=CollectionViewSet)
router.register("cart", viewset=CartViewSet)
review_router = routers.NestedSimpleRouter(router, "product", lookup="product")
review_router.register("review", ReviewViewSet, basename="product_reviews")
cart_router = routers.NestedSimpleRouter(router,"cart", lookup="cart")
cart_router.register("item", CartItemViewSet, basename="cart-item")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(review_router.urls)),
    path("", include(cart_router.urls))
]



# urlpatterns = [
#     path("product/", ProductList.as_view()),
#     path("product/<int:pk>", ProductDetail.as_view()),
#     path("collection/", CollectionList.as_view()),
#     path("collection/<int:pk>", CollectionDetail.as_view(), name="collection-detail"),
# ]
