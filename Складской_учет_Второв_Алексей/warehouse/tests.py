from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .models import Category, Supplier, Product, StockMovement

class WarehouseTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Канцелярия")
        self.supplier = Supplier.objects.create(name="Учебный поставщик")
        self.product = Product.objects.create(
            sku="PEN-001", name="Ручка", category=self.category, supplier=self.supplier,
            purchase_price=Decimal("15.50"), quantity=10, minimum_quantity=2
        )

    def test_incoming_movement_increases_stock(self):
        StockMovement.objects.create(product=self.product, movement_type="IN", quantity=5)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 15)

    def test_outgoing_movement_decreases_stock(self):
        StockMovement.objects.create(product=self.product, movement_type="OUT", quantity=4)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 6)

    def test_cannot_write_off_more_than_available(self):
        with self.assertRaises(ValidationError):
            StockMovement.objects.create(product=self.product, movement_type="OUT", quantity=11)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)

    def test_products_api_returns_list(self):
        client = APIClient()
        response = client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_summary_report(self):
        response = APIClient().get("/api/reports/summary/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_products"], 1)
        self.assertEqual(response.data["total_units"], 10)
