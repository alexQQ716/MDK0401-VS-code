from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Category, Supplier, Product, StockMovement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    stock_value = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "sku", "name", "category", "category_name", "supplier", "supplier_name",
                  "unit", "purchase_price", "quantity", "minimum_quantity", "location",
                  "description", "stock_value", "is_low_stock", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    movement_type_display = serializers.CharField(source="get_movement_type_display", read_only=True)

    class Meta:
        model = StockMovement
        fields = ["id", "product", "product_name", "movement_type", "movement_type_display",
                  "quantity", "document_number", "note", "created_at", "created_by"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        try:
            return StockMovement.objects.create(**validated_data)
        except ValidationError as exc:
            raise serializers.ValidationError({"detail": exc.messages})
