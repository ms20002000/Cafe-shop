import json

from decimal import Decimal

from django.conf import settings

from django.utils import timezone



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



    def add(self, product, quantity=1, override_quantity=False):

        """

        Add a product to the cart or update its quantity.

        """

        product_id = str(product.id)

        if product_id not in self.cart:

            self.cart[product_id] = {'quantity': 0,

                                     'price': str(product.price)}

        if override_quantity:

            self.cart[product_id]['quantity'] = quantity

        else:

            self.cart[product_id]['quantity'] += quantity

        self.save()



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