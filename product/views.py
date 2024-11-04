from .forms import ProductAddForm, CategoryAddForm, CategoryUpdateForm, ProductUpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.db.models import Count, Sum


class ProductView(View):
    template_name = 'product/home.html'

    def get(self, request):
        categories = Category.objects.filter(is_available=True).annotate(product_count=Count('products'))
        products = Product.objects.annotate(total_sold=Sum('order_items__quantity')
                                    ).order_by('-total_sold')
        top_items = products[:10]
        return render(request, self.template_name, {'categories': categories, 'top_items': top_items})

    def post(self, request):
        query = request.POST.get('q', '')  
        if query == '':
            categories = Category.objects.filter(is_available=True)
            return render(request, self.template_name, {'categories': categories})
        
        products = Product.objects.filter(name__icontains=query)  

        is_empty = not products.exists()  

        context = {
            'products': products,
            'query': query,
            'is_empty': is_empty, 
        }
        return render(request, self.template_name, context)

    
def product_list(request, name):
    category = get_object_or_404(Category, name=name)
    if category.name == 'All Products':
        products = Product.objects.filter(is_available=True)
    else:    
        products = Product.objects.filter(category=category, is_available=True)
    return render(request, 'product/product_list.html', {'products': products})
    


def product_detail(request, name, product_name):
    product = get_object_or_404(Product, name=product_name)
    return render(request, 'product/product_detail.html', {'product': product})


class AddCategoryView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'product/add_category.html'

    def test_func(self):
        return self.request.user.is_admin  

    def get(self, request):
        form = CategoryAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CategoryAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')
        return render(request, self.template_name, {'form': form})


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryUpdateForm
    template_name = 'product/update_category.html'
    success_url = reverse_lazy('home')  

    def test_func(self):
        return self.request.user.is_admin


class AddProductView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'product/add_product.html'

    def test_func(self):
        return self.request.user.is_admin  

    def get(self, request):
        form = ProductAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')
        return render(request, self.template_name, {'form': form})
    

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'product/update_product.html'
    success_url = reverse_lazy('home')  

    def test_func(self):
        return self.request.user.is_admin

