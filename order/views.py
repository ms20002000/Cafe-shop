from django.shortcuts import render, redirect
from .models import Cart, Order, CartItem, OrderItem

def finalize_order(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(user=request.user, cart=cart, total_price=0)
    
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            menu_item=item.menu_item,
            quantity=item.quantity
        )
        total_price += item.menu_item.price * item.quantity
    
    order.total_price = total_price
    order.save()
    cart_items.delete() 
    return redirect('order_summary', order_id=order.id)
