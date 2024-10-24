from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'product/categoty_list.html', {'categories': categories})

    
def product_list(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'product/product_list.html', {'products': products, 'category': category})


def product_detail(request, id, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/product_detail.html', {'product': product})