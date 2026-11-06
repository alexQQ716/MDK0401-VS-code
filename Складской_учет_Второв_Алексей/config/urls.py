from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from warehouse.views import CategoryViewSet, SupplierViewSet, ProductViewSet, StockMovementViewSet, SummaryReportView

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("suppliers", SupplierViewSet, basename="supplier")
router.register("products", ProductViewSet, basename="product")
router.register("movements", StockMovementViewSet, basename="movement")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/reports/summary/", SummaryReportView.as_view(), name="summary-report"),
]
