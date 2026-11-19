from django.test import TestCase
from .models import Category, Product
class CatalogTests(TestCase):
    def test_product_string(self):
        category = Category.objects.create(name="Канцелярия")
        product = Product.objects.create(name="Бумага", sku="P-001", category=category, quantity=5)
        self.assertIn("Бумага", str(product))
