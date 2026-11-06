# Generated for the educational warehouse inventory application.
import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=100, unique=True, verbose_name="Название категории")), ("description", models.TextField(blank=True, verbose_name="Описание"))],
            options={"verbose_name": "категория", "verbose_name_plural": "Категории", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=160, unique=True, verbose_name="Наименование поставщика")), ("contact_person", models.CharField(blank=True, max_length=120, verbose_name="Контактное лицо")), ("phone", models.CharField(blank=True, max_length=30, verbose_name="Телефон")), ("email", models.EmailField(blank=True, max_length=254, verbose_name="Электронная почта")), ("address", models.CharField(blank=True, max_length=250, verbose_name="Адрес"))],
            options={"verbose_name": "поставщик", "verbose_name_plural": "Поставщики", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("sku", models.CharField(max_length=40, unique=True, verbose_name="Артикул")), ("name", models.CharField(max_length=180, verbose_name="Название товара")), ("unit", models.CharField(default="шт.", max_length=20, verbose_name="Единица измерения")), ("purchase_price", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))], verbose_name="Закупочная цена")), ("quantity", models.PositiveIntegerField(default=0, verbose_name="Остаток")), ("minimum_quantity", models.PositiveIntegerField(default=0, verbose_name="Минимальный остаток")), ("location", models.CharField(blank=True, max_length=80, verbose_name="Место хранения")), ("description", models.TextField(blank=True, verbose_name="Описание")), ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")), ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")), ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="warehouse.category", verbose_name="Категория")), ("supplier", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="products", to="warehouse.supplier", verbose_name="Поставщик"))],
            options={"verbose_name": "товар", "verbose_name_plural": "Товары", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="StockMovement",
            fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("movement_type", models.CharField(choices=[("IN", "Поступление"), ("OUT", "Списание")], max_length=3, verbose_name="Тип операции")), ("quantity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name="Количество")), ("document_number", models.CharField(blank=True, max_length=60, verbose_name="Номер документа")), ("note", models.CharField(blank=True, max_length=250, verbose_name="Комментарий")), ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата операции")), ("created_by", models.CharField(blank=True, max_length=120, verbose_name="Ответственный")), ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="movements", to="warehouse.product", verbose_name="Товар"))],
            options={"verbose_name": "движение товара", "verbose_name_plural": "Движения товаров", "ordering": ["-created_at"]},
        ),
    ]
