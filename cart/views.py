from cart.py import Cart
from forms.py import CartAddProductForm
from django.shortcuts import get_object_or_404 , redirect , render
from product.models import Product
from django.views.decorators.http import require_POST
"""from django.http import JsonResponse
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
        item_price = data.get('price')

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
"""
@require_POST
def cart_add(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)

    if form.is_valid():

        cd = form.cleaned_data

        cart.add(product=product,

                 quantity=cd['quantity'],

                 override_quantity=cd['override'])

    return redirect('cart:cart_detail')





@require_POST
def cart_remove(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect('cart:cart_detail')



def cart_detail(request):

    cart = Cart(request)

    for item in cart:

        item['update_quantity_form'] = CartAddProductForm(initial={

                            'quantity': item['quantity'],

                            'override': True})

    return render(request, 'cart/detail.html', {'cart': cart})