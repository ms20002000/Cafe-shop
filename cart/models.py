from django.db import models
from product.models import Product
from account.models import CustomUser

class Table(models.Model):
    number = models.IntegerField()
    qr_code = models.CharField(max_length=200)

    def __str__(self):
        return self.number
    

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts')
    table = models.OneToOneField(Table, on_delete=models.CASCADE, related_name='cart')
    date = models.DateTimeField(auto_now_add=True)
    total_items = models.PositiveIntegerField(default=0)
    total_price = models.FloatField(default=0.0)

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

    def __str__(self):
        return f'Cart {self.id} for {self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f'{self.quantity} of {self.menu_item.name}'
