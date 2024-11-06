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
            self.cart = json.loads(cart_cookie)
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
        return cart_data

    def transfer_to_session(self):
        self.request.session['cart'] = self.cart

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
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
        self.save()
        self.request.session.pop(settings.CART_COOKIE_NAME, None)