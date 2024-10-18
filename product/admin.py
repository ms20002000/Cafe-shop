from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_photo')  
    search_fields = ('name',)  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'category', 'product_photo')  
    list_filter = ('category', 'price')
    search_fields = ('name', 'description')  
    list_editable = ('price', 'stock_quantity')  
