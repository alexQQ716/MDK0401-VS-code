from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField("Название категории", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField("Наименование поставщика", max_length=160, unique=True)
    contact_person = models.CharField("Контактное лицо", max_length=120, blank=True)
    phone = models.CharField("Телефон", max_length=30, blank=True)
    email = models.EmailField("Электронная почта", blank=True)
    address = models.CharField("Адрес", max_length=250, blank=True)

    class Meta:
        verbose_name = "поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField("Артикул", max_length=40, unique=True)
    name = models.CharField("Название товара", max_length=180)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категория")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name="Поставщик")
    unit = models.CharField("Единица измерения", max_length=20, default="шт.")
    purchase_price = models.DecimalField("Закупочная цена", max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    quantity = models.PositiveIntegerField("Остаток", default=0)
    minimum_quantity = models.PositiveIntegerField("Минимальный остаток", default=0)
    location = models.CharField("Место хранения", max_length=80, blank=True)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self):
        return f"{self.sku} — {self.name}"

    @property
    def stock_value(self):
        return self.purchase_price * self.quantity

    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_quantity

class StockMovement(models.Model):
    IN = "IN"
    OUT = "OUT"
    TYPE_CHOICES = [(IN, "Поступление"), (OUT, "Списание")]
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="movements", verbose_name="Товар")
    movement_type = models.CharField("Тип операции", max_length=3, choices=TYPE_CHOICES)
    quantity = models.PositiveIntegerField("Количество", validators=[MinValueValidator(1)])
    document_number = models.CharField("Номер документа", max_length=60, blank=True)
    note = models.CharField("Комментарий", max_length=250, blank=True)
    created_at = models.DateTimeField("Дата операции", auto_now_add=True)
    created_by = models.CharField("Ответственный", max_length=120, blank=True)

    class Meta:
        verbose_name = "движение товара"
        verbose_name_plural = "Движения товаров"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_movement_type_display()}: {self.product} × {self.quantity}"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Сохранённое движение нельзя изменять: создайте корректирующую операцию.")
        if not self.quantity or self.quantity < 1:
            raise ValidationError("Количество должно быть не меньше 1.")
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=self.product_id)
            if self.movement_type == self.IN:
                product.quantity += self.quantity
            elif self.movement_type == self.OUT:
                if product.quantity < self.quantity:
                    raise ValidationError(f"Недостаточно товара на складе. Доступно: {product.quantity}.")
                product.quantity -= self.quantity
            else:
                raise ValidationError("Неизвестный тип движения.")
            product.save(update_fields=["quantity", "updated_at"])
            super().save(*args, **kwargs)
