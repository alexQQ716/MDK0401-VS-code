from django.contrib import admin
from .models import StockMovement

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("created_at", "product", "movement_type", "quantity", "document_number", "created_by")
    list_filter = ("movement_type", "created_at")
    search_fields = ("product__name", "product__sku", "document_number")
    readonly_fields = ("created_at",)
    def save_model(self, request, obj, form, change):
        if not change and not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
