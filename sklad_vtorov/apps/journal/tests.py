from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.catalog.models import Category, Product
from .models import StockMovement
class MovementTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Тест")
        self.product = Product.objects.create(name="Товар", sku="T-1", category=category, quantity=10)
    def test_income_updates_stock(self):
        StockMovement.objects.create(product=self.product, movement_type="IN", quantity=3)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 13)
    def test_expense_updates_stock(self):
        StockMovement.objects.create(product=self.product, movement_type="OUT", quantity=4)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 6)
    def test_cannot_expense_more_than_stock(self):
        with self.assertRaises(ValidationError):
            StockMovement.objects.create(product=self.product, movement_type="OUT", quantity=20)
