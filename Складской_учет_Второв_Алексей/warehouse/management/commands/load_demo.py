from decimal import Decimal
from django.core.management.base import BaseCommand
from warehouse.models import Category, Supplier, Product

class Command(BaseCommand):
    help = "Добавляет демонстрационные категории, поставщиков и товары"

    def handle(self, *args, **options):
        office, _ = Category.objects.get_or_create(name="Канцелярия")
        tech, _ = Category.objects.get_or_create(name="Техника")
        supplier, _ = Supplier.objects.get_or_create(
            name="ООО «Учебный поставщик»",
            defaults={"phone": "+7 900 000-00-00", "email": "supplier@example.com"}
        )
        demo = [
            ("PEN-001", "Ручка синяя", office, Decimal("15.50"), 120, 20, "Стеллаж A-1"),
            ("PAP-002", "Бумага A4", office, Decimal("320.00"), 35, 10, "Стеллаж A-2"),
            ("MOU-003", "Мышь компьютерная", tech, Decimal("650.00"), 8, 5, "Стеллаж B-1"),
        ]
        for sku, name, category, price, qty, minimum, location in demo:
            Product.objects.get_or_create(
                sku=sku,
                defaults={"name": name, "category": category, "supplier": supplier,
                          "purchase_price": price, "quantity": qty,
                          "minimum_quantity": minimum, "location": location}
            )
        self.stdout.write(self.style.SUCCESS("Демонстрационные данные добавлены."))
