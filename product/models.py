from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category_photo = models.ImageField(upload_to='category_photos/', default='category_photos/default.jpg')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_photo = models.ImageField(upload_to='product_photos/', default='product_photos/default.jpg')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name