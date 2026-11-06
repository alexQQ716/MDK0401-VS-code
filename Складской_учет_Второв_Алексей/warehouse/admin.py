from django.contrib import admin
from .models import Category, Supplier, Product, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "phone", "email")
    search_fields = ("name", "contact_person", "phone", "email")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category", "quantity", "minimum_quantity", "purchase_price", "location", "low_stock")
    list_filter = ("category", "supplier")
    search_fields = ("sku", "name", "location")
    readonly_fields = ("created_at", "updated_at")

    @admin.display(boolean=True, description="Низкий остаток")
    def low_stock(self, obj):
        return obj.is_low_stock

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("created_at", "product", "movement_type", "quantity", "document_number", "created_by")
    list_filter = ("movement_type", "created_at")
    search_fields = ("product__name", "product__sku", "document_number")
    readonly_fields = ("created_at",)
