from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category


def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, 'product/list.html', {'categories': categories})
    elif request.method == 'POST':
        return render(request, 'product/list.html')
    
def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'product/list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product/detail.html', {'product': product})