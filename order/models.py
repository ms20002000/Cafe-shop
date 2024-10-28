from django.core.exceptions import ValidationError
from django.db import models
from account.models import CustomUser
from product.models import Product, Category
from django.utils.translation import gettext_lazy as _

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    qr_code = models.CharField(max_length=200)

    def __str__(self):
        return str(self.number)

class Order(models.Model):

    class StatusOrder(models.TextChoices):
        PENDING = "P", _("Pending")
        REGISTERED = "R", _("Registered")
        APPROVED = "A", _("Approved")
        CANCELLED = "CA", _("Cancelled")
        COOKING = "CK", _("Cooking")
        COMPLETED = "C", _("Completed")


    class PaymentMethod(models.TextChoices):
        CASH = "C", _("Cash")
        INTERNET = "I", _("Internet")

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=StatusOrder.choices, default=StatusOrder.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=20, default=PaymentMethod.CASH, choices=PaymentMethod.choices)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    modify_by = models.ForeignKey(CustomUser, default=1, on_delete=models.CASCADE)

    def total_items_count(self):
        return sum(item.quantity for item in self.items.all())
    
    def total_price_amount(self):
        return sum(item.total_price() for item in self.items.all())

    def clean(self):
        if self.status == 'P' and Order.objects.filter(table=self.table, status='P').exclude(pk=self.pk).exists():
            raise ValidationError(f'Table {self.table} already has a pending order.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.id} by {self.modify_by.phone_number}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', default=1)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
