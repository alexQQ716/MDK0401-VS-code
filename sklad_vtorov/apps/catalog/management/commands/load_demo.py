from django.core.management.base import BaseCommand
from apps.catalog.models import Category, Supplier, Product

class Command(BaseCommand):
    help = "Добавляет демонстрационные категории, поставщиков и товары"
    def handle(self, *args, **options):
        office, _ = Category.objects.get_or_create(name="Канцелярия")
        tech, _ = Category.objects.get_or_create(name="Техника")
        supplier, _ = Supplier.objects.get_or_create(name="ООО Поставка", defaults={"phone": "+7 900 000-00-00"})
        samples = [
            ("Бумага А4", "DEMO-001", office, 50, 10, "пач."),
            ("Ручка синяя", "DEMO-002", office, 100, 20, "шт."),
            ("Клавиатура", "DEMO-003", tech, 8, 3, "шт."),
        ]
        for name, sku, category, qty, minimum, unit in samples:
            Product.objects.get_or_create(sku=sku, defaults={"name": name, "category": category, "supplier": supplier, "quantity": qty, "minimum_quantity": minimum, "unit": unit, "purchase_price": 100, "sale_price": 150})
        self.stdout.write(self.style.SUCCESS("Демонстрационные данные добавлены."))
