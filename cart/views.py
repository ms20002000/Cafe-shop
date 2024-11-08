from order.models import Order, OrderItem
from django.contrib import messages
from decimal import Decimal
from .forms import OrderCreateForm, CartAddProductForm
from .cart import Cart
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from product.models import Product
from django.conf import settings

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # مقدار پیش‌فرض 1
    for _ in range(quantity):
        cart.add(product_id)
    
    return _set_cart_cookie_and_redirect(cart, 'cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return _set_cart_cookie_and_redirect(cart, 'cart_detail')

@require_POST
def cart_update_quantity(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart.remove(product_id)
        cart.add(product_id)
    else:
        cart.remove(product_id)

    return _set_cart_cookie_and_redirect(cart, 'cart_detail')

def cart_detail(request):
    cart = Cart(request)
    cart_items = list(cart.iter())
    for item in cart_items:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        }) 
        item['total_price'] = item['product'].price * item['quantity']
    
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'cart': cart,
    })

def checkout(request):
    cart = Cart(request)
    order_form = OrderCreateForm()
    
    return render(request, 'cart/checkout.html', {
        'cart_items': list(cart.iter()),
        'cart': cart,
        'order_form': order_form
    })

@require_POST
def finalize_cart(request):
    cart = Cart(request)
    order_form = OrderCreateForm(request.POST)

    active_order_id = request.session.get('order_id')
    if active_order_id:
        active_order = Order.objects.filter(id=active_order_id).first()
        if active_order and active_order.status not in [Order.StatusOrder.COMPLETED, Order.StatusOrder.CANCELLED]:
            response = redirect('order_summary')
            response.delete_cookie(settings.CART_COOKIE_NAME)
            return response

    if order_form.is_valid():
        order = Order.objects.create(
            table=order_form.cleaned_data['table'],
            total_price=cart.get_total_price(),
            status=Order.StatusOrder.PENDING,
            payment_method=order_form.cleaned_data['payment_method'],
        )

        for item in cart.iter():
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity']
            )

        request.session['order_id'] = order.id
        order_history = request.session.get('order_history', [])
        order_history.append(order.id)
        request.session['order_history'] = order_history
        request.session.set_expiry(365 * 24 * 60 * 60)

        cart.clear()
        response = redirect('order_summary')
        response.delete_cookie(settings.CART_COOKIE_NAME)
        return response
    else:
        return redirect('cart_detail')

def order_history(request):
    order_history_ids = request.session.get('order_history', [])
    orders = Order.objects.filter(id__in=order_history_ids).order_by('-created_at')
    return render(request, 'cart/order_history.html', {'orders': orders})

def order_summary(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id) if order_id else None
    return render(request, 'cart/order_summary.html', {'order': order})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cart/order_summary.html', {'order': order})

def _set_cart_cookie_and_redirect(cart, redirect_url):
    response = redirect(redirect_url)
    response.set_cookie(settings.CART_COOKIE_NAME, cart.save(), max_age=3600)
    return response
