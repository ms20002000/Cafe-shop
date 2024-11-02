import json

from decimal import Decimal

from django.conf import settings

from django.utils import timezone

from product.models import Product
from django.shortcuts import get_object_or_404 

class Cart:

    def init(self, request):

        """

        Initialize the cart.

        """

        self.request = request

        self.cart = self.request.COOKIES.get(settings.CART_COOKIE_NAME)

        if self.cart:

            self.cart = json.loads(self.cart)

        else:

            self.cart = {}



    def add(self, product_identifier):
        # Attempt to retrieve the product by ID first
        try:
            product_id = int(product_identifier)  # Convert to int if it's a numeric string
            product = Product.objects.get(id=product_id)
        except (ValueError, Product.DoesNotExist):
            # If that fails, try to get it by name
            product = get_object_or_404(Product, name=product_identifier)

        # Now you can safely access product.id
        if product.id in self.cart:
            self.cart[product.id]['quantity'] += 1  # Update quantity if exists
        else:
            self.cart[product.id] = {'quantity': 1, 'price': product.price}  # Add new product
        self.save()  # Save the cart state


    def save(self):

        # Set the cookie with the cart data

        self.request.set_cookie(settings.CART_COOKIE_NAME, json.dumps(self.cart), max_age=3600)  # 1 hour



    def remove(self, product):

        """

        Remove a product from the cart.

        """

        product_id = str(product.id)

        if product_id in self.cart:

            del self.cart[product_id]

            self.save()



    def iter(self):

        """

        Iterate over the items in the cart and get the products

        from the database.

        """

        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:

            cart[str(product.id)]['product'] = product

        for item in cart.values():

            item['price'] = Decimal(item['price'])

            item['total_price'] = item['price'] * item['quantity']

            yield item



    def len(self):

        """

        Count all items in the cart.

        """

        return sum(item['quantity'] for item in self.cart.values())  



    def get_total_price(self):

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())    



    def clear(self):

        # Clear the cart cookie

        self.request.delete_cookie(settings.CART_COOKIE_NAME)   