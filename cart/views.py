from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
from django.shortcuts import render

class CartView(LoginRequiredMixin, UserPassesTestMixin, View):
    # Ensure user passes test (you can define your own test)
    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request):
        # Retrieve the cart from the session
        cart = request.session.get('cart', {})
        
        # Render the cart.html template with the cart data
        return render(request, 'cart/cart.html', {'cart': cart})

    def post(self, request):
        # Get data from the request
        data = json.loads(request.body)
        item_name = data.get('name')
        item_count = data.get('count')
        item_price = data.get('price')v 

        # Initialize cart in session if it doesn't exist
        if 'cart' not in request.session:
            request.session['cart'] = {}

        # Update the cart with the new item
        request.session['cart'][item_name] = {
            'count': item_count,
            'price': item_price
        }

        # Save the session
        request.session.modified = True

        return JsonResponse({'message': 'Item added to cart'}, status=201)

    def put(self, request):
        # Update an existing item in the cart
        data = json.loads(request.body)
        item_name = data.get('name')
        item_count = data.get('count')

        if 'cart' in request.session and item_name in request.session['cart']:
            # Update the item count
            request.session['cart'][item_name]['count'] = item_count
            request.session.modified = True
            return JsonResponse({'message': 'Cart item updated'}, status=200)
        
        return JsonResponse({'message': 'Item not found in cart'}, status=404)

    def delete(self, request):
        # Remove an item from the cart
        data = json.loads(request.body)
        item_name = data.get('name')

        if 'cart' in request.session and item_name in request.session['cart']:
            del request.session['cart'][item_name]
            request.session.modified = True
            return JsonResponse({'message': 'Item removed from cart'}, status=204)
        
        return JsonResponse({'message': 'Item not found in cart'}, status=404)
