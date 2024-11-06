from .models import Category, Product
from django import forms

class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_photo']

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'product_photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(
            is_available=True).exclude(name="All Products")


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
        fields = ['name', 'description', 'price', 'category', 'is_available', 'product_photo']