from .models import Category, Product
from django import forms

class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_photo']

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'stock_quantity', 'category', 'product_photo']

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_available', 'category_photo']
        labels = {
            'name': 'نام',
            'is_available': 'فعالسازی دسته بندی',
            'category_photo': 'عکس دسته‌بندی',
        }
        
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock_quantity', 'is_available', 'product_photo']