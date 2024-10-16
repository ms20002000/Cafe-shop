from django.shortcuts import render, redirect
from .models import Cart, CartItem, Product

def add_to_cart(request, item_id):
    menu_item = Product.objects.get(id=item_id)
    cart = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart.html', {'cart': cart})
