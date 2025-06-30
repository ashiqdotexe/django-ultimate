from django.urls import path
from .views import ProductViewSet,CollectionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("product", viewset=ProductViewSet)
router.register("collection", viewset=CollectionViewSet)

urlpatterns = router.urls



# urlpatterns = [
#     path("product/", ProductList.as_view()),
#     path("product/<int:pk>", ProductDetail.as_view()),
#     path("collection/", CollectionList.as_view()),
#     path("collection/<int:pk>", CollectionDetail.as_view(), name="collection-detail"),
# ]
