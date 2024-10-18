from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    category_photo = models.ImageField(upload_to='category_photos/', default='category_photos/default.jpg')

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()
    description = models.TextField()
    stock_quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_photo = models.ImageField(upload_to='product_photos/', default='product_photos/default.jpg')

    def __str__(self):
        return self.name