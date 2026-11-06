from django.db.models import Sum, F, DecimalField, ExpressionWrapper, Q
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Supplier, Product, StockMovement
from .serializers import CategorySerializer, SupplierSerializer, ProductSerializer, StockMovementSerializer

class BaseReadWriteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

class CategoryViewSet(BaseReadWriteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ["name", "description"]
    ordering_fields = ["name"]

class SupplierViewSet(BaseReadWriteViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    search_fields = ["name", "contact_person", "phone", "email"]
    ordering_fields = ["name"]

class ProductViewSet(BaseReadWriteViewSet):
    queryset = Product.objects.select_related("category", "supplier").all()
    serializer_class = ProductSerializer
    search_fields = ["sku", "name", "category__name", "location"]
    ordering_fields = ["name", "quantity", "purchase_price", "updated_at"]

class StockMovementViewSet(BaseReadWriteViewSet):
    queryset = StockMovement.objects.select_related("product").all()
    serializer_class = StockMovementSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "quantity"]

class SummaryReportView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all()
        total_products = products.count()
        total_units = products.aggregate(total=Sum("quantity"))["total"] or 0
        stock_value = products.aggregate(
            total=Sum(ExpressionWrapper(F("purchase_price") * F("quantity"),
                                       output_field=DecimalField(max_digits=18, decimal_places=2)))
        )["total"] or 0
        low_stock = products.filter(quantity__lte=F("minimum_quantity")).count()
        movements = StockMovement.objects.aggregate(
            incoming=Sum("quantity", filter=Q(movement_type="IN")),
            outgoing=Sum("quantity", filter=Q(movement_type="OUT")),
        )
        return Response({
            "total_products": total_products,
            "total_units": total_units,
            "stock_value": str(stock_value),
            "low_stock_products": low_stock,
            "incoming_units": movements["incoming"] or 0,
            "outgoing_units": movements["outgoing"] or 0,
            "categories": Category.objects.count(),
            "suppliers": Supplier.objects.count(),
        })
