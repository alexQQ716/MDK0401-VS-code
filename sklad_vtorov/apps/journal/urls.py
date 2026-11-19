from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import StockMovementViewSet
router = DefaultRouter()
router.register("movements", StockMovementViewSet)
urlpatterns = [path("api/", include(router.urls))]
