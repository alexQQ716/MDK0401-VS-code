from django.conf import settings
from django.db import models, transaction
from django.core.exceptions import ValidationError
from apps.catalog.models import Product

class StockMovement(models.Model):
    INCOME = "IN"
    EXPENSE = "OUT"
    TYPES = [(INCOME, "Поступление"), (EXPENSE, "Списание")]
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="movements", verbose_name="Товар")
    movement_type = models.CharField("Тип операции", max_length=3, choices=TYPES)
    quantity = models.PositiveIntegerField("Количество")
    document_number = models.CharField("Номер документа", max_length=80, blank=True)
    comment = models.TextField("Комментарий", blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    created_at = models.DateTimeField("Дата операции", auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Складское движение"
        verbose_name_plural = "Складские движения"
    def __str__(self): return f"{self.get_movement_type_display()}: {self.product} — {self.quantity}"
    def clean(self):
        if self.quantity <= 0:
            raise ValidationError({"quantity": "Количество должно быть больше нуля."})
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Сохранённую операцию нельзя изменять. Создайте корректирующую операцию.")
        self.full_clean()
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=self.product_id)
            if self.movement_type == self.INCOME:
                product.quantity += self.quantity
            elif self.movement_type == self.EXPENSE:
                if product.quantity < self.quantity:
                    raise ValidationError({"quantity": "Недостаточно товара на складе."})
                product.quantity -= self.quantity
            else:
                raise ValidationError({"movement_type": "Неизвестный тип операции."})
            product.save(update_fields=["quantity"])
            super().save(*args, **kwargs)
