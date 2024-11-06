import json
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404 
from product.models import Product

class Cart:

    def __init__(self, request):
        self.request = request
        cart_cookie = self.request.COOKIES.get(settings.CART_COOKIE_NAME)

        if cart_cookie:
            try:
                self.cart = json.loads(cart_cookie)
            except json.JSONDecodeError:
                self.cart = {}
        else:
            self.cart = {}

    def add(self, product_identifier, quantity=1):
        try:
            product_id = int(product_identifier)  
            product = Product.objects.get(id=product_id)
        except (ValueError, Product.DoesNotExist):
            product = get_object_or_404(Product, name=product_identifier)

        product_id_str = str(product.id)
        if product_id_str in self.cart:
            self.cart[product_id_str]['quantity'] += quantity
        else:
            self.cart[product_id_str] = {'quantity': quantity, 'price': str(product.price)}
        
        self.save()  

    def save(self):
        cart_data = json.dumps(self.cart)
        return cart_data  # فقط داده‌ها را برمی‌گرداند

    def set_cookie(self, response):
        cart_data = self.save()
        response.set_cookie(settings.CART_COOKIE_NAME, cart_data)  # ذخیره در کوکی

    def transfer_to_session(self):
        self.request.session['cart'] = self.cart

    def remove(self, product_id):
        product_id_str = str(product_id)
        if product_id_str in self.cart:
            del self.cart[product_id_str]
            self.save()

    def iter(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())  

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())    

    def clear(self):
        self.cart = {}
        self.request.COOKIES.pop(settings.CART_COOKIE_NAME, None)  # حذف کوکی
        
    def update_quantity(self, product_id, quantity):
        product_id_str = str(product_id)
        if product_id_str in self.cart:
            if quantity > 0:
                self.cart[product_id_str]['quantity'] = quantity
            else:
                self.remove(product_id)  # اگر مقدار صفر یا منفی باشد، محصول را حذف کنید
        self.save()
