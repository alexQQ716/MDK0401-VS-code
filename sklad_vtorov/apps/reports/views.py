from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import render
from apps.catalog.models import Product, Category, Supplier
from apps.journal.models import StockMovement

@login_required
def home(request):
    products = Product.objects.select_related("category", "supplier")
    context = {
        "product_count": products.count(),
        "category_count": Category.objects.count(),
        "supplier_count": Supplier.objects.count(),
        "low_stock": products.filter(quantity__lte=F("minimum_quantity")),
        "recent_movements": StockMovement.objects.select_related("product")[:10],
        "stock_value": products.aggregate(total=Sum(ExpressionWrapper(F("quantity") * F("purchase_price"), output_field=DecimalField())))["total"] or 0,
    }
    return render(request, "reports/home.html", context)

@login_required
def summary_api(request):
    from django.http import JsonResponse
    return JsonResponse({
        "products": Product.objects.count(),
        "categories": Category.objects.count(),
        "suppliers": Supplier.objects.count(),
        "movements": StockMovement.objects.count(),
        "low_stock": Product.objects.filter(quantity__lte=F("minimum_quantity")).count(),
    })
