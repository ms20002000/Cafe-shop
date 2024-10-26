from django.db import models
from account.models import CustomUser
from product.models import Product, Category

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    qr_code = models.CharField(max_length=200)

    def __str__(self):
        return str(self.number)

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('P', 'Pending'), ('C', 'Completed')])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=20, default='Cash')
    table = models.OneToOneField(Table, on_delete=models.CASCADE, related_name='order', null=True, blank=True)
    modify_by = models.ForeignKey(CustomUser, default=1, on_delete=models.CASCADE)

    def total_items_count(self):
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total
    
    def total_price_amount(self):
        total = 0
        for item in self.items.all():
            total += item.total_price()
        return total

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        self.total_price = self.total_price_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.id} by {self.user.phone_number}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', default=1)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'