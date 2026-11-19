from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    description = models.TextField("Описание", blank=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    def __str__(self): return self.name

class Supplier(models.Model):
    name = models.CharField("Наименование поставщика", max_length=180)
    contact_person = models.CharField("Контактное лицо", max_length=120, blank=True)
    phone = models.CharField("Телефон", max_length=30, blank=True)
    email = models.EmailField("Электронная почта", blank=True)
    address = models.TextField("Адрес", blank=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField("Наименование товара", max_length=180)
    sku = models.CharField("Артикул", max_length=60, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категория")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name="Поставщик")
    unit = models.CharField("Единица измерения", max_length=20, default="шт.")
    purchase_price = models.DecimalField("Закупочная цена", max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    sale_price = models.DecimalField("Цена продажи", max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    quantity = models.IntegerField("Остаток", default=0)
    minimum_quantity = models.PositiveIntegerField("Минимальный остаток", default=0)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Добавлен", auto_now_add=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    def __str__(self): return f"{self.name} ({self.sku})"
    @property
    def is_low_stock(self): return self.quantity <= self.minimum_quantity
